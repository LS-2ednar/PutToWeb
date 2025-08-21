import os, shutil

def copy_to_target_directory(source="static",target="public"):
    cwd = os.getcwd()
    source_folder = os.path.join(cwd,source)
    target_folder = os.path.join(cwd,target)

    if not os.path.exists(source_folder):
        raise Exception(f"source directory: {source_folder} does not exist!")

    if not os.path.exists(target_folder):
        os.mkdir(target_folder)
    else:
        print(f"\n\nRemoveing {target_folder} and data:")
        try:
            shutil.rmtree(target_folder)
        except:
            print("None")

    """2. Copy all files and subdirectories from static to public & log files as we go"""
    """This part below this line needs work """

    if not os.path.exists(target_folder):
        print(f"\n\nRecreateing: {target_folder}\n\n")
        os.mkdir(target_folder)

    elements_in_source = os.listdir(source_folder)

    for element in elements_in_source:
        element_path = os.path.join(source_folder,element)
        if os.path.isfile(element_path):
            print(f"File: {element}")
        else:
            print(f"Directory: {element}")

    print("\n\n")

"""- remove after testing-"""

if __name__ == "__main__":
    copy_to_target_directory()