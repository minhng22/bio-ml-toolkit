from pkgs.stemcellprediction.experiment.resnet50 import run_experiment
from pkgs.stemcellprediction.experiment.inceptionv3 import run_experiment as run_inceptionv3_experiment
from pkgs.stemcellprediction.experiment.efficientnet import run_experiment as run_efficientnet_experiment
from pkgs.stemcellprediction.experiment.vgg16 import run_experiment as run_vgg16_experiment
from pkgs.stemcellprediction.experiment.types import SupportedModel

def run_model(selected_model: str, image_paths):
    if selected_model == SupportedModel.PT_RESNET50.value:
        print("Running ResNet50 model...")
        return run_experiment(image_paths)
    elif selected_model == SupportedModel.PT_INCEPTIONV3.value:
        print("Running InceptionV3 model...")
        return run_inceptionv3_experiment(image_paths)
    elif selected_model == SupportedModel.PT_EFFICIENTNET.value:
        print("Running EfficientNet model...")
        return run_efficientnet_experiment(image_paths)
    elif selected_model == SupportedModel.PT_VGG16.value:
        print("Running VGG16 model...")
        return run_vgg16_experiment(image_paths)
    else:
        print("No valid model selected.")