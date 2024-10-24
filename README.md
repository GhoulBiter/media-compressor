# **Streamlit-Based Media Compression Tool**

This project is a secure and flexible media compression tool built using Python, Streamlit, FFMPEG, and Pillow. It allows users to select directories, choose video or image files, and apply compression settings such as format conversion, resolution limit, and quality/bitrate adjustment. The tool also includes logging and basic security checks.

This tool is designed for developers and content creators who need an efficient, secure, and flexible way to compress videos and images for web or media applications. By leveraging modern tools like Streamlit, FFMPEG, and Pillow, it provides a user-friendly interface for file selection and compression with flexible configuration options.

## **Features**

- **Video Compression**: Convert and compress videos to formats such as MP4 and WebM using FFMPEG.
- **Image Compression**: Compress and convert images to formats such as JPG, PNG, and WebP using Pillow.
- **File Selection**: Select specific files or entire directories, with support for filtering by file type.
- **Compression Settings**: Adjust resolution limits, select output formats, and modify quality/bitrate settings.
- **Logging**: Comprehensive logging is included to track the progress and any potential issues during the compression process.
- **Security**: Includes basic validation of file paths and MIME types to enhance security.
- **Progress Tracking**: The tool displays a progress bar while processing files to give users real-time feedback.

## **Technologies Used**

- **Streamlit**: Used for building the interactive user interface.
- **FFMPEG**: Handles video compression and format conversion.
- **Pillow**: Processes and compresses images.
- **Python**: Core programming language used for the project.

## **Requirements**

To run this tool, you will need the following libraries installed:

- **Python 3.10+** (Python 3.12.7 was used originally)
- **FFMPEG**: Must be installed and available in your system's PATH. It should include support for `libvpx` (for WebM encoding) and other necessary codecs.
- **Pillow**
- **Streamlit**
- **python-magic-bin** (for Windows) or **python-magic** (for Linux/Mac)
- **pyclamd** (Optional, for virus scanning; current features are disabled by default)

**Note**: **pyclamd** is used for virus scanning but is disabled by default due to potential issues with ClamAV in certain environments. If you wish to enable virus scanning, ensure that ClamAV is properly installed **AND** running, then update the `scan_file_for_viruses` function in the code by commenting out or removing the early default ```return True``` line to re-enable scanning.

You can install the required Python packages via `pip`:

```bash
pip install streamlit Pillow moviepy python-magic-bin pyclamd
```

If using Linux or Mac:

```bash
pip install streamlit Pillow moviepy python-magic pyclamd
```

Ensure that FFMPEG is installed and added to your system's PATH. You can download a pre-built version of FFMPEG from [Gyan.dev](https://www.gyan.dev/ffmpeg/builds/) or [ffmpeg.org](https://ffmpeg.org/download.html).

## **Installation**

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Set up a virtual environment (optional but recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Linux/Mac
   venv\Scripts\activate     # On Windows
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure FFMPEG:**

   Make sure FFMPEG is installed with the necessary codecs, particularly `libvpx` (for WebM), `libx264`, and `libvorbis`. You can verify the installation by running:

   ```bash
   ffmpeg -version
   ```

   If the codecs are missing, download the full FFMPEG build from [Gyan.dev](https://www.gyan.dev/ffmpeg/builds/).

5. **Run the application:**

   ```bash
   streamlit run main_app.py
   ```

6. **Use the web interface:**

   The application will launch in your default web browser. You can now interact with the tool through the provided interface.

## **Usage**

### **Interface Overview**

- **Enter Directory Path**: Provide the absolute path to the directory where your media files are stored.
- **Parse Subdirectories**: Optionally, enable parsing of subdirectories.
- **File Selection**: Choose which file types and directories to include.
- **Compression Settings**:
  - **Output Format**: Choose the format for compressed files (MP4, WebM, JPG, PNG, or WebP).
  - **Resolution Limit**: Set a maximum width/height for video/image resolution.
  - **Quality**: Adjust the compression quality for **images** (1-100).
  - **Bitrate**: Set the target bitrate for **videos** (in kilobits per second).

### **Steps to Compress Files:**

1. Enter the absolute path of the directory containing your media files.
2. Select whether to parse subdirectories.
3. Choose the file types and directories you wish to include.
4. Select the desired compression settings:
   - **Output Format** (e.g., MP4 for videos or JPG for images).
   - **Resolution Limit**: Define the maximum resolution.
   - **Quality/Bitrate**: For images, select quality (1-100); for videos, set the bitrate.
5. Click **Compress and Convert** to begin processing. The tool will show a progress bar as the files are compressed.

### **Logging**

Logging can be configured to display either **Basic** or **Verbose** output. Logs are written to a file called `app.log` in the same directory as the application. This file will track:

- Files being processed.
- Any errors encountered.
- Details of the compression process.

### **Supported Formats**

- **Video**: MP4, WebM, AVI, MOV, MKV.
- **Image**: JPG, PNG, WebP, TIFF, BMP, GIF.

## **Configuration File (`config.yaml`)**

This project uses a configuration-driven approach to handle security settings, logging preferences, and file processing constraints. All configuration settings can be easily modified in the `config.yaml` file, allowing for flexible control over file handling without changing the Python code.

### **Configuration Settings**

#### **1. Security Settings**

The security section controls access restrictions, allowed file types, and size limits.

- **`base_directory`**: Specifies the base directory where file operations are allowed. Access to directories outside this base path is restricted for security purposes. Ensure this path is set to a valid directory on your system.

  Example:

  ```yaml
  base_directory: "~/Files_Directory"
  ```

- **`allowed_mime_types`**: Defines the MIME types that are allowed for output files. These are checked to ensure the file being processed is of an acceptable type (e.g., `image/`, `video/`).

  Example:

  ```yaml
  allowed_mime_types:
    - image/
    - video/
  ```

- **`allowed_extensions`**: Lists the specific file extensions that are allowed for output files. Only files with these extensions will be processed.

  Example:

  ```yaml
  allowed_extensions:
    - jpg
    - png
    - mp4
    - webm
  ```

- **`max_file_size_mb`**: Sets a limit on the maximum file size (in MB) that can be processed. If set to `0`, there is no file size limit.

  Example:

  ```yaml
  max_file_size_mb: 100  # Limit file size to 100 MB
  ```

  If you don't want any limit, you can set this to `0`:

  ```yaml
  max_file_size_mb: 0  # No limit on file size
  ```

#### **2. Logging Settings**

The logging section controls the verbosity of logging output.

- **`level`**: Defines the logging level. You can adjust it to one of the following levels: `DEBUG`, `INFO`, `WARNING`, `ERROR`, depending on how much information you want to see in the logs.

  Example:

  ```yaml
  level: INFO
  ```

  - **DEBUG**: Shows detailed information for debugging purposes.
  - **INFO**: Shows general information about the program's operations.
  - **WARNING**: Shows warnings about potential issues.
  - **ERROR**: Shows only error messages.

### **Modifying the Configuration**

1. Open the `config.yaml` file in the root of the project.
2. Adjust the security or logging settings as needed, ensuring paths and values are valid.
3. Save your changes.
4. The application will automatically load the new settings the next time it's run.

### **Example Configuration (`config.yaml`)**

```yaml
security:
  base_directory: "~/Files_Directory"
  allowed_mime_types:
    - image/
    - video/
  allowed_extensions:
    - jpg
    - png
    - mp4
    - webm
  max_file_size_mb: 100  # Maximum file size in MB

logging:
  level: INFO  # Set the logging level to INFO
```

### Example Workflow

1. Place your media files in the `~/Files_Directory` folder, or specify another base directory in the configuration file.
2. Example directory structure:

```text
~/Files_Directory/
├── child_directory_1/
│ └── image1.jpg
├── child_directory_2/
│ └── video1.mp4
```

## **Troubleshooting**

### **Missing FFMPEG Codecs**

If you encounter errors related to missing codecs (e.g., `libvpx`), ensure your FFMPEG installation includes support for WebM encoding and other necessary codecs. Reinstall or download a build from [Gyan.dev](https://www.gyan.dev/ffmpeg/builds/).

One possible issue is that moviepy comes with a shipped version of ffmpeg that does not include the libvpx codec. The workaround is to download the full (not essentials!) version of ffmpeg and overwrite the ffmpeg binaries in your venv, conda env or python libraries directories with the ones from the ffmpeg version you downloaded.

### **Image.ANTIALIASING Errors**

This might be an issue you encounter depending on the specific python, Pillow and moviepy versions you use. The latest version of moviepy (v1.0.3) has a change that was pushed to fix the deprecation of ```Image.ANTIALIASING``` in place for ```Image.LANCZOS``` but this was not reflected accurately when I set up the conda environment here. In this case, the fix was quite simple which was to manually replace the code in a specific function in ```moviepy/video/fx/resize.py``` with code from the github repo's master branch.

Around line 24, you will find a try/except block. Replace the try block's contents with the following:

``` python
try:
  # TRY USING PIL/PILLOW AS RESIZER
  from PIL import Image
  import numpy as np
  def resizer(pic, new_size):
      new_size = list(map(int, new_size))[::-1]
      # shape = pic.shape
      # if len(shape) == 3:
      #     newshape = (new_size[0], new_size[1], shape[2])
      # else:
      #     newshape = (new_size[0], new_size[1])

      pil_img = Image.fromarray(pic)
      # resized_pil = pil_img.resize(new_size[::-1], Image.ANTIALIASING)
      resized_pil = pil_img.resize(new_size[::-1], Image.LANCZOS)
      # arr = np.fromstring(resized_pil.tostring(), dtype="uint8")
      # arr.reshape(newshape)
      return np.array(resized_pil)

  # return (resizer, [])
      
  resizer.origin = "PIL"
```

### **File Access Issues**

Make sure the files you are trying to compress are accessible from the directory you specify. Ensure that directory paths are correctly validated and that your user permissions allow access to those files.

### **Error Logs**

In case of any processing errors, check the `app.log` file for detailed error messages. This file will help you troubleshoot specific issues related to compression or file access.

## **Future Enhancements**

The following features are planned for future versions:

- **CNN-Based Enhancements**: Planned features include using Convolutional Neural Networks (CNNs) for content-aware compression, where important regions of a video (e.g., faces) are compressed with higher quality, and denoising techniques to enhance video quality post-compression.

- **Preset Profiles**: Ready-to-use compression settings for various use cases.

- **Advanced User Preferences**: Save and load user-defined settings for easier use.

- **Output File-Type Independent Settings Fields**: Creating separate fields for each output file type selected and making output file types correspond to different types of input file types through one-to-one or one-to-many mapping.

- **Allowing Optional Placement in a Compressed Files Directory**: Users will have the option to specify a directory where all compressed files will be saved, keeping the original directories intact rather than the compressed files being placed with the original files.

## **License**

This project is licensed under the MIT License.

## **Contributing**

If you would like to contribute to this project, feel free to submit a pull request or open an issue with any suggestions or bug reports.

---

### **Contact**

For any questions or issues, please feel free to contact the project maintainer.
