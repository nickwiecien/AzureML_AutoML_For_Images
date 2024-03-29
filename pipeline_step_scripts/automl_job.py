from azureml.core import Run, Dataset
import argparse
from azureml.core.compute import ComputeTarget
import os

#Parse Input Arguments
parser = argparse.ArgumentParser("Retrieve AML Dataset and Launch AutoML for Images Job")
parser.add_argument("--model_name", type=str, required=True)
parser.add_argument("--dataset_name", type=str, required=True)
parser.add_argument("--compute_name", type=str, required=True)
args, _ = parser.parse_known_args()
model_name = args.model_name
dataset_name = args.dataset_name
compute_name = args.compute_name

#Get current run and AML workspace
current_run = Run.get_context()
ws = current_run.experiment.workspace
experiment_name = current_run.experiment.name

compute_target = ComputeTarget(workspace=ws, name=compute_name)

from azureml.automl.core.shared.constants import ImageTask
from azureml.train.automl import AutoMLImageConfig
from azureml.train.hyperdrive import BanditPolicy, RandomParameterSampling
from azureml.train.hyperdrive import choice, uniform

from azureml.core import Dataset
dataset = Dataset.get_by_name(ws, name=dataset_name)
formatted_datasets = [('Training_Data', dataset)]


from azureml.train.automl import AutoMLImageConfig
from azureml.train.hyperdrive import GridParameterSampling, choice
from azureml.automl.core.shared.constants import ImageTask

# AutoML configuration docs
# https://docs.microsoft.com/en-us/azure/machine-learning/how-to-auto-train-image-models
# https://docs.microsoft.com/en-us/azure/machine-learning/how-to-use-automl-small-object-detect?msclkid=6746843ab6ea11ec9aa5a6acbb3b0498

parameter_space = {
    "model": choice(
        {
            'model_name': choice('fasterrcnn_resnet50_fpn'),
            'learning_rate': uniform(0.0001, 0.001),
            'optimizer': choice('sgd', 'adam', 'adamw'),
            'min_size': choice(1000,1500), # model-specific
            'tile_grid_size': choice('(4, 2)', '(3, 2)', '(5, 3)'), #Enables automatic tiling of images
        },
        {
            'model_name': choice('fasterrcnn_resnet101_fpn'),
            'learning_rate': uniform(0.0001, 0.001),
            'optimizer': choice('sgd', 'adam', 'adamw'),
            'min_size': choice(1000,1500), # model-specific
            'tile_grid_size': choice('(4, 2)', '(3, 2)', '(5, 3)'),
        }
    ),
}

tuning_settings = {
    "iterations": 15,
    "max_concurrent_iterations": 5,
    "hyperparameter_sampling": RandomParameterSampling(parameter_space),
    "early_termination_policy": BanditPolicy(
        evaluation_interval=2, slack_factor=0.2, delay_evaluation=6
    ),
}

image_automl_config = AutoMLImageConfig(
    task=ImageTask.IMAGE_OBJECT_DETECTION,
    compute_target=compute_target,
    training_data=dataset,
    **tuning_settings
)

new_run = current_run.experiment.submit(image_automl_config)
new_run.wait_for_completion()

best_child_run = new_run.get_best_child()
metrics = best_child_run.get_metrics()
mAP = max(metrics['mean_average_precision'])
precision = max(metrics['precision'])
recall = max(metrics['recall'])

updated_tags = {'Mean Average Precision': mAP, 'Precision': precision, 'Recall': recall}

os.makedirs('tmp')

best_child_run.download_files(prefix='./outputs', output_directory='tmp',append_prefix=True)
best_child_run.download_files(prefix='./train_artifacts', output_directory='tmp',append_prefix=True)

current_run.upload_folder('automl_outputs', 'tmp')

model = current_run.register_model(model_name, model_path='automl_outputs', model_framework='AUTOML', tags=updated_tags, datasets=formatted_datasets, sample_input_dataset = dataset)
