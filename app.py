import os
import streamlit as st
import logging
from utils import configure_logging
from utils.security_checks import validate_path, BASE_DIR
from compressors import ImageCompressor, VideoCompressor

# Configure logging
st.title("Secure File Compression and Conversion Tool with Logging")

log_level = st.selectbox("Select logging level:", options=["Basic", "Verbose"])
if log_level == "Basic":
    configure_logging(logging.INFO)
elif log_level == "Verbose":
    configure_logging(logging.DEBUG)

logger = logging.getLogger(__name__)

# Get directory path input
dir_path = st.text_input("Enter the absolute path to the directory:", BASE_DIR)

# Checkbox for parsing subdirectories
parse_subdirs = st.checkbox("Parse subdirectories", value=True)

if dir_path and os.path.isdir(dir_path):
    # Validate the directory path
    if not validate_path(dir_path):
        st.error("Invalid directory path. Access is restricted.")
    else:
        # Retrieve folder structure
        folder_structure = {}
        for root, dirs, files in os.walk(dir_path):
            if not parse_subdirs:
                dirs[:] = []  # Do not traverse subdirectories
            folder = os.path.abspath(root)
            folder_structure[folder] = files

        if folder_structure:
            # File Selection
            st.subheader("File Selection")
            all_file_types = [
                "mp4",
                "webm",
                "avi",
                "mov",
                "mkv",
                "jpg",
                "jpeg",
                "png",
                "webp",
                "tiff",
                "bmp",
                "gif",
            ]
            file_types = st.multiselect(
                "Select file types to include:",
                options=all_file_types,
                default=all_file_types,
            )
            selected_dirs = st.multiselect(
                "Select directories to include:",
                options=list(folder_structure.keys()),
                default=list(folder_structure.keys()),
            )

            # Compression Settings
            st.subheader("Compression Settings")

            # Output Format
            compress_format = st.selectbox(
                "Choose output format:", options=["webm", "webp", "mp4", "jpg", "png"]
            )

            # Resolution Limit
            resolution_limit = st.number_input(
                "Resolution limit (max width or height in pixels):",
                value=1080,
                min_value=100,
            )

            # Quality or Bitrate
            if compress_format in ["jpg", "png", "webp"]:
                quality = st.slider(
                    "Quality (1-100):", min_value=1, max_value=100, value=75
                )
                compressor = ImageCompressor(
                    output_format=compress_format,
                    resolution_limit=resolution_limit,
                    quality=quality,
                )
            elif compress_format in ["mp4", "webm"]:
                bitrate = st.number_input(
                    "Bitrate (in kilobits per second):", value=1000, min_value=100
                )
                compressor = VideoCompressor(
                    output_format=compress_format,
                    resolution_limit=resolution_limit,
                    bitrate=bitrate,
                )
            else:
                st.error("Unsupported output format selected.")
                st.stop()

            # Process Files
            if st.button("Compress and Convert"):
                total_files = 0
                selected_files = []

                for dir in selected_dirs:
                    files = folder_structure[dir]
                    for file in files:
                        file_ext = os.path.splitext(file)[-1].lstrip(".").lower()
                        if file_ext in file_types:
                            file_path = os.path.join(dir, file)
                            selected_files.append(file_path)
                            total_files += 1

                if total_files == 0:
                    st.warning("No files selected for processing.")
                else:
                    progress_bar = st.progress(0)
                    processed_files = 0

                    for file_path in selected_files:
                        file_ext = os.path.splitext(file_path)[-1].lstrip(".").lower()
                        if file_ext in ["mp4", "webm", "avi", "mov", "mkv"]:
                            result = compressor.compress_video(file_path)
                        elif file_ext in [
                            "jpg",
                            "jpeg",
                            "png",
                            "webp",
                            "tiff",
                            "bmp",
                            "gif",
                        ]:
                            result = compressor.compress_image(file_path)
                        else:
                            st.warning(f"Unsupported file type: {file_path}")
                            continue

                        if result:
                            st.write(f"Compressed file saved at: {result}")
                        else:
                            st.error(f"Failed to process file: {file_path}")

                        processed_files += 1
                        progress_bar.progress(processed_files / total_files)

                    st.success("Processing completed.")
else:
    if dir_path:
        st.error("Invalid directory path. Please enter a valid path.")
