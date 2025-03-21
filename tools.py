import os
import shutil

# Function to empty a specified folder.
def empty_folder(directory_name):
    print(f"[INFO] Cleaning up directory: '{directory_name}'")
    if not os.path.isdir(directory_name):
        print(f"[DEBUG] Directory '{directory_name}' does not exist. Creating it.")
        os.makedirs(directory_name)
    else:
        folder = directory_name
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    print(f"[DEBUG] Deleting file: '{file_path}'")
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    print(f"[DEBUG] Deleting directory: '{file_path}'")
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"[ERROR] Error while deleting '{file_path}': {e}")

# Function to list all files in a specified directory.
def list_dir(path):
    print(f"[INFO] Listing contents of directory: '{path}'")
    try:
        directory_content = os.listdir(path)
        print(f"[DEBUG] Directory '{path}' contains: {directory_content}")
        return directory_content
    except FileNotFoundError as e:
        print(f"[ERROR] Directory '{path}' not found: {e}")
        return []
