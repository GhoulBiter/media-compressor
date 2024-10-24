import os
from PIL import Image
import logging
from utils.security_checks import (
    validate_path,
    validate_file_type,
    scan_file_for_viruses,
)

logger = logging.getLogger(__name__)


class ImageCompressor:
    def __init__(self, output_format, resolution_limit, quality):
        self.output_format = output_format.upper()
        self.resolution_limit = resolution_limit
        self.quality = quality  # For images, quality is between 1-100

    def compress_image(self, file_path):
        """
        Compresses and converts an image file.

        Args:
            file_path (str): The path to the image file.

        Returns:
            str: The path to the compressed image file, or None if an error occurred.
        """
        try:
            if not validate_path(file_path):
                return None

            if not validate_file_type(file_path, ["image/"]):
                return None

            if not scan_file_for_viruses(file_path):
                return None

            file_path = os.path.abspath(file_path)
            logger.info(f"Processing image file: {file_path}")

            image = Image.open(file_path)

            # Resize if necessary
            width, height = image.size
            max_dimension = max(width, height)
            if max_dimension > self.resolution_limit:
                scale_factor = self.resolution_limit / max_dimension
                new_size = (int(width * scale_factor), int(height * scale_factor))
                logger.debug(f"Resizing image to: {new_size}")
                image = image.resize(new_size, Image.Resampling.LANCZOS)
            else:
                logger.debug("No resizing needed for image.")

            # Set output file path
            output_file = (
                os.path.splitext(file_path)[0]
                + f"_compressed.{self.output_format.lower()}"
            )

            # Save the image with the specified quality
            image.save(output_file, format=self.output_format, quality=self.quality)

            logger.info(f"Compressed image saved at: {output_file}")
            return output_file

        except Exception as e:
            logger.exception(f"Error processing image {file_path}: {e}")
            return None
