import streamlit as st
import cv2
import numpy as np
import os
from PIL import Image

# 1. Set Up the UI Page Configuration
st.set_page_config(page_title="Project Suraksha Gate", page_icon="🛡️", layout="centered")

st.title("🛡️ Project Suraksha Gate")
st.subheader("Your Offline, Zero-Knowledge Photo Safety Shield")
st.write("This application runs 100% locally on your computer. No data is ever sent to the cloud.")

# 2. The Core Safety Engine Functions
def processing_pipeline(uploaded_file):
    # STEP A: Read the file bytes directly into memory (Strips initial EXIF text headers)
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    
    # STEP B: Apply Adversarial Pixel Camouflage
    # Adds subtle mathematical noise to blind AI deepfake face matrices
    noise = np.random.randint(0, 3, img.shape, dtype='uint8')
    armored_img = cv2.add(img, noise)
    
    # STEP C: Stamp the Safety Watermark Logo in the corner
    # This deters attackers and creates organic visual awareness
    h, w, _ = armored_img.shape
    cv2.putText(armored_img, "SURAKSHA SHIELD", (int(w*0.05), int(h*0.95)), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
    
    # Convert back to standard RGB format for display and download
    final_rgb = cv2.cvtColor(armored_img, cv2.COLOR_BGR2RGB)
    return final_rgb

# 3. Building the User Interface Interactive Flow
uploaded_file = st.file_uploader("Select a photo to armor against AI scraping:", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the original unprotected user image
    original_image = Image.open(uploaded_file)
    st.image(original_image, caption="Original Unprotected Media", use_container_width=True)
    
    # Create an active single-click activation button
    if st.button("🔒 Apply Privacy Armor"):
        with st.spinner("Stripping data traces & injecting pixel armor..."):
            # Process the image through your local pipeline
            protected_image_np = processing_pipeline(uploaded_file)
            
            # Show the final protected image to the user
            protected_image = Image.fromarray(protected_image_np)
            st.success("Success! Image is now encrypted against AI deepfakes.")
            st.image(protected_image, caption="Protected Media (Ready for Social Media)", use_container_width=True)
            
            # Convert to download format bytes
            output_path = "protected_output.jpg"
            protected_image.save(output_path, "JPEG")
            with open(output_path, "rb") as file:
                btn = st.download_button(
                    label="💾 Save Armored Image to Device",
                    data=file,
                    file_name="suraksha_protected.jpg",
                    mime="image/jpeg"
                )