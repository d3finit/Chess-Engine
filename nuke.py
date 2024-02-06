import os
import threading

def delete_file(file_path):
    try:
        if os.path.exists(file_path) and os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Deleted: {file_path}")
    except Exception as e:
        print(f"Error deleting {file_path}: {str(e)}")

def delete_files_in_folder(folder_path):
    try:
        if not os.path.exists(folder_path):
            print(f"The folder '{folder_path}' does not exist.")
            return

        files = os.listdir(folder_path)

        # Create a thread for each file and delete it concurrently
        threads = []
        for file in files:
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                thread = threading.Thread(target=delete_file, args=(file_path,))
                threads.append(thread)
                thread.start()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

        print(f"All files in '{folder_path}' have been deleted.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    folder_path = input("Enter the folder path: ")
    delete_files_in_folder(folder_path)
