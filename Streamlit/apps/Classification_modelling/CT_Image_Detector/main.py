import os
import time
import shutil

from PIL import Image
import torch
import streamlit as st

from apps.Classification_modelling.CT_Image_Detector.CT_detector import Detector


def predict(image_path, conf, thick):
    dect = Detector(image_path, conf, thick)
    preds = dect.predict_()
    if os.path.exists(preds['label']):
        with open(preds['label'], 'r') as f:
            pred = f.read()
            label = int(pred.split()[0])
            score = round(float(pred.split()[-1]), 2)
    else:
        score=100.0
        label=0
    return preds['image'], score, label

def detect():
    st.title('CT Scan Detector')
    st.write("")
    st.markdown("A Robust CT scan detector to identify infected region in Covid19 patient's CT scans")
    st.markdown('This feature provides accurate results in seconds.')
    conf = st.sidebar.slider("Confidence Threshold:", 0.1, 0.9, 0.3, step=0.1)
    thick = st.sidebar.slider("Boundingbox Thickness:", 1, 5, 1)
    file_up = st.file_uploader("Upload an image", type = "jpg")
    if file_up is not None:
        with open("apps/Classification_modelling/CT_Image_Detector/images/image.jpg", "wb") as f:
            f.write(file_up.getbuffer())
        image = Image.open("apps/Classification_modelling/CT_Image_Detector/images/image.jpg")

        c1, c2 = st.beta_columns([1,1])

        with c1:
            st.image(image, caption = 'Uploaded Image.', use_column_width = True)
        st.write("")
        st.write("Just a second ... Predicting 🚀")
        image, score, label = predict("apps/Classification_modelling/CT_Image_Detector/images/image.jpg", conf, thick)

        image = Image.open(image)
        with c2:
            st.image(image, caption = 'Predicted Image.', use_column_width = True)
        if label == 1:
            st.write("The CT scan shows that, you have been affected by Covid19 with confidence {}%".format(score*100))
        else:
            st.write("The CT scan shows that, you're not been affected by Covid19 with confidence {}%".format(score))

        os.remove("apps/Classification_modelling/CT_Image_Detector/images/image.jpg")
        shutil.rmtree("apps/Classification_modelling/CT_Image_Detector/runs/")
