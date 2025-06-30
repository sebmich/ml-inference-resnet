
# dispatcher.py

import time
import requests
import threading
import queue
import os

WORKER_ENDPOINT = "http://localhost:8002/predict"
job_queue = queue.Queue()

def worker_thread():
    while True:
        if not job_queue.empty():
            job = job_queue.get()
            image_path = os.path.join('images', job)
            try:
                with open(image_path, 'rb') as f:
                    files = {'file': f}
                    res = requests.post(WORKER_ENDPOINT, files=files)
                    print(f"✅ Job: {job} => {res.status_code}, {res.json()}")
            except Exception as e:
                print(f"❌ Failed to process job {job}: {e}")
        time.sleep(1)

def dispatch(repeat=1):
    # Queue all image files in the directory, multiple times
    images = [f for f in os.listdir('images') if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    for _ in range(repeat):
        for image in images:
            job_queue.put(image)
            print(f"📨 Job queued: {image}")
            time.sleep(0.5)  # optional delay between jobs

if __name__ == "__main__":
    threading.Thread(target=worker_thread, daemon=True).start()
    dispatch(repeat=5)  # send each image 5 times (for load test)

