"""
Utility functions for managing directories and files related to news articles.

This module includes functions for creating directories to save images and Excel files,
moving images from a source directory to a new directory, and zipping the contents of a 
folder.

Functions:
- create_new_dir_to_save_images(src_dir: str) -> str: Creates a new directory within the 
  specified source directory and returns the path to the new directory.
- move_images_to_repository(new_dir: str, src_dir_images: str) -> None: Moves images from 
  the source directory to the specified new directory and handles errors during the process.
- zip_folder(source_folder: str, target_folder: str) -> None: Zips the contents of the source 
  folder into a zip file located in the target folder.

Exceptions:
- The functions may raise exceptions related to file and directory operations, which should be 
  handled by the caller.

Logging:
- Logs informational messages and errors related to directory and file operations.
"""
import os
import shutil
import logging
import zipfile


def create_new_dir_to_save_images(src_dir):
    """
    Creates a new directory to save images and Excel files.

    Args:
        src_dir (str): The source directory where the new directory will be created.

    Returns:
        str: The path of the newly created directory.

    Raises:
        Exception: If there is an error creating the directory.
    """
    logging.info("Creating new dir to save excel and images from search...")
    try:
        new_dir_name = "news_images"

        new_dir_path = os.path.join(src_dir, new_dir_name)

        os.makedirs(new_dir_path, exist_ok=True)

    except ImportError as exception:
        logging.error("Error creating new dir: %s ", exception)
        raise

    logging.info("New dir Created")
    return new_dir_path


def move_images_to_repository(new_dir, src_dir_images):
    """
    Moves images from the source directory to a new directory.

    Args:
        new_dir (str): The destination directory where images will be moved.
        src_dir_images (str): The source directory containing the images to move.

    Raises:
        shutil.Error: If there is an error moving files.
        Exception: If there is an unexpected error during the process.
    """
    logging.info("Moving news pictures to new dir")
    try:
        for file_name in os.listdir(src_dir_images):
            full_file_name = os.path.join(src_dir_images, file_name)
            shutil.move(full_file_name, new_dir)
    except shutil.Error:
        logging.error((
            "Error moving file %s : you are trying to extract the same search", full_file_name))
        logging.warning(("Excluding images from %s ", src_dir_images))
        for filename in os.listdir(src_dir_images):
            file_path = os.path.join(src_dir_images, filename)
            if os.path.isfile(file_path):
                try:
                    os.remove(file_path)
                except ImportError as exception:
                    logging.error(("Error removing news images %s ", exception))
    except ImportError as exception:
        logging.error(("Unexpected error: %s ", exception))


def zip_folder(source_folder, target_folder):
    """
    Zips the contents of the source folder into a zip file in the target folder.

    Args:
        source_folder (str): The folder whose contents will be zipped.
        target_folder (str): The folder where the zip file will be saved.

    Returns:
        None
    """
    output_zip = os.path.join(target_folder, "news_images.zip")

    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(source_folder):
            for file in files:
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, source_folder)
                zipf.write(full_path, relative_path)
