from copy_to_target_directory import copy_to_target_directory
from markdown_to_webpage import generate_page, generate_pages_recursively
import sys

def main():
    if len(sys.argv) != 2:
        basepath = "/"
    else:
        basepath = sys.argv[1]

    copy_to_target_directory()
    generate_pages_recursively("content","template.html","docs",basepath)
    
if __name__ == "__main__":
    main()
    