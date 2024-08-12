import os
import shutil
import logging
def create_new_dir_to_save_excel_and_images(dir, from_date, to_date, phrase):
    logging.info("Creating new dir to save excel and images from search...")
    try:
        new_dir_name = f"news_data-searched_{phrase}_{from_date}_to_{to_date}"

        new_dir_path = os.path.join(dir, new_dir_name)

        os.makedirs(new_dir_path, exist_ok=True)

    except ImportError as e:
        logging.error(f"Error creating new dir: {e}")
        raise

    logging.info("New dir Created")
    return new_dir_path


def move_images_to_repository(new_dir, src_dir_images):
        logging.info("Moving news pictures to new dir")
        try:
            for file_name in os.listdir(src_dir_images):
                full_file_name = os.path.join(src_dir_images, file_name)
                shutil.move(full_file_name, new_dir)
        except shutil.Error as e:
            logging.error(f"Error moving file {full_file_name}: you are trying to extract the same search")
            logging.warning(f"Excluding images from {src_dir_images}")
            for filename in os.listdir(src_dir_images):
                file_path = os.path.join(src_dir_images, filename)
                if os.path.isfile(file_path):
                    try:
                        os.remove(file_path)
                    except Exception as e:
                        logging.error(f"Error removing news images {e}")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")