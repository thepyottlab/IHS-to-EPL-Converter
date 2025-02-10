import tkinter as tk
from tkinter import filedialog
import re
import os

def select_directory():
    """Open a dialog to select a directory and return the selected path."""
    root = tk.Tk()
    root.withdraw()
    return filedialog.askdirectory()

def custom_sort_key(filename):
    """Generate a sort key for each filename based on predefined logic.

    Args:
        filename (str): The filename to generate a sort key for.

    Returns:
        tuple: A tuple containing the primary and secondary sort keys.
    """
    parts = filename.split(' ')
    primary_sort = parts[0]
    secondary_sort_value = 0 if parts[1] == "Clicks-analyzed..txt" else float(
        parts[1].split('.')[0])
    return primary_sort, secondary_sort_value

def get_text_files(directory):
    """List all text files in the given directory.

    Args:
        directory (str): Path to the directory.

    Returns:
        list: A list of filenames (str) that end with '.txt'.
    """
    return [file for file in os.listdir(directory) if file.endswith('.txt')]


def process_file(directory, text_file):
    """Read and process a text file, converting it to a corrected format.

    Args:
        directory (str): The directory containing the file.
        text_file (str): The filename to process.
    """
    file_path = os.path.join(directory, text_file)

    # Read the file content
    with open(file_path, 'r') as file:
        content = file.read()

    # Regular expression to match 'np.float64(<number>)'
    pattern = r"np\.float64\(([\d\.]+)\)"

    # Replace matches with just the number
    modified_content = re.sub(pattern, r"\1", content)

    # Determine the new filename if the extension is '..txt'
    if text_file.endswith('..txt'):
        new_file_name = text_file[:-4] + text_file[-3:]
        new_file_path = os.path.join(directory, new_file_name)

        # Write the modified content to the new file
        with open(new_file_path, 'w') as new_file:
            new_file.write(modified_content)

        # Ensure the original file is closed before deletion
        os.remove(file_path)
    else:
        # Write the modified content back to the same file
        with open(file_path, 'w') as file:
            file.write(modified_content)

    print(
        f"Processed and saved: {new_file_name if text_file.endswith('..txt') else text_file}")


def main():
    """Main function to execute the program workflow."""
    directory = select_directory()
    text_files = sorted(get_text_files(directory), key=custom_sort_key)
    for text_file in text_files:
        process_file(directory, text_file)

if __name__ == "__main__":
    main()

