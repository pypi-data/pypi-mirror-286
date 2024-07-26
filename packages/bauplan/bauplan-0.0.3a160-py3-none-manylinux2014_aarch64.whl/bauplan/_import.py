import os
from io import StringIO
from typing import Any, Callable, Dict, Optional

import grpc
import yaml  # type: ignore

from . import exceptions
from ._common import _OperationContainer
from ._protobufs.bauplan_pb2 import (
    JobId,
    RunnerInfo,
)
from .bpln_proto.commander.service.v2.service_pb2 import (
    ApplyImportPlanRequest,
    ApplyImportPlanResponse,
    CreateImportPlanRequest,
    CreateImportPlanResponse,
)
from .state import ApplyPlanState, PlanImportState

JOB_STATUS_FAILED = 'FAILED'
JOB_STATUS_SUCCESS = 'SUCCESS'
JOB_STATUS_CANCELLED = 'CANCELLED'


def _validate_plan_yaml(plan_yaml: str) -> None:
    if not isinstance(plan_yaml, str):
        raise exceptions.InvalidPlanError('invalid plan YAML; plan YAML string is required')
    if not plan_yaml or plan_yaml.strip() == '':
        raise exceptions.InvalidPlanError('invalid plan YAML; plan YAML string is required')

    try:
        yaml.safe_load(StringIO(plan_yaml))
    except yaml.YAMLError as e:
        raise e


def _handle_apply_import_log(log: RunnerInfo, state: ApplyPlanState) -> None:
    if log.runner_event.apply_plan_done.error_message or log.runner_event.apply_plan_done.success:
        if log.runner_event.apply_plan_done.error_message:
            state.error = log.runner_event.apply_plan_done.error_message
            state.job_status = JOB_STATUS_FAILED
            if os.getenv('BPLN_DEBUG'):
                print(f'Apply plan failed, error is: {state.error}')
            return True
        if log.runner_event.apply_plan_done.success:
            state.job_status = JOB_STATUS_SUCCESS
            if os.getenv('BPLN_DEBUG'):
                print('Apply plan successful')
            return True
    return False


def _timeout_factory_apply(seconds: int) -> Callable:
    def _timeout(sig: Any, frame: Any) -> None:
        raise TimeoutError(f'Plan import execution took longer than {seconds} seconds')

    return _timeout


def _handle_plan_import_log(log: RunnerInfo, state: PlanImportState) -> None:
    if (
        log.runner_event.import_plan_created.error_message
        or log.runner_event.import_plan_created.plan_as_yaml
    ):
        if log.runner_event.import_plan_created.error_message:
            state.error = log.runner_event.import_plan_created.error_message
            state.job_status = JOB_STATUS_FAILED
            if os.getenv('BPLN_DEBUG'):
                print(f'Plan import failed, error is: {log.runner_event.import_plan_created.error_message}')
            return True
        if log.runner_event.import_plan_created.success:
            state.job_status = JOB_STATUS_SUCCESS
            state.plan_yaml = log.runner_event.import_plan_created.plan_as_yaml
            if os.getenv('BPLN_DEBUG'):
                print('Create import plan success')
            return True
    return False


def _timeout_factory_plan(seconds: int) -> Callable:
    def _timeout(sig: Any, frame: Any) -> None:
        raise TimeoutError(f'Plan import execution took longer than {seconds} seconds')

    return _timeout


class _Import(_OperationContainer):
    def plan(self, search_string: str, args: Optional[Dict[str, str]] | None = None) -> PlanImportState:
        """
        Create a table import plan from an S3 location.
        This is the equivalent of running through the CLI the ``bauplan import plan`` command.
        """
        if not isinstance(search_string, str):
            raise ValueError(
                "invalid search string; search string is required, e.g., 's3://bucket-name/*.parquet'"
            )
        if not search_string or search_string.strip() == '':
            raise ValueError("search string is required, e.g., 's3://bucket-name/*.parquet'")
        search_string = search_string.strip()
        if not search_string.startswith('s3://'):
            raise ValueError('search string must be an S3 path')
        if not isinstance(search_string, str):
            raise ValueError("invalid output file; output file is required, e.g., 'my_import_plan.yaml'")

        client_v1, metadata_v1 = self._common.get_commander_and_metadata(args)
        client_v2, metadata_v2 = self._common.get_commander_v2_and_metadata(args)

        if os.getenv('BPLN_DEBUG'):
            print('Create import plan', 'search_string', search_string)
        response: CreateImportPlanResponse = client_v2.CreateImportPlan(
            CreateImportPlanRequest(search_string=search_string, args=args or {}), metadata=metadata_v2
        )
        job_id = JobId(id=response.job_id)
        if os.getenv('BPLN_DEBUG'):
            print('Create import plan job_id', response.job_id)

        log_stream: grpc.Call = client_v1.SubscribeLogs(job_id, metadata=metadata_v1)
        state = PlanImportState(job_id=job_id.id)
        for log in log_stream:
            if _handle_plan_import_log(log, state):
                break
        return state

    def apply(
        self,
        plan_yaml: str,
        branch_name: str,
        table_name: str,
        args: Optional[Dict[str, str]] | None = None,
    ) -> ApplyPlanState:
        """
        Apply a Bauplan table import plan for a given branch and table.
        This is the equivalent of running through the CLI the ``bauplan import apply`` command.
        """
        _validate_plan_yaml(plan_yaml)
        if not isinstance(table_name, str) and table_name.strip():
            raise ValueError("table is required, e.g. 'table_name'")
        if not isinstance(branch_name, str) and branch_name.strip():
            raise ValueError("branch is required, e.g. 'myname.mybranch'")

        client_v1, metadata_v1 = self._common.get_commander_and_metadata(args)
        client_v2, metadata_v2 = self._common.get_commander_v2_and_metadata(args)

        if os.getenv('BPLN_DEBUG'):
            print('Apply import plan', 'plan_yaml\n', plan_yaml)
            print('Apply import plan', 'branch', branch_name)
            print('Apply import plan', 'table', table_name)
        response: ApplyImportPlanResponse = client_v2.ApplyImportPlan(
            ApplyImportPlanRequest(
                plan_yaml=plan_yaml, branch=branch_name, table=table_name, args=args or {}
            ),
            metadata=metadata_v2,
        )
        job_id = JobId(id=response.job_id)
        if os.getenv('BPLN_DEBUG'):
            print('Apply import plan job_id', response.job_id)
        log_stream: grpc.Call = client_v1.SubscribeLogs(job_id, metadata=metadata_v1)
        state = ApplyPlanState(job_id=job_id.id)
        for log in log_stream:
            if _handle_apply_import_log(log, state):
                break
        return state
