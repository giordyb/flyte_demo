#
#%%
from flytekit.models.launch_plan import LaunchPlanState
from flytekit.common import utils, schedules, tasks
from flytekit.sdk.tasks import python_task, outputs, inputs
from flytekit.sdk.types import Types
from flytekit.sdk.workflow import workflow_class, Output, Input
from flytekit.common.tasks.task import SdkTask


@workflow_class
class myworkflow(object):
    string_in = Input(Types.String, required=True, help="input string")
    csv_url = "https://www.stats.govt.nz/assets/Uploads/Annual-enterprise-survey/Annual-enterprise-survey-2018-financial-year-provisional/Download-data/annual-enterprise-survey-2018-financial-year-provisional-csv.csv"
    dataset = Input(Types.CSV, default=Types.CSV.create_at_known_location(
        csv_url), help="A CSV File")

    download_dataset = SdkTask.fetch("flytedemo","development","fk_tasks.tasks_and_workflow.download_dataset","f7fdff3213e101fea7feeb03f5bf88d3f0b0814c")
    return_dataset = download_dataset(dataset=dataset)
    read_pickle = SdkTask.fetch("flytedemo","development","fk_tasks.tasks_and_workflow.read_pickle","f7fdff3213e101fea7feeb03f5bf88d3f0b0814c")
    return_pickle = read_pickle(dataset=return_dataset.outputs.out)
    
    myoutput = Output(return_pickle.outputs.csv_head, sdk_type=Types.String)

# %%
