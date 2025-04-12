import torch
import torchvision.transforms as transforms
from torchvision.models import resnet50
from PIL import Image

def load_model():
    model = resnet50(pretrained=True)
    model.eval()
    return model

def preprocess_image(image_path):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    image = Image.open(image_path).convert('RGB')
    return transform(image).unsqueeze(0)

def predict(model, image_tensor):
    with torch.no_grad():
        outputs = model(image_tensor)
        _, predicted = outputs.topk(3, 1, True, True)
    return predicted

def run_experiment(image_paths):
    print('image paths ', image_paths)
    model = load_model()
    for i, image_path in enumerate(image_paths):
        image_tensor = preprocess_image(image_path)
        predictions = predict(model, image_tensor)
        print(f"Image {i+1} predictions:")
        for idx in predictions[0]:
            print(f"  Class ID: {idx.item()}")