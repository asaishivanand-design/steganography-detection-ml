import streamlit as st
import cv2
import numpy as np
import pickle

st.title("🔍 Steganography Detection Tool")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg"])

def extract_features(img):
    img = cv2.resize(img, (128,128))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    features = []
    features.append(np.mean(gray))
    features.append(np.std(gray))
    
    edges = cv2.Canny(gray, 50, 150)
    features.append(np.mean(edges))
    
    features.append(np.mean(np.abs(np.diff(gray))))
    
    return np.array(features).reshape(1, -1)

if uploaded_file:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    
    st.image(img, caption="Uploaded Image", use_column_width=True)
    
    features = extract_features(img)
    
    # simple rule (since no saved model yet)
    if features[0][1] > 50:
        st.error("⚠️ Steganography Detected")
    else:
        st.success("✅ Clean Image")
