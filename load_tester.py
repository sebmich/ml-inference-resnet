import json
import time
from typing import Tuple
from barazmoon import BarAzmoon

''''class MyLoadTester(BarAzmoon):
    def get_request_data(self) -> Tuple[str, bytes]:
        with open("test.jpeg", "rb") as f:
            image_bytes = f.read()
        return "img_1", image_bytes


# Wrap image in multipart/form-data format
        form = FormData()
        form.add_field(
            name="file",                # must match FastAPI param name
            value=image_bytes,
            filename="test.jpeg",
            content_type="image/jpeg"
        )
        return "img_1", form
    def process_response(self, sent_data_id: str, response: json):
        print(f"{sent_data_id}: Response => {response}")

# Read workload from file
with open("workload.txt") as f:
    # Read the entire line and split on spaces
    workload = [int(x) for x in f.read().split()]


# Replace with your actual FastAPI inference endpoint
endpoint = "http://127.0.0.1:8000/predict"

# Start load testing
tester = MyLoadTester(
    workload=workload,
    endpoint=endpoint,
    http_method="post"
)
tester.start()'''

import json
import time
import random
from typing import Tuple
from pathlib import Path
from barazmoon import BarAzmoon

class MyLoadTester(BarAzmoon):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image_paths = []
        for ext in ["*.jpg", "*.jpeg", "*.JPEG", "*.png"]:
            self.image_paths += list(Path("images").glob(ext))
        if not self.image_paths:
            raise FileNotFoundError("No image files found in 'images/' directory.")

    def get_request_data(self) -> Tuple[str, bytes]:
        image_path = random.choice(self.image_paths)
        with open(image_path, "rb") as f:
            image_bytes = f.read()
        print(f"=> Sending image: {image_path.name}")
        return image_path.name, image_bytes  # Return raw bytes, NOT FormData

    def process_response(self, sent_data_id: str, response: json):
        print(f"{sent_data_id}: Response => {response}")

if __name__ == "__main__":
    try:
        with open("workload.txt") as f:
            workload = [int(x) for x in f.read().split()]
            print(f"=> Loaded workload: {workload}")
    except Exception as e:
        print("❌ Failed to load workload.txt:", e)
        workload = [1, 2, 3]

    endpoint = "http://127.0.0.1:8000/predict"

    try:
        tester = MyLoadTester(
            workload=workload,
            endpoint=endpoint,
            http_method="post"
        )
        print("✅ Load tester initialized. Starting test...")
        tester.start()
    except Exception as e:
        print("❌ Error running load tester:", e)


