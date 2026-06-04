from textnode import TextNode, TextType
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
