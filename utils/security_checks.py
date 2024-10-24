import os
import magic  # You'll need to install python-magic-bin on Windows
import logging
import pyclamd  # Requires ClamAV to be installed and running
from utils.read_config import load_config

# Define the base directory to restrict file access
BASE_DIR = os.path.abspath(os.path.expanduser("~/Desktop/projects"))
logger = logging.getLogger(__name__)


# Initialize configuration
config = load_config()

# Extract security-related settings
BASE_DIR = os.path.abspath(os.path.expanduser(config["security"]["base_directory"]))
ALLOWED_MIME_TYPES = config["security"]["allowed_mime_types"]
ALLOWED_EXTENSIONS = config["security"]["allowed_extensions"]
MAX_FILE_SIZE_MB = config["security"]["max_file_size_mb"]

logger = logging.getLogger(__name__)
logging.basicConfig(level=config["logging"]["level"])


def validate_path(path):
    """
    Validates that the given path is within the allowed BASE_DIR.
    """
    abs_path = os.path.abspath(path)
    if not abs_path.startswith(BASE_DIR):
        logger.error(f"Access denied for path: {abs_path}")
        return False
    return True


def validate_file_type(file_path, expected_types=ALLOWED_MIME_TYPES):
    """
    Validates the actual MIME type of a file against expected types.
    """
    try:
        mime_type = magic.from_file(file_path, mime=True)
        if any(mime_type.startswith(expected) for expected in expected_types):
            logger.debug(f"File {file_path} has valid MIME type: {mime_type}")
            return True
        else:
            logger.error(f"Invalid MIME type for file {file_path}: {mime_type}")
            return False
    except Exception as e:
        logger.exception(f"Error checking MIME type for file {file_path}: {e}")
        return False


def validate_extension(file_path):
    """
    Validates that the file has an allowed extension.
    """
    ext = os.path.splitext(file_path)[-1].lower().lstrip(".")
    if ext not in ALLOWED_EXTENSIONS:
        logger.error(f"File extension {ext} is not allowed for file: {file_path}")
        return False
    return True


def validate_file_size(file_path):
    """
    Validates that the file size is within the allowed limit.
    """
    if MAX_FILE_SIZE_MB == 0:  # Skip file size check if set to 0
        return True

    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    if file_size_mb > MAX_FILE_SIZE_MB:
        logger.error(
            f"File {file_path} exceeds the maximum size of {MAX_FILE_SIZE_MB} MB."
        )
        return False
    return True


def scan_file_for_viruses(file_path):
    """
    Scans a file using ClamAV to check for viruses.
    """

    # Skip virus scanning for now
    return True

    try:
        cd = pyclamd.ClamdAgnostic()
        if cd.ping():
            scan_result = cd.scan_file(file_path)
            if scan_result is None:
                logger.debug(f"File {file_path} is clean.")
                return True
            else:
                logger.error(f"Virus detected in file {file_path}: {scan_result}")
                return False
        else:
            logger.error("ClamAV daemon is not running.")
            return False
    except Exception as e:
        logger.exception(f"Error scanning file {file_path} for viruses: {e}")
        return False
