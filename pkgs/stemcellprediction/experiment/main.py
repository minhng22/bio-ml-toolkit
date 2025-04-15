from pkgs.stemcellprediction.experiment.resnet50 import run_experiment
from pkgs.webapp.stem_cell_page import uploaded_images

def run_model(selected_model):
    if selected_model == 'resnet50':
        print("Running ResNet50 model...")
        return run_experiment(uploaded_images)
    elif selected_model == 'inceptionv3':
        print("Running InceptionV3 model...")
    elif selected_model == 'efficientnet':
        print("Running EfficientNet model...")
    elif selected_model == 'vgg16':
        print("Running VGG16 model...")
    else:
        print("No valid model selected.")