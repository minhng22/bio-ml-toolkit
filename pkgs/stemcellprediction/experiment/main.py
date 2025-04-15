from pkgs.stemcellprediction.experiment.resnet50 import run_experiment
from pkgs.stemcellprediction.experiment.inceptionv3 import run_experiment as run_inceptionv3_experiment
from pkgs.stemcellprediction.experiment.efficientnet import run_experiment as run_efficientnet_experiment
from pkgs.stemcellprediction.experiment.vgg16 import run_experiment as run_vgg16_experiment

def run_model(selected_model, image_paths):
    if selected_model == 'resnet50':
        print("Running ResNet50 model...")
        return run_experiment(image_paths)
    elif selected_model == 'inceptionv3':
        print("Running InceptionV3 model...")
        return run_inceptionv3_experiment(image_paths)
    elif selected_model == 'efficientnet':
        print("Running EfficientNet model...")
        return run_efficientnet_experiment(image_paths)
    elif selected_model == 'vgg16':
        print("Running VGG16 model...")
        return run_vgg16_experiment(image_paths)
    else:
        print("No valid model selected.")