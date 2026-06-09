from htmlnode import ParentNode
from textnode import TextNode, TextType, BlockType, text_node_to_html_node
import re


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    if not delimiter:
        raise ValueError("delimiter must be a non-empty string")

    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        segments = node.text.split(delimiter)
        if len(segments) % 2 == 0:
            raise ValueError(f"missing closing delimiter in: {node.text}")

        for index, segment in enumerate(segments):
            if segment == "":
                continue
            if index % 2 == 0:
                new_nodes.append(TextNode(segment, TextType.TEXT))
            else:
                new_nodes.append(TextNode(segment, text_type))

    return new_nodes

def extract_markdown_images(text): 
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue
        remaining = node.text
        for alt, url in images:
            sections = remaining.split(f"![{alt}]({url})",1)
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            remaining = sections[1]
        if remaining:
            new_nodes.append(TextNode(remaining, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue
        remaining = node.text
        for anchor, url in links:
            sections = remaining.split(f"[{anchor}]({url})",1)
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(anchor, TextType.LINK, url))
            remaining = sections[1]
        if remaining:
            new_nodes.append(TextNode(remaining, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def markdown_to_blocks(markdown):
    if not markdown:
        return []

    lines = markdown.splitlines()
    blocks = []
    current_block = []
    in_code_block = False

    for line in lines:
        if line.startswith("```"):
            if in_code_block:
                current_block.append(line)
                blocks.append("\n".join(current_block).strip())
                current_block = []
                in_code_block = False
            else:
                if current_block:
                    blocks.append("\n".join(current_block).strip())
                    current_block = []
                current_block = [line]
                in_code_block = True
            continue

        if in_code_block:
            current_block.append(line)
            continue

        if line.strip() == "":
            if current_block:
                blocks.append("\n".join(current_block).strip())
                current_block = []
            continue

        current_block.append(line)

    if current_block:
        blocks.append("\n".join(current_block).strip())

    return [block for block in blocks if block]


def block_to_block_type(block):
    lines = block.split("\n")
    stripped = block.strip()
    if re.match(r"^#{1,6} ", stripped):
        return BlockType.H
    if stripped.startswith("```"):
        return BlockType.C
    if all(line.startswith(">") for line in lines):
        return BlockType.Q
    if all(re.match(r"^- ", line) for line in lines if line.strip()):
        return BlockType.UL
    if all(re.match(r"^\d+\. ", line) for line in lines if line.strip()):
        return BlockType.OL
    return BlockType.P


def text_to_children(text):
    return [text_node_to_html_node(node) for node in text_to_textnodes(text)]


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    stripped = block.strip()

    if block_type == BlockType.C:
        code_content = stripped.strip("`").strip()
        if code_content.startswith("```"):
            code_content = code_content[3:]
        if code_content.endswith("```"):
            code_content = code_content[:-3]
        code_node = text_node_to_html_node(TextNode(code_content, TextType.CODE))
        return ParentNode("pre", [code_node])

    if block_type == BlockType.H:
        heading_level = len(stripped) - len(stripped.lstrip("#"))
        heading_level = min(max(heading_level, 1), 6)
        heading_text = stripped[heading_level:].strip()
        return ParentNode(f"h{heading_level}", text_to_children(heading_text))

    if block_type == BlockType.UL:
        list_items = []
        for line in stripped.splitlines():
            item_text = line.strip()
            if item_text.startswith(("-", "*", "+")):
                list_items.append(ParentNode("li", text_to_children(item_text[1:].strip())))
        return ParentNode("ul", list_items)

    if block_type == BlockType.OL:
        list_items = []
        for line in stripped.splitlines():
            item_text = line.strip()
            if re.match(r"^\d+\. ", item_text):
                list_items.append(ParentNode("li", text_to_children(re.sub(r"^\d+\. ", "", item_text))))
        return ParentNode("ol", list_items)

    if block_type == BlockType.Q:
        quote_lines = [line[1:].strip() for line in stripped.splitlines() if line.startswith(">")]
        return ParentNode("blockquote", text_to_children("\n".join(quote_lines)))

    return ParentNode("p", text_to_children(stripped))


def markdown_to_html_node(markdown):
    block_nodes = [block_to_html_node(block) for block in markdown_to_blocks(markdown)]
    return ParentNode("div", block_nodes)
