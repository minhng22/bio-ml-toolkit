from pkgs.stemcellprediction.experiment.resnet50 import run_experiment

def run_model(selected_model, image_paths):
    if selected_model == 'resnet50':
        print("Running ResNet50 model...")
        return run_experiment(image_paths)
    elif selected_model == 'inceptionv3':
        print("Running InceptionV3 model...")
    elif selected_model == 'efficientnet':
        print("Running EfficientNet model...")
    elif selected_model == 'vgg16':
        print("Running VGG16 model...")
    else:
        print("No valid model selected.")