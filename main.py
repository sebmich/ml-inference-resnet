from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from app.utils import get_top_predictions


app = FastAPI()

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        predictions = get_top_predictions(image_bytes)
        return JSONResponse(content={"predictions": predictions})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/health")
async def health():
    return {"status": "ok"}

