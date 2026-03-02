from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode





def main():
    text_node_dummy = TextNode("Pesho is here", TextType.bold)
    print(text_node_dummy)


main()