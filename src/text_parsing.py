from textnode import TextNode, TextType


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