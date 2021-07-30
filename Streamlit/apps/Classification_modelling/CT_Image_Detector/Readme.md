### This folder is for CT scan detection using Yolov5

#### Steps
- Install the dependencies using the code:
```
pip install requirements.txt
```
- Run app.py in the parent folder

#### Info
- Don't delete the images folder, the model saves images uploaded in the UI here and deletes it later when done inference.

- The pretrained model in in the model folder.

- yolov5 is clones from the repo "https://github.com/ultralytics/yolov5.git", to get the predictions.

- CT_detector.py is the main class which regulates the infernece pipeline.

- main.py is used for the streamlit UI and backend code.
