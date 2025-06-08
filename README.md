ML Inference API (ResNet18 + FastAPI)

This project is an image classification API using a pre-trained ResNet18 model from PyTorch, served with FastAPI.

Setup and Run Locally:

1. Clone the repo:
git clone https://github.com/sebmich/ml-inference-resnet.git
cd ml-inference-resnet

2. Create and activate a virtual environment:
python3 -m venv venv
source venv/bin/activate

3. Install dependencies:
pip install -r requirements.txt

4. Run the FastAPI server:
uvicorn main:app --reload

5. Open your browser at http://127.0.0.1:8000/docs to test the API.

How to Use the API:

Send a POST request with an image file to /predict. Example using curl:
curl -X POST "http://127.0.0.1:8000/predict" -F "file=@your_image.jpg"


Project Structure:

main.py             # FastAPI app code
requirements.txt    # Python dependencies
README.md           # This file

