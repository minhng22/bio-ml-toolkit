import torch
import torchvision.transforms as transforms
from torchvision.models import vgg16
from PIL import Image

def load_stem_cell_model():
    model = vgg16(pretrained=True)
    num_features = model.classifier[6].in_features
    model.classifier[6] = torch.nn.Linear(num_features, 2)
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

def predict_stem_cell_differentiation(model, image_tensor):
    with torch.no_grad():
        outputs = model(image_tensor)
        probabilities = torch.nn.functional.softmax(outputs, dim=1)
        _, predicted = torch.max(probabilities, 1)
    return predicted.item(), probabilities.squeeze().tolist()

def run_experiment(image_paths):
    model = load_stem_cell_model()
    results = []
    for i, image_path in enumerate(image_paths):
        image_tensor = preprocess_image(image_path)
        prediction, probabilities = predict_stem_cell_differentiation(model, image_tensor)
        results.append({
            'image_path': image_path,
            'prediction': 'Differentiated' if prediction == 1 else 'Not Differentiated',
            'probabilities': probabilities
        })
    return results