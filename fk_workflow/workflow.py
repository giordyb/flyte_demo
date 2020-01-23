#
#%%
from flytekit.models.launch_plan import LaunchPlanState
from flytekit.common import utils, schedules, tasks
from flytekit.sdk.tasks import python_task, outputs, inputs
from flytekit.sdk.types import Types
from flytekit.sdk.workflow import workflow_class, Output, Input
from flytekit.common.tasks.task import SdkTask
uppercase_task = SdkTask.fetch_latest("flytedemo","development","fk_tasks.tasks_and_workflow.uppercase_task")
reverse_task = SdkTask.fetch_latest("flytedemo","development","fk_tasks.tasks_and_workflow.reverse_task")
read_pickle = SdkTask.fetch_latest("flytedemo","development","fk_tasks.tasks_and_workflow.read_pickle")
download_dataset = SdkTask.fetch_latest("flytedemo","development","fk_tasks.tasks_and_workflow.download_dataset")


@workflow_class
class myworkflow(object):
    string_in = Input(Types.String, required=True, help="input string")
    csv_url = "https://www.stats.govt.nz/assets/Uploads/Annual-enterprise-survey/Annual-enterprise-survey-2018-financial-year-provisional/Download-data/annual-enterprise-survey-2018-financial-year-provisional-csv.csv"

    dataset = Input(Types.CSV, default=Types.CSV.create_at_known_location(csv_url),
                    help="A CSV File")
    return_dataset = download_dataset(dataset=dataset)
    return_pickle = read_pickle(dataset=return_dataset.outputs.out)
    upper_out = uppercase_task(input_string=string_in)
    reversed_out = reverse_task(input_string=upper_out.outputs.output_string)
    myoutput = Output(return_pickle.outputs.csv_head, sdk_type=Types.String)

    mystringoutput = Output(reversed_out.outputs.rev_output_string, sdk_type=Types.String)
