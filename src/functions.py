from textnode import TextNode, TextType, text_node_to_html_node
import re
from enum import Enum
from htmlnode import HTMLNode, ParentNode, LeafNode

#for now does not allow for nested inline elements
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.extend([old_node])
        else:
            splitted_old_node = old_node.text.split(delimiter)
 #           if len(splitted_old_node) % 2 == 0:            #I don't know if I am allowed to do that
 #               raise Exception("incorrect markdown syntax")
            for i in range (0, len(splitted_old_node)):
                if i % 2 == 0:
                    new_nodes.append(TextNode(text = splitted_old_node[i], text_type = TextType.TEXT))
                if delimiter == "**" and i % 2 == 1:
                    new_nodes.append(TextNode(text = splitted_old_node[i], text_type = TextType.BOLD))
                if delimiter == "_" and i % 2 == 1:
                    new_nodes.append(TextNode(text = splitted_old_node[i], text_type = TextType.ITALIC))
                if delimiter == "`" and i % 2 == 1:
                    new_nodes.append(TextNode(text = splitted_old_node[i], text_type = TextType.CODE))
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
                for i in range (0, len(splitted_old_node)):
                    if i % 3 == 0:
                        new_nodes.append(TextNode(text = splitted_old_node[i], text_type = TextType.TEXT))
                    if i % 3 == 1:
                        new_nodes.append(TextNode(text = splitted_old_node[i], text_type = TextType.IMAGE, url = splitted_old_node[i+1]))
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
                for i in range (0, len(splitted_old_node)):
                    if i % 3 == 0:
                        new_nodes.append(TextNode(text = splitted_old_node[i], text_type = TextType.TEXT))
                    if i % 3 == 1:
                        new_nodes.append(TextNode(text = splitted_old_node[i], text_type = TextType.LINK, url = splitted_old_node[i+1]))
    return new_nodes

def text_to_textnodes(text):
    old_node = [TextNode(text = text, text_type = TextType.TEXT)]
    final_nodes = split_nodes_link(split_nodes_image(split_nodes_delimiter(split_nodes_delimiter(split_nodes_delimiter(old_node, "**", TextType.BOLD), "_", TextType.ITALIC), "`", TextType.CODE)))
    return final_nodes


#Md doc to blocks md

def markdown_to_blocks(markdown):
    split_md = markdown.split("\n\n")
    blocks_md = []
    for block in split_md:
        blocks_md.append(block.strip())
    return blocks_md


class BlockType(Enum):
    PARAGRAPH = "",
    HEADING = "#",
    CODE = "```"
    QUOTE = ">"
    UNORDERED_LIST = "-"
    ORDERED_LIST = "."

def block_to_block_type(block_md):
    if re.match(r"^#{1,6}\s", block_md):    
        return BlockType.HEADING
    if re.match(r"^```[\s\S]*```$", block_md):
        return BlockType.CODE
    if re.match(r"^>", block_md) and len(re.findall(r"\n", block_md)) + 1 == len (re.findall(r">", block_md)): #need to fix
        return BlockType.QUOTE
    if re.match(r"^[*-] ", block_md):
        return BlockType.UNORDERED_LIST
    if re.match(r"^1\.\s", block_md): #make it, so the digit must go from 1 onward !!!
        i = 2
        matches = []
        while True:
            matches.append(re.findall(fr"^\n{i}\.\s", block_md))
            i += 1
            if len(matches[i-3]) != 2 or len(matches) != i-2:
                break
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def text_to_children(text):             #used for all block types except BlockType.CODE
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)
    return html_nodes

def markdown_to_html_node(markdown):
    blocks_md = markdown_to_blocks(markdown)
    html_nodes = []
    for block_md in blocks_md:
        block_type = block_to_block_type(block_md)
        if block_type == BlockType.HEADING:
            hashtag_string = re.findall(r'^(#+)', block_md)
            number_heading = len(hashtag_string[0])
            heading_text = re.findall(r'#+\s(.+)', block_md)
            html_node = ParentNode(tag=f"h{number_heading}", children=text_to_children(heading_text[0]))

        if block_type == BlockType.CODE:
            code_text_with_white_spaces = re.findall(r'```\n([\s\S]+)```', block_md)
            code_text_lines = re.findall(r'([^\n]+)', code_text_with_white_spaces[0])
            code_text = ""
            for code_text_line in code_text_lines:
                if not code_text_line.lstrip() == "":
                    code_text += code_text_line.lstrip() + "\n"
            text_node = TextNode(code_text, TextType.CODE_BLOCK)
            html_node = text_node_to_html_node(text_node)

        if block_type == BlockType.QUOTE:
            quote_strings = re.findall(r'>([^\n]+)', block_md)
            full_quote_string = ""
            for quote_string in quote_strings:
                full_quote_string += quote_string.lstrip() + "\n"
            html_node = ParentNode(tag="blockquote", children=text_to_children(full_quote_string))

        if block_type == BlockType.UNORDERED_LIST:  
            listed_items = re.findall(r"-\s([^\n]+)", block_md)
            list_children = []
            for listed_item in listed_items:
                list_children.append(ParentNode(tag = "li", children=text_to_children(listed_item)))
            html_node = ParentNode(tag="ul", children=list_children)


        if block_type == BlockType.ORDERED_LIST:
            listed_items = re.findall(r"\d{1}\.\s([^\n]+)", block_md)
            list_children = []
            for listed_item in listed_items:
                list_children.append(ParentNode(tag = "li", children = text_to_children(listed_item)))
            html_node = ParentNode(tag="ol", children=list_children)

        if block_type == BlockType.PARAGRAPH:
            first_paragraph = re.findall(r'([^\n]+)', block_md)
            p_text = ""
            for i in range (len(first_paragraph)):
                if not first_paragraph[i].lstrip() == "":
                    if first_paragraph[i] == first_paragraph[-1]:
                        p_text += first_paragraph[i].lstrip()
                    else:
                        p_text += first_paragraph[i].lstrip() + " "
            if not p_text == "":
                html_node = ParentNode(tag="p", children=text_to_children(p_text))
            else:
                html_node = LeafNode(tag=None, value=None)
        if html_node != LeafNode(tag=None, value=None):
            html_nodes.append(html_node)

    parent_html = ParentNode(tag="div", children=html_nodes)
    return parent_html
