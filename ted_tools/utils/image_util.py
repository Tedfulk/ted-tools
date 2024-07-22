from PIL import Image
import os


def convert_webp_to_jpeg(file_path):
    """
    Check if the given file is a WebP image and convert it to a JPG file.

    Parameters:
    - file_path: str - The path to the file to be checked and converted.

    Returns:
    - str - The path to the converted JPG file, or an error message.
    """
    # Check if the file extension is .webp
    if not file_path.lower().endswith(".webp"):
        return "The file is not a WebP image based on its extension."

    try:
        # Attempt to open the image to confirm it's a valid WebP file
        with Image.open(file_path) as img:
            # Define the new file name with a .jpeg extension
            new_file_path = os.path.splitext(file_path)[0] + ".jpeg"

            # Convert and save the image as a JPG file
            img.convert("RGB").save(new_file_path, "JPEG")

            # return f"Converted to JPG and saved as: {new_file_path}"
            return new_file_path
    except IOError:
        return "Failed to open or process the file. Please ensure it is a valid WebP image."
