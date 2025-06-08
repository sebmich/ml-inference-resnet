from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from torchvision import transforms
from torchvision.models import resnet18, ResNet18_Weights
from PIL import Image
import torch
import json
import io

# Load labels
with open("imagenet_class_index.json", "r") as f:
    idx_to_label = json.load(f)

# Load model
weights = ResNet18_Weights.IMAGENET1K_V1
model = resnet18(weights=weights)
model.eval()

# Image transform
transform = weights.transforms()

# Init app
app = FastAPI()

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img_t = transform(image).unsqueeze(0)  # add batch dimension

    with torch.no_grad():
        output = model(img_t)
        _, index = torch.max(output, 1)
        class_id = str(index.item())
        label = idx_to_label[class_id][1]

    return JSONResponse(content={"class_id": class_id, "label": label})

