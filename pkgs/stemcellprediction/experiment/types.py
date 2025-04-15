# an enum contains model dropdown options
from enum import Enum

class SupportedModel(Enum):
    PT_RESNET50 = "pretrained ResNet50"
    PT_INCEPTIONV3 = "pretrained InceptionV3"
    PT_EFFICIENTNET = "pretrained EfficientNet"
    PT_VGG16 = "pretrained VGG16"
