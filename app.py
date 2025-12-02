import streamlit as st
from PIL import Image
import io
import numpy as np

st.set_page_config(page_title="Image Processor", layout="wide")
st.title("🎨 Simple Image Processing App")

# Sidebar untuk settings
with st.sidebar:
    st.header("Settings")
    operation = st.selectbox(
        "Select Operation",
        ["Grayscale", "Rotate", "Resize", "Flip", "Brightness", "Blur"],
    )

    if operation == "Rotate":
        angle = st.slider("Rotation Angle", -180, 180, 45)
    elif operation == "Resize":
        width = st.slider("Width", 100, 1000, 300)
        height = st.slider("Height", 100, 1000, 300)
    elif operation == "Brightness":
        brightness = st.slider("Brightness", 0.1, 3.0, 1.0)
    elif operation == "Blur":
        blur_radius = st.slider("Blur Radius", 0, 10, 2)

# Main area
uploaded = st.file_uploader(
    "📤 Upload an image",
    type=["png", "jpg", "jpeg", "bmp", "tiff"],
    help="Upload any image file",
)

if uploaded:
    # Buka gambar
    image = Image.open(uploaded)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🖼️ Original Image")
        st.image(image, use_column_width=True)
        st.caption(f"Size: {image.size} | Mode: {image.mode}")

    with col2:
        st.subheader("✨ Processed Image")

        # Proses gambar sesuai operasi
        processed = image.copy()

        if operation == "Grayscale":
            if processed.mode != "L":
                processed = processed.convert("L")

        elif operation == "Rotate":
            processed = processed.rotate(angle, expand=True)

        elif operation == "Resize":
            processed = processed.resize((width, height))

        elif operation == "Flip":
            processed = processed.transpose(Image.FLIP_LEFT_RIGHT)

        elif operation == "Brightness":
            from PIL import ImageEnhance

            enhancer = ImageEnhance.Brightness(processed)
            processed = enhancer.enhance(brightness)

        elif operation == "Blur":
            processed = processed.filter(ImageFilter.GaussianFilter(blur_radius))

        # Tampilkan hasil
        st.image(processed, use_column_width=True)

        # Download button
        buffered = io.BytesIO()
        processed.save(buffered, format="PNG")

        st.download_button(
            label="⬇️ Download Processed Image",
            data=buffered.getvalue(),
            file_name="processed_image.png",
            mime="image/png",
        )

# Info footer
st.markdown("---")
st.caption("Made with Streamlit • Simple Image Processing App")
