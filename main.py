
import streamlit as st
from PIL import Image
import os
import shutil

def split_image_into_tiles(image, tiles_width, tiles_height, output_folder="output_tiles"):
    # A4 dimensions in pixels at 300 DPI
    A4_WIDTH, A4_HEIGHT = 2480, 3508
    image_width, image_height = tiles_width * A4_WIDTH, tiles_height * A4_HEIGHT
    resized_image = image.resize((image_width, image_height))

    # Create output folder
    os.makedirs(output_folder, exist_ok=True)

    for row in range(tiles_height):
        for col in range(tiles_width):
            left = col * A4_WIDTH
            upper = row * A4_HEIGHT
            right = left + A4_WIDTH
            lower = upper + A4_HEIGHT

            tile = resized_image.crop((left, upper, right, lower))
            tile.save(os.path.join(output_folder, f"tile_{row + 1}_{col + 1}.jpg"))

    # Zip the folder
    shutil.make_archive(output_folder, 'zip', output_folder)

st.title("Image Splitter App")
st.write("Upload an image, split it into A4 tiles, and download the result.")

uploaded_file = st.file_uploader("Upload your image", type=["jpg", "jpeg", "png"])
tiles_width = st.number_input("Number of A4 tiles (width)", min_value=1, value=5)
tiles_height = st.number_input("Number of A4 tiles (height)", min_value=1, value=3)

if uploaded_file:
    with open("uploaded_image.jpg", "wb") as f:
        f.write(uploaded_file.getbuffer())
    img = Image.open("uploaded_image.jpg")

    if st.button("Split Image"):
        split_image_into_tiles(img, tiles_width, tiles_height)
        with open("output_tiles.zip", "rb") as f:
            st.download_button("Download Tiled Image", f, file_name="output_tiles.zip")
