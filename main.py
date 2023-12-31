from io import BytesIO

import numpy as np
import tensorflow as tf
import uvicorn
from PIL import Image
from fastapi import FastAPI, UploadFile

app: FastAPI = FastAPI()

MODEL=tf.keras.models.load_model("./2")


class_names=["Early Blight", "Late Blight", "Healthy"]

@app.get("/ping")
async def ping():
    return "Hello, I am alive "

def read_file_as_image(data) -> np.ndarray:
    image=np.array(Image.open(BytesIO(data)))
    return image

@app.post("/predict")
async def predict(
        file: UploadFile

):
    image= read_file_as_image(await file.read())
    img_batch=np.expand_dims(image,0)
    predictions= MODEL.predict(img_batch)
    predicted_class=class_names[np.argmax(predictions[0])]
    confidence=np.max(predictions[0])
    return{
        'class':predicted_class,
        'confidence': float(confidence)
    }

if __name__ == "__main__":
    import os

    # Get the port number from the environment variable if available (for deployment)
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

