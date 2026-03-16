from textnode import TextNode, TextType, text_node_to_html_node
import re

#for now does not allow for nested inline elements
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.extend([old_node])
        else:
            splitted_old_node = old_node.text.split(delimiter)
            if len(splitted_old_node) % 2 == 0:
                raise Exception("incorrect markdown syntax")
            for i in range (0, len(splitted_old_node)):
                if i % 2 == 0:
                    new_nodes.append(TextNode(text = splitted_old_node[i], text_type = TextType.TEXT))
                if delimiter == "**" and i % 2 == 1:
                    new_nodes.append(TextNode(text = splitted_old_node[i], text_type = TextType.BOLD))
                if delimiter == "_" and i % 2 == 1:
                    new_nodes.append(TextNode(text = splitted_old_node[i], text_type = TextType.ITALIC))
                if delimiter == "`" and i % 2 == 1:
                    new_nodes.append(TextNode(text = splitted_old_node[i], text_type = TextType.CODE))
#    print(new_nodes)
    return new_nodes

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern,text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT: #dont know if I need this test
            new_nodes.extend([old_node])
        else:
            if extract_markdown_links(old_node.text) is None:
                new_nodes.extend([old_node])
            else:
                splitted_old_node = [x for x in re.split(pattern, old_node.text) if x != ""]
 #               print(splitted_old_node)
 #               matches = extract_markdown_links(old_node.text)
                for i in range (0, len(splitted_old_node)):
                    if i % 3 == 0:
                        new_nodes.append(TextNode(text = splitted_old_node[i], text_type = TextType.TEXT))
                    if i % 3 == 1:
                        new_nodes.append(TextNode(text = splitted_old_node[i], text_type = TextType.IMAGE, url = splitted_old_node[i+1]))
 #   print(new_nodes)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT: #dont know if I need this test
            new_nodes.extend([old_node])
        else:
            if extract_markdown_links(old_node.text) is None:
                new_nodes.extend([old_node])
            else:
                splitted_old_node = [x for x in re.split(pattern, old_node.text) if x != ""]
 #               print(splitted_old_node)
 #               matches = extract_markdown_links(old_node.text)
                for i in range (0, len(splitted_old_node)):
                    if i % 3 == 0:
                        new_nodes.append(TextNode(text = splitted_old_node[i], text_type = TextType.TEXT))
                    if i % 3 == 1:
                        new_nodes.append(TextNode(text = splitted_old_node[i], text_type = TextType.LINK, url = splitted_old_node[i+1]))
#    print(new_nodes)
    return new_nodes

def text_to_textnodes(text):
    old_node = [TextNode(text = text, text_type = TextType.TEXT)]
    final_nodes = split_nodes_link(split_nodes_image(split_nodes_delimiter(split_nodes_delimiter(split_nodes_delimiter(old_node, "**", TextType.BOLD), "_", TextType.ITALIC), "`", TextType.CODE)))
#    print(final_nodes)
    return final_nodes



def markdown_to_blocks(markdown):
    split_md = markdown.split("\n\n")
    blocks_md = []
    for block in split_md:
        blocks_md.append(block.strip())
#    print(blocks_md)
    return blocks_md
