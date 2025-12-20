# Bài 1
filename = 'alice.txt'
try:
    with open(filename) as f_obj:
        contents = f_obj.read()
        print(contents)
except FileNotFoundError:
    print(f"File {filename} không tồn tại.")


# Bài 2
filename = 'alice.txt'
try:
    with open(filename) as f_obj:
        contents = f_obj.read()
except FileNotFoundError:
    msg = "File " + filename + " không tồn tại."
    print(msg)
else:
    words = contents.split()
    num_words = len(words)
    print("File " + filename + " có " + str(num_words) + " từ.")

# Bài 3
def count_words(filename):
    try:
        with open(filename) as f_obj:
            contents = f_obj.read()
    except FileNotFoundError:
        msg = "File " + filename + " không tồn tại."
        print(msg)
    else:
        words = contents.split()
        num_words = len(words)
        print("File " + filename + " có " + str(num_words) + " từ.")

filenames = ['f1.txt', 'f2.txt', 'f3.txt']
for filename in filenames:
    count_words(filename)

# Bài 4
import zipfile

# Compress files into a zip archive
def compress_files(zip_name, file_list):
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        for file in file_list:
            zipf.write(file)
    print(f"Compressed files into {zip_name}")

# Extract files from a zip archive
def extract_files(zip_name, extract_path='.'):
    with zipfile.ZipFile(zip_name, 'r') as zipf:
        zipf.extractall(extract_path)
    print(f"Extracted files from {zip_name} to {extract_path}")

files_to_compress = ['f1.txt', 'f2.txt', 'f3.txt']
zip_filename = 'files.zip'

compress_files(zip_filename, files_to_compress)
extract_files(zip_filename, 'extracted_files')

