import os
from moviepy.editor import VideoFileClip
from moviepy.video.fx import resize
import logging
from utils.security_checks import (
    validate_path,
    validate_file_type,
    scan_file_for_viruses,
)

logger = logging.getLogger(__name__)


class VideoCompressor:
    def __init__(self, output_format, resolution_limit, bitrate):
        self.output_format = output_format.lower()
        self.resolution_limit = resolution_limit
        self.bitrate = bitrate  # In kilobits per second (e.g., '500k')

    def compress_video(self, file_path):
        """
        Compresses and converts a video file.

        Args:
            file_path (str): The path to the video file.

        Returns:
            str: The path to the compressed video file, or None if an error occurred.
        """
        try:
            if not validate_path(file_path):
                return None

            if not validate_file_type(file_path, ["video/"]):
                return None

            if not scan_file_for_viruses(file_path):
                return None

            file_path = os.path.abspath(file_path)
            logger.info(f"Processing video file: {file_path}")

            video = VideoFileClip(file_path)

            # Resize if necessary
            width, height = video.size
            max_dimension = max(width, height)
            if max_dimension > self.resolution_limit:
                scale_factor = self.resolution_limit / max_dimension
                new_size = (int(width * scale_factor), int(height * scale_factor))
                logger.debug(f"Resizing video to: {new_size}")
                video = resize.resize(video, new_size)
            else:
                logger.debug("No resizing needed for video.")

            # Set output file path
            output_file = (
                os.path.splitext(file_path)[0] + f"_compressed.{self.output_format}"
            )

            # Select codec based on output format
            if self.output_format == "webm":
                codec = "libvpx-vp9"
                audio_codec = "libvorbis"
            elif self.output_format == "mp4":
                codec = "libx264"
                audio_codec = "aac"
            else:
                logger.error(f"Unsupported output format: {self.output_format}")
                return None

            # Write the compressed video
            video.write_videofile(
                output_file,
                codec=codec,
                audio_codec=audio_codec,
                bitrate=f"{self.bitrate}k",
                preset="medium",
                threads=4,
                logger=None,  # Suppress moviepy's own logging
            )
            video.close()

            logger.info(f"Compressed video saved at: {output_file}")
            return output_file

        except Exception as e:
            logger.exception(f"Error processing video {file_path}: {e}")
            return None
