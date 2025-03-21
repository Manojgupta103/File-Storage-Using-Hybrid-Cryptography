import tools

# Function to divide large files into smaller chapters.
def divide():
    print("[INFO] Starting file division process.")
    tools.empty_folder('files')
    tools.empty_folder('raw_data')

    # Read the uploaded file's name.
    FILE = tools.list_dir('uploads')
    FILE = './uploads/' + FILE[0]
    print(f"[DEBUG] File to be divided: {FILE}")

    # Define size constants.
    MAX = 1024 * 32  # 32 KB - max chapter size
    BUF = 50 * 1024 * 1024 * 1024  # 50 GB - memory buffer size

    chapters = 0
    uglybuf = b""
    meta_data = open('raw_data/meta_data.txt', 'w')
    file__name = FILE.split('/')[-1]
    print(f"[INFO] Writing metadata for file: {file__name}")
    meta_data.write(f"File_Name={file__name}\n")

    # Read and divide the file into chapters.
    with open(FILE, 'rb') as src:
        while True:
            print(f"[INFO] Creating chapter {chapters + 1}.")
            target_file = open(f'files/SECRET{chapters:07d}', 'wb')
            written = 0

            # Write data to the chapter file until the MAX size is reached.
            while written < MAX:
                if len(uglybuf) > 0:
                    target_file.write(uglybuf)
                read_data = src.read(min(BUF, MAX - written))
                target_file.write(read_data)
                written += len(read_data)
                uglybuf = src.read(1)
                if len(uglybuf) == 0:
                    break
            target_file.close()

            if len(uglybuf) == 0:
                print("[INFO] End of file reached.")
                break

            chapters += 1

    # Store metadata about the number of chapters.
    meta_data.write(f"chapters={chapters + 1}")
    meta_data.close()
    print(f"[INFO] File division completed with {chapters + 1} chapters.")
