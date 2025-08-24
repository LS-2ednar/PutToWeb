from utils import markdown_to_html_node
import os

def extract_title(markdown):
    for line in markdown.splitlines():
        line = line.strip()
        if line.startswith("# "):
            return line.replace("# ","").strip()
    raise Exception("NO TITLE DEFINED")

def generate_page(from_path, template_path, dest_path, basepath):
    from_path = os.path.abspath(from_path)
    template_path = os.path.abspath(template_path)
    dest_path = os.path.abspath(dest_path)

    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as file:
        page_content = file.read()
        file.close()
    with open(template_path) as file:
        template = file.read()
        file.close()

    html_content = markdown_to_html_node(page_content).to_html()
    title = extract_title(page_content)
    full_html = template.replace("{{ Title }}",title).replace("{{ Content }}",html_content)
    """full_html = full_html.replace('href="/',f'href="/{basepath}').replace('src="/',f'src="{basepath}')"""

    with open(dest_path,"w+") as file:
        file.write(full_html)
        file.close()

def generate_pages_recursively(dir_path_content, template_path, dest_dir_path, basepath):
    dir_path_content = os.path.abspath(dir_path_content)
    template_path = os.path.abspath(template_path)
    dest_dir_path = os.path.abspath(dest_dir_path)
    
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for content in os.listdir(dir_path_content):
        content_path = os.path.join(dir_path_content,content)
        dest_path = os.path.join(dest_dir_path,content.replace(".md",".html"))
        new_basepath = os.path.join(basepath,content)

        if content.endswith(".md"):
            print("creating html file for:")
            print(f"{dir_path_content}/{content}")
            generate_page(content_path,template_path,dest_path, new_basepath)
        else:
            if not os.path.isfile(content_path) and not os.path.exists(dest_path):
                os.mkdir(dest_path)
                generate_pages_recursively(content_path, template_path, dest_path, new_basepath)