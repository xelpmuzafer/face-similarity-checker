import os
from itertools import combinations
import streamlit as st
from deepface import DeepFace
from PIL import Image

# Directory containing the images
data_dir = "data"

# Streamlit UI
st.title("Image Similarity Checker with DeepFace")

# Display all images in the directory
image_files = [os.path.join(data_dir, file) for file in os.listdir(data_dir) if file.endswith((".png", ".jpg", ".jpeg"))]

if not image_files:
    st.error("No images found in the specified directory.")
else:
    st.subheader("Images in the Folder")
    cols = st.columns(4)  # Display images in columns

    for idx, image_path in enumerate(image_files):
        with cols[idx % 4]:
            img = Image.open(image_path)
            st.image(img, caption=os.path.basename(image_path))

    # Button to start matching
    if st.button("Match Images"):
        st.subheader("Matching Results")

        same_person_pairs = []

        # Perform pairwise comparison
        for file1, file2 in combinations(image_files, 2):
            try:
                result = DeepFace.verify(file1, file2, model_name="VGG-Face", enforce_detection=False)
                print(result)
                similarity = result['verified']
                if similarity:
                    same_person_pairs.append((file1, file2, result['distance']))
            except Exception as e:
                st.warning(f"Error comparing {file1} and {file2}: {e}")

        # Display results
        if same_person_pairs:
            for file1, file2, distance in same_person_pairs:
                col1, col2 = st.columns(2)

                with col1:
                    img1 = Image.open(file1)
                    st.image(img1, caption=os.path.basename(file1))

                with col2:
                    img2 = Image.open(file2)
                    st.image(img2, caption=os.path.basename(file2))

                st.success(f"These images are likely of the same person (Distance: {distance:.2f})")
        else:
            st.info("No images in the directory are of the same person.")
