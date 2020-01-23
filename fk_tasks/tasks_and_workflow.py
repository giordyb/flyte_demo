#
#%%
import datetime
import urllib.request as _request
import pandas as pd
from flytekit.models.launch_plan import LaunchPlanState
from flytekit.common import utils, schedules
from flytekit.sdk.tasks import python_task, outputs, inputs
from flytekit.sdk.types import Types
from flytekit.sdk.workflow import workflow_class, Output, Input


@inputs(input_string=Types.String)
@outputs(output_string=Types.String)
@python_task
def uppercase_task(wf_params,input_string,output_string):
    output_string.set(input_string.upper())

@inputs(input_string=Types.String)
@outputs(rev_output_string=Types.String)
@python_task
def reverse_task(wf_params,input_string,rev_output_string):
    myoutput = input_string
    myoutput = myoutput[::-1]
    rev_output_string.set(myoutput)


@inputs(dataset=Types.CSV)
@outputs(out=Types.Blob)
@python_task
def download_dataset(wf_params,dataset,out):
    dataset.download()
    wf_params.logging.info(dataset.local_path)
    df = pd.read_csv(dataset.local_path)
    wf_params.logging.info(df.head())
    with utils.AutoDeletingTempDir('test') as tmpdir:
        df.to_pickle(tmpdir.name + '/dataset.pkl')
        out.set(tmpdir.name + '/dataset.pkl')

    

@inputs(dataset=Types.Blob)
@outputs(csv_head=Types.String)
@python_task
def read_pickle(wf_params,dataset,csv_head):
    dataset.download()
    unpickled_df = pd.read_pickle(dataset.local_path)
    wf_params.logging.info(type(unpickled_df))
    csv_head.set(unpickled_df.head().to_string())



@workflow_class
class myworkflow(object):
    csv_url = "https://www.stats.govt.nz/assets/Uploads/Annual-enterprise-survey/Annual-enterprise-survey-2018-financial-year-provisional/Download-data/annual-enterprise-survey-2018-financial-year-provisional-csv.csv"
    string_in = Input(Types.String, required=True, help="input string")
    dataset = Input(Types.CSV, default=Types.CSV.create_at_known_location(
        csv_url),
                    help="A CSV File")

    return_dataset = download_dataset(dataset=dataset)
    return_pickle = read_pickle(dataset=return_dataset.outputs.out)
    upper_out = uppercase_task(input_string=string_in)
    reversed_out = reverse_task(input_string=upper_out.outputs.output_string)
    myoutput = Output(return_pickle.outputs.csv_head, sdk_type=Types.String)
    mystringoutput = Output(reversed_out.outputs.rev_output_string, sdk_type=Types.String)
