import re
from htmlnode import *
from textnode import *
from enum import Enum

class BlockType(Enum):
    paragraph = "paragraph"
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
    node = TextNode(text.replace("\n",""),TextType.TEXT)
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
    raw_blocks = re.split(r"\n\s*\n", markdown.strip())
    blocks = [block.strip() for block in raw_blocks if block.strip()]
    return blocks

def block_to_block_type(block):
    if not block or block.strip() == "":
        return BlockType.paragraph
    if block.startswith("```") and block.endswith("```"):
        return BlockType.code
    if block.lstrip().startswith(">"):
        return BlockType.quote
    lines = block.splitlines()
    if all(line.lstrip().startswith(("-", "*")) for line in lines if line.strip() != ""):
        return BlockType.unordered_list
    if all(re.match(r"^\d+\.", line.lstrip()) for line in lines if line.strip() != ""):
        return BlockType.ordered_list
    if re.match(r"^#{1,6}\s", block):
        return BlockType.heading
    return BlockType.paragraph

def split_list(text):
    if len(text.split("-")) > 1:
        return text.split("-")
    else:
        return text.split("\n")


def create_htmlnode_from_block(block: str, block_type: BlockType) -> HTMLNode:
    if block_type == BlockType.paragraph:
        normalized = " ".join(block.splitlines()).strip()
        inlines = [text_node_to_html_node(n) for n in text_to_textnodes(normalized)]
        return HTMLNode("p", None, inlines)

    elif block_type == BlockType.heading:
        # Match leading 1–6 hashes, then a space, then the title
        m = re.match(r"^(#{1,6})\s+(.*)$", block.strip())
        if not m:
            # Fallback: treat as paragraph if malformed heading
            inlines = [text_node_to_html_node(n) for n in text_to_textnodes(block)]
            return HTMLNode("p", None, inlines)
        level = min(len(m.group(1)), 6)
        title = m.group(2).strip()
        return HTMLNode(f"h{level}", title)

    elif block_type == BlockType.code:
        # Strip triple backticks and optional language id on the first line
        raw = block.strip()
        if raw.startswith("```"):
            raw = raw[3:]
            # Optional language token until first newline
            if "\n" in raw:
                first_nl = raw.find("\n")
                # ignore language token raw[:first_nl]
                raw = raw[first_nl + 1 :]
        if raw.endswith("```"):
            raw = raw[:-3]
        # Do not parse inline formatting inside code blocks
        return HTMLNode("pre", None, [HTMLNode("code", raw)])

    elif block_type == BlockType.quote:
        stripped_lines = []
        for line in block.splitlines():
            line = line.lstrip()
            if line.startswith(">"):
                line = line[1:]
                if line.startswith(" "):
                    line = line[1:]
            stripped_lines.append(line)
        quote_text = " ".join(stripped_lines).strip()
        inlines = [text_node_to_html_node(n) for n in text_to_textnodes(quote_text)]
        return HTMLNode("blockquote", None, inlines)

    elif block_type == BlockType.unordered_list:
        items = []
        for line in block.splitlines():
            line = line.rstrip()
            if not line.strip():
                continue
            m = re.match(r"^\s*[-*]\s+(.*)$", line)
            if not m:
                continue
            item_text = m.group(1).strip()
            inlines = [text_node_to_html_node(n) for n in text_to_textnodes(item_text)]
            items.append(HTMLNode("li", None, inlines))
        return HTMLNode("ul", None, items)

    elif block_type == BlockType.ordered_list:
        items = []
        for line in block.splitlines():
            line = line.rstrip()
            if not line.strip():
                continue
            m = re.match(r"^\s*\d+\.\s+(.*)$", line)
            if not m:
                continue
            item_text = m.group(1).strip()
            inlines = [text_node_to_html_node(n) for n in text_to_textnodes(item_text)]
            items.append(HTMLNode("li", None, inlines))
        return HTMLNode("ol", None, items)

    else:
        raise TypeError(f"Unsupported BlockType: {block_type}")

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        html_children.append(create_htmlnode_from_block(block,block_type))
        
    return HTMLNode("div",None,html_children,None)