import os
import hashlib
import sys

def hash_file(file_path):
    """Generate a hash for the file content."""
    hasher = hashlib.md5()
    with open(file_path, 'rb') as file:
        buf = file.read()
        hasher.update(buf)
    return hasher.hexdigest()

def find_duplicate_files(directory):
    """Find duplicate files in the specified directory."""
    hash_to_files = {}
    duplicate_files = []

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = hash_file(file_path)
            if file_hash in hash_to_files:
                hash_to_files[file_hash].append(file_path)
            else:
                hash_to_files[file_hash] = [file_path]

    for files_list in hash_to_files.values():
        if len(files_list) > 1:
            duplicate_files.extend(files_list[1:])

    return duplicate_files

def delete_duplicate_files(duplicate_files):
    """Delete the duplicate files."""
    for file_path in duplicate_files:
        try:
            os.remove(file_path)
            print(f"Deleted duplicate file: {file_path}")
        except OSError as e:
            print(f"Error deleting file: {file_path}. {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python duplicate_file_remover.py <directory>")
        sys.exit(1)

    target_directory = sys.argv[1]

    if not os.path.isdir(target_directory):
        print("Invalid directory path.")
        sys.exit(1)

    duplicate_files = find_duplicate_files(target_directory)

    if duplicate_files:
        delete_duplicate_files(duplicate_files)
    else:
        print("No duplicate files found.")