import tools

# Function to restore original file from the divided chapters.
def restore():
    print("[INFO] Starting file restoration process.")
    tools.empty_folder('restored_file')

    chapters = 0

    # Reading metadata to retrieve file information.
    print("[INFO] Reading metadata from 'raw_data/meta_data.txt'")
    meta_data = open('raw_data/meta_data.txt', 'r')
    meta_info = [row.split('=')[1].strip() for row in meta_data]
    meta_data.close()

    file_name = meta_info[0]
    print(f"[INFO] Restoring file: {file_name}")
    address = 'restored_file/' + file_name

    list_of_files = sorted(tools.list_dir('files'))
    print(f"[DEBUG] Found {len(list_of_files)} chapter files for restoration.")

    # Reassemble the chapters into the original file.
    with open(address, 'wb') as writer:
        for file in list_of_files:
            print(f"[INFO] Restoring chapter '{file}'")
            path = 'files/' + file
            with open(path, 'rb') as reader:
                for line in reader:
                    writer.write(line)
                reader.close()
        writer.close()
    
    tools.empty_folder('files')
    print("[INFO] File restoration completed successfully.")
