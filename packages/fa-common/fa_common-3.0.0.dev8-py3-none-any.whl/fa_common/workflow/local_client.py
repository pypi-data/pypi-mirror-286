import asyncio
from copy import deepcopy
from typing import Any, Optional, Union

from fa_common.models import BucketMeta

from .base_client import WorkflowBaseClient
from .local_utils import run_prefect_jobs
from .models import JobTemplate, LocalWorkflowRun, WorkflowId


class LocalWorkflowClient(WorkflowBaseClient):
    """
    Singleton client for interacting with local-workflows.
    Is a wrapper over the existing local-workflows python client to provide specialist functions for
    the Job/Module workflow.

    Please don't use it directly, use `fa_common.workflow.utils.get_workflow_client`.
    """

    __instance = None
    # local_workflow_client = None

    def __new__(cls) -> "LocalWorkflowClient":
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
            # app = get_current_app()
            # cls.__instance.local_workflow_client = app.local_workflow_client  # type: ignore
        return cls.__instance

    async def run_job(self, job_base: JobTemplate) -> LocalWorkflowRun:
        if isinstance(job_base.inputs, list):
            jobs = []
            for i, inp in enumerate(job_base.inputs):
                job = deepcopy(job_base)
                job.custom_id = i + 1
                job.name = f"{job.name}-subjob-{i+1}"
                job.inputs = inp
                jobs.append(job)
        else:
            jobs = [job_base]

        flow_run = run_prefect_jobs(jobs, flow_name=job_base.module.name, ignore_clean_up=True, return_state=True)
        flow_run_name = f"{job_base.module.name}: {flow_run.id}"
        return LocalWorkflowRun(
            id=WorkflowId(uid=str(flow_run.id), name=flow_run_name), state=flow_run.type.value, message=flow_run.message, template=job_base
        )

    async def get_workflow(
        self,
        bucket_id: str,
        workflow_id: Union[int, str],
        output: bool = False,
        file_refs: bool = True,
        namespace: Optional[str] = None,
    ) -> LocalWorkflowRun:
        """
        This Python function defines an abstract method `get_workflow` that retrieves
        information about a workflow run.
        """
        print("get_workflow is currently a placeholder")
        await asyncio.sleep(0)
        return None

    async def delete_workflow(
        self,
        bucket_id: str,
        workflow_id: Union[
            int,
            str,
        ],
        namespace: Optional[str],
        force_data_delete: Optional[bool] = False,
    ):
        """
        :param force_data_delete: if True, if workflow does not exist in the records,
        it would yet continue with deletion of artifacts and output data.
        """
        print("delete_workflow is currently a placeholder")
        await asyncio.sleep(0)

    async def _delete_workflow_artifacts(self, workflow_id: Union[int, str]):
        """
        This method deletes artifacts of a workflow
        """
        print("_delete_workflow_artifacts is currently a placeholder")
        await asyncio.sleep(0)

    async def retry_workflow(self, workflow_id: Union[int, str], user_id: Optional[str] = None):
        """
        Retry the workflow.
        """
        print("retry_workflow is currently a placeholder")
        await asyncio.sleep(0)

    async def get_workflow_log(
        self,
        workflow_id: WorkflowId,
        bucket_meta: BucketMeta,
        namespace: str | None = None,
    ) -> dict[Any, Any]:
        """
        This abstract method defines an asynchronous function to retrieve
        the workflow log based on the workflow ID, with optional parameters
        for bucket ID and namespace.
        """
        print("get_workflow_log is currently a placeholder")
        await asyncio.sleep(0)
        return {}

    async def get_job_log(
        self,
        job_id: Union[int, str],
        workflow_id: WorkflowId,
        user_id: Optional[str] = None,
    ):
        """
        This method gets the logs of a job.
        """
        print("get_job_log is currently a placeholder")
        await asyncio.sleep(0)
