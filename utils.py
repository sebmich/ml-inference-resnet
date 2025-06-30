from torchvision.models import resnet18, ResNet18_Weights
from PIL import Image
import torch
import io

weights = ResNet18_Weights.IMAGENET1K_V1
model = resnet18(weights=weights)
model.eval()
transform = weights.transforms()

def get_top_predictions(image_bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img_t = transform(image).unsqueeze(0)
    with torch.no_grad():
        outputs = model(img_t)
        _, index = torch.max(outputs, 1)
        idx = index.item()
    category = weights.meta["categories"][idx]
    return {"class_id": idx, "label": category}

