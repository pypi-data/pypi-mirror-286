#Project Path

project_path is a Python library designed to help you easily locate the path of your project by searching for specific files in the current directory and its parent directories.

##Installation
pip install prjpath.

##Usage
get_project_path(add_to_PATH=True)
This function returns the path of the project by checking for the existence of 'main.py' and 'README.md' simultaneously, or the existence of the '.prjroot' file in the current directory or its parent directories. If found, it returns that path; otherwise, it moves one directory up until it reaches the root. If the root is reached, it returns the path where the script using the library is located.


**add_to_PATH** (bool, optional): If True, adds the project path to sys.path. Defaults to False.
###Parameters
####Returns
str: The path of the project.


**path_to_be_appended** (str, optional): 
###Parameters
The path to be appended to sys.path. Defaults to the project path obtained from get_project_path().
####Returns 
bool :True if it was added correctly, False otherwise


## Contributing  

Contributions are always welcome! 