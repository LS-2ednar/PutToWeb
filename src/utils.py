import re
from htmlnode import *
from textnode import *
from enum import Enum

class BlockType(Enum):
    paragraph = "paragrah"
    heading = "heading"
    code = "code"
    quote = "quote"
    unordered_list = "unordered_list"
    ordered_list = "ordered_list"

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
    textnodes = split_nodes_link(images)

    return textnodes

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
        if len(block) == 0:
            continue
        blocks.append(block.strip())
    return blocks

def block_to_block_type(block):
    if len(block) == 0:
        return
    if block[0:3] == "```" and block[-3::] == "```":
        return BlockType.code
    elif block[0] == ">":
        return BlockType.quote
    elif block[0] == "-":
        return BlockType.unordered_list
    elif block[1] == "." and block[0].isdigit():
        return BlockType.ordered_list
    elif "#" in block[0:7]:
        return BlockType.heading
    else:
        return BlockType.paragraph

def textnode_to_html(textnode):
    if textnode.text_type == TextType.TEXT:
        return f"<p>{textnode.text}</p>"
    elif textnode.text_type == TextType.BOLD:
        return f"<b>{textnode.text}</b>"
    elif textnode.text_type == TextType.ITALIC:
        return f"<i>{textnode.text}</i>"
    elif textnode.text_type == TextType.CODE:
        return f"<code>{textnode.text}</code>"
    elif textnode.text_type == TextType.LINK:
        return f'<a href="{textnode.url}">{textnode.text}</a>'
    elif textnode.text_type == TextType.IMAGE:
        return f'<img src="{textnode.url}" alt="{textnode.text}">'


def create_html_from_block(block,block_type):

    if block_type == BlockType.paragraph:
        return f"<div>{1}</div>"
    elif block_type == BlockType.heading:
        return f"<div>{2}</div>"
    elif block_type == BlockType.code:
        return f"<div>{3}</div>"
    elif block_type == BlockType.quote:
        return f"<div>{4}</div>"
    elif block_type == BlockType.unordered_list:
        return f"<div>{5}</div>"
    elif block_type == BlockType.ordered_list:
        return f"<div>{6}</div>"
    else:
        raise TypeError(f"No BlockType: {block_type} define ")
    

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    new_html = ""
    for block in blocks:
        block_type = block_to_block_type(block)
        
        """
        Will mostliekly need to rework some of the markdown_to_blocks function specially the part about ordered and unordered lists!
        """
        
    return 
