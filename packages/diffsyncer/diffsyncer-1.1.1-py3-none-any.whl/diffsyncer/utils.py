from pathlib import Path
import shutil


def get_qrcode_images(directory: str):
    directory_path = Path(directory)
    image_files = list(directory_path.glob("**/*.jpg")) + list(
        directory_path.glob("**/*.png")
    )
    return [str(file) for file in image_files]


def remove_dir(directory: str):
    directory_path = Path(directory)
    shutil.rmtree(directory_path, ignore_errors=True)
