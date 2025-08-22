import os, shutil

def copy_to_target_directory(source="static",target="public", rm = True):
    cwd = os.getcwd()
    source_dir = os.path.join(cwd,source)
    target_dir = os.path.join(cwd,target)

    if not os.path.exists(source_dir):
        raise Exception(f"source directory: {source_dir} does not exist!")

    if not os.path.exists(target_dir):
        os.mkdir(target_dir)
    else:
        if rm:
            print("="*100)
            message = f"START REMOVAL PROCESS OF {target.upper()}"
            print(f"{message:^100}")
            print("="*100)
            print(f"\n\nRemoveing {target_dir} and its data:\n\n")
            try:
                shutil.rmtree(target_dir)
            except:
                print("None")
            print("="*100)
            print("\n")


    if not os.path.exists(target_dir):
        print("="*100)
        print(f"\n\nRecreateing: {target_dir}\n\n")
        os.mkdir(target_dir)
        print("="*100)
        print("="*100)
        print("="*36,"START THE COPYING PROCESS","="*37)
        print("="*100)



    for element in os.listdir(source_dir):
        source_file_path = os.path.join(source_dir,element)
        target_file_path = os.path.join(target_dir,element)
        if os.path.isfile(os.path.join(source_dir,element)):
            print(f"\nCopying File: {element} \nFrom /{source} to /{target}\n")
            shutil.copy(source_file_path,target_file_path)
        else:
            print("="*100)
            print(f"Next Directory to Copy: {element}")
            os.mkdir(target_file_path)
            print("="*100)
            copy_to_target_directory(source_file_path,target=target,rm=None)
    print("="*100)
    print("="*46," DONE ","="*46)
    print("="*100)