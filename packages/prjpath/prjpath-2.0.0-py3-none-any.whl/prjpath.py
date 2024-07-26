import os
import sys
import inspect
import time


def get_project_path(add_to_PATH=False):
    """
    This function returns the path of the project by checking for the existence
    of 'main.py' and 'README.md' simultaneously, or the existence of the '.prjroot' file
    in the current directory or its parent directories. If found, it returns that path;
    otherwise, it moves one directory up until it reaches the root. If the root is reached,
    it returns the path where the script using the library is located.


    :param add_to_PATH: If True, adds the project path to sys.path.
    :return: str: The path of the project.
    """
    # Determine the caller file correctly regardless of whether it's a .py or a compiled .exe
    if getattr(sys, 'frozen', False):  # Check if the script is compiled
        caller_file = sys.executable
    else:
        caller_file = inspect.stack()[1].filename


    current_directory = os.path.dirname(os.path.abspath(caller_file))


    while True:
        # Check if both main.py and README.md exist in the current directory
        files_in_directory = {file.lower() for file in os.listdir(current_directory)}
        if ({"main.py", "readme.md"}.issubset(files_in_directory)) or (".prjroot" in files_in_directory):
            if add_to_PATH:
                sys.path.append(current_directory)
            return current_directory


        # Move one directory up
        new_directory = os.path.dirname(current_directory)


        # If the new directory is the same as the current directory, we have reached the root
        if new_directory == current_directory:
            if add_to_PATH:
                sys.path.append(os.path.dirname(caller_file))
            return os.path.dirname(caller_file)


        current_directory = new_directory



def add_project_path_to_PATH(path_to_be_appended=get_project_path()):
    """
    This function adds the project path to the sys.path list. It is useful for
    including the project directory in the Python path, allowing easy import of
    modules from the project.


    Args:
        path_to_be_appended (str, optional): The path to be appended to sys.path.
            Defaults to the project path obtained from get_project_path().
    """
    try:
        sys.path.append(path_to_be_appended)
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        raise ValueError(f"prjpath library: The directory: {path_to_be_appended}\n could not be appended to PATH.")

