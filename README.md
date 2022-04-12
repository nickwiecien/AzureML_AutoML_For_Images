# AzureML AutoML for Images Pipeline Sample (Object Detection)

This repository contains sample code for creating an Azure Machine Learning pipeline to launch an AutoML for Images (specifically focused on object detection) using a labeled dataset sourced from an [AML-linked datastore](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-access-data), created and exported using (Azure ML's Data Labeling Tool)[https://docs.microsoft.com/en-us/azure/machine-learning/how-to-label-data]. Instructions for creating a labeled dataset, and executing the code within are contained in the document below.

![Azure ML Object Detection Model Training (AutoML for Images)](img/automl.png?raw=true "Azure ML Object Detection Model Training (AutoML for Images)")

## Prerequisites

To execute the code contained within this repo, you will need access to an Azure Machine Learning workspace. Additionally, we recommend creating a separate storage container within the Azure Storage resource that gets created with the AML workspace, and linking that as a standalone datastore for holding images. See the link below for details on creating an Azure ML workspace.

[Quickstart: Create an Azure Machine Learning Workspace](https://docs.microsoft.com/en-us/azure/machine-learning/quickstart-create-resources).

## Getting Started

 - As a first step, create an Azure Machine Learning workspace. Then, create a separate storage container in the default AML blob storage account for your images. You can link this new storage account as a separate datastore to your AML workspace by following [this document](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-connect-data-ui?tabs=credential).

 - After creating an AML workspace and linking your new storage account/datastore, upload images to this datastore using either Azure Storage Explorer, AzCopy, PowerShell, the Azure CLI, or via the blob storage UI in the Azure portal. See the [document linked here](https://docs.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-portal) for more details on the listed options.

 - Once you have uploaded images to your attached datastore you should be able to browse your files using the `Browse (Preview)` feature in the datastore viewed through the AML Studio. Next, create a Data Labeling project, add your images to a new dataset, and begin labeling your images. Follow these guides on [creating an image labeling project](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-create-image-labeling-projects), [labeling images](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-label-data), and [exporting labeled datasets](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-use-labeled-dataset) to create and export a labeled object detection dataset. 

 - After creating and exporting your labeled object detection dataset it is time to set up and run the Azure Machine Learning pipeline for executing an AutoML for Images training job. While you can execute the notebooks attached in this repo locally, we recommend using the pre-configured `Python 3.8 - AzureML` environment available on an AML Compute Instance. Details about creating a Compute Instance and running Jupyter, Jupyter Lab, VSCode, tec. can be found here. <i>Note:</i> It is <u>HIGHLY</u> encouraged that you set up your compute instance to turn off on a schedule, and stop the instance when not in use to avoid unnecessary charges. Once you have created your compute instance, you can clone this repo by opening a terminal window and executing the following command:

 ```
git clone https://github.com/nickwiecien/AzureML_AutoML_For_Images
 ```

 - After cloning this repo navigate to the `./AzureML_AutoML_For_Images/PipelineDefinition.ipynb` notebook. Prior to executing cells in this notebook, update the variable values under the `Trigger a Pipeline Execution from the Notebook` header, specifically change these values: `MY_EXPERIMENT`, `MY_MODEL`, and `MY_DATASET`. The last value should be the name of your exported labeled dataset, the two prior should reflect something meaningful towards your experiment and the model you are creating. Once these values are updated run all cells in the notebook.

 - You can monitor experiment progress by navigating through the experiments tab in the AML Studio. The pipeline included here will kickoff an AutoML for Images child training run. By drilling into that experiment you can observe performance across models/epochs. Once the job completes, the best performing model will be registered in the AML workspace by default.

 - To test your registered model navigate to the `./AzureML_AutoML_For_Images/VisionModelTesting.ipynb` notebook. Here, you will need to update the model name, and sample image path to successfully run the notebook. <i>Note:</i> This section should be considered under construction. Additional changes are forthcoming to ensure this works as expected.
