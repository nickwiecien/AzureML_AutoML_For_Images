# AzureML AutoML for Images Pipeline Sample (Object Detection)

<i>Extended documentation coming soon...</i>

To execute the code contained within this repo, you will need access to an Azure Machine Learning workspace. As a first step, upload and label a set of images using AML's data labeling tools. [See the following documents for guidance on creating a labeled image dataset](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-create-image-labeling-projects). Once you have completed your labeling, export your dataset as an Azure Machine Learning dataset.

To create an AML pipeline for training a custom object detection model, run the notebook located at `./PipelineDefinition.ipynb`. Be sure to update the named datasets/models/experiments throughout to align with your data.

Following training, you can test your model directly by executing the `./VisionModelTesting.ipynb` notebook. Update the parameter values throughout to reflect location of your sample images as well as your trained model.

