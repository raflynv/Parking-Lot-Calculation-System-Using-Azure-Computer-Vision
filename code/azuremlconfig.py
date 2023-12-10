import os
import azureml.core
from azureml.core.experiment import Experiment

print("\n------------Azure Machine Learning Configuration-------------")
subscription_id = os.environ.get("SUBSCRIPTION_ID", "23494b49-7f7e-48e7-84a8-71d0f2d4854a")
resource_group = os.environ.get("RESOURCE_GROUP", "mygroup")
workspace_name = os.environ.get("WORKSPACE_NAME", "MLtest")

from azureml.core import Workspace
try:
    ws = Workspace(subscription_id = subscription_id, resource_group = resource_group, workspace_name = workspace_name)
    ws.write_config()
    print("Workspace Berjalan")
except:
    print("Error: Workspace not found")

ws = Workspace.from_config()
print('Current Azure ML Workspace: ' + ws.name, 
      'Region: ' + ws.location, 
      'Resource Group: ' + ws.resource_group, sep='\n')

AMLexperiment = 'ParkingCounter'
from azureml.core import experiment
experiment = Experiment(workspace=ws, name = AMLexperiment)
experiment
print("----------------------------End------------------------------\n")