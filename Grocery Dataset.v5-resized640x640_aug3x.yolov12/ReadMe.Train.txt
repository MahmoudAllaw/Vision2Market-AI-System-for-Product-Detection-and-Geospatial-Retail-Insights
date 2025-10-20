*Activate Environment :
. .\.venv\Scripts\Activate.ps1

*Enable GPU Training Cuda
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

*Check Yolo if it can see the GPU
yolo checks



*start training model (for first time use only !):
yolo task=detect mode=train model=yolo12.yaml data="C:/Users/mahmo/Downloads/AI-Product detect & search/Grocery Dataset.v5-resized640x640_aug3x.yolov12/data.yaml" epochs=30 batch=4 name=train1 amp=false

* Test 1 img :
yolo task=detect mode=predict model="C:/Users/mahmo/Downloads/AI-Product detect `& search/runs/detect/train/weights/best.pt" source="C:/Users/mahmo/Downloads/AI-Product detect `& search/test.jpg" save=True
