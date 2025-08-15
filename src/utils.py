import re
from htmlnode import *
from textnode import *

def text_node_to_html_node(text_node):
    if not isinstance(text_node,TextNode):
        raise ValueError("No TextNode Type provided!")
    
    match text_node.text_type:
        case TextType.TEXT | "text":
            return LeafNode(None, text_node.text)
        case TextType.BOLD | "bold":
            return LeafNode("b", text_node.text)
        case TextType.ITALIC | "italic":
            return LeafNode("i", text_node.text)
        case TextType.CODE | "code":
            return LeafNode("code", text_node.text)
        case TextType.LINK | "link":
            if not text_node.url:
                raise ValueError("LINK nodes require a url")
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE | "image":
            if not text_node.url:
                raise ValueError("IMAGE nodes require a url")
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})

    raise Exception("Undefined Tag used")

def text_to_textnodes(text):
    node = TextNode(text,TextType.TEXT)
    code = split_nodes_delimiter([node],"`",TextType.CODE)
    code_bold = split_nodes_delimiter(code,"**",TextType.BOLD)
    code_bold_itlaic= split_nodes_delimiter(code_bold,"_",TextType.ITALIC)
    images = split_nodes_image(code_bold_itlaic)    
    images_links = split_nodes_link(images)

    return images_links

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    This function will need tweeking later to ensure we can also work with combined formatting -> bold+italic etc.
    """
    new_nodes = []
    for node in old_nodes:
        split_nodes = node.text.split(delimiter)
        index = 0
        for new_node in split_nodes:
            if index == 1:
                new_nodes.append(TextNode(new_node,text_type))
                index = 0
            else:
                new_nodes.append(TextNode(new_node,node.text_type))
                index += 1

    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        images_in_node = extract_markdown_images(node.text)
        if len(images_in_node) == 0:
            new_nodes.append(node)
            continue
        leftover_node_text = node.text
        for image in images_in_node:
            if len(leftover_node_text) == 0:
                break
            sections = leftover_node_text.split(f"![{image[0]}]({image[1]})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0],TextType.TEXT))
            new_nodes.append(TextNode(image[0],TextType.IMAGE,image[1]))
            substring_to_remove = sections[0]+f"![{image[0]}]({image[1]})"
            leftover_node_text = leftover_node_text.replace(substring_to_remove,"")
        if len(leftover_node_text) != 0:
            new_nodes.append(TextNode(leftover_node_text, TextType.TEXT))
    
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        links_in_node = extract_markdown_links(node.text)
        if len(links_in_node) == 0:
            new_nodes.append(node)
            continue
        leftover_node_text = node.text
        for link in links_in_node:
            if len(leftover_node_text) == 0:
                break
            sections = leftover_node_text.split(f"[{link[0]}]({link[1]})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0],TextType.TEXT))
            new_nodes.append(TextNode(link[0],TextType.LINK,link[1]))
            substring_to_remove = sections[0]+f"[{link[0]}]({link[1]})"
            leftover_node_text = leftover_node_text.replace(substring_to_remove,"")
        if len(leftover_node_text) != 0:
            new_nodes.append(TextNode(leftover_node_text, TextType.TEXT))

    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)

def markdown_to_blocks(markdown):
    raw_blocks = markdown.split("\n\n")
    blocks = []
    for block in raw_blocks:
        if len(block) == "":
            continue
        blocks.append(block.strip())
    return blocks