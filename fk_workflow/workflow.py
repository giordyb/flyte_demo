#
#%%
from flytekit.models.launch_plan import LaunchPlanState
from flytekit.common import utils, schedules, tasks
from flytekit.sdk.tasks import python_task, outputs, inputs
from flytekit.sdk.types import Types
from flytekit.sdk.workflow import workflow_class, Output, Input
from flytekit.common.tasks.task import SdkTask
read_task = SdkTask.fetch_latest("flytedemo","development","fk_tasks.tasks_and_workflow.download_dataset","1e0d95cc82b85cdd96feab3c6f9b6e2f7baba216")
download_task = SdkTask.fetch_latest("flytedemo","development","fk_tasks.tasks_and_workflow.download_dataset","1e0d95cc82b85cdd96feab3c6f9b6e2f7baba216")
@workflow_class
class myworkflow(object):
    string_in = Input(Types.String, required=True, help="input string")
    dataset = Input(Types.CSV, default=Types.CSV.create_at_known_location(
        "http://172.16.140.171:8000/label_summary.csv"),
                    help="A CSV File")
    return_dataset = download_task(dataset=dataset)
    return_pickle = read_task(dataset=return_dataset.outputs.out)
    myoutput = Output(return_pickle.outputs.csv_head, sdk_type=Types.String)
# %%
