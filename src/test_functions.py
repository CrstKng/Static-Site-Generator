import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from functions import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
from functions import markdown_to_blocks, BlockType, block_to_block_type, markdown_to_html_node

class TestTextNode(unittest.TestCase):
    def test_split_delimiter(self):
        node_list = [TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)]
        self.assertEqual(split_nodes_delimiter(node_list, "**", TextType.BOLD), [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded phrase", TextType.BOLD),
            TextNode(" in the middle", TextType.TEXT),
        ])

    def test_split_delimiter2(self):
        node_list = [TextNode("This is text with one **bolded phrase** in the middle and second **one** in the end", TextType.TEXT)]
        self.assertEqual(split_nodes_delimiter(node_list, "**", TextType.BOLD), [
            TextNode("This is text with one ", TextType.TEXT),
            TextNode("bolded phrase", TextType.BOLD),
            TextNode(" in the middle and second ", TextType.TEXT),
            TextNode("one", TextType.BOLD),
            TextNode(" in the end", TextType.TEXT),
        ])

    def test_split_delimiter3(self):
        node_list = [TextNode("This is text with a _italic phrase_ in the middle", TextType.TEXT)]
        self.assertEqual(split_nodes_delimiter(node_list, "_", TextType.ITALIC), [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("italic phrase", TextType.ITALIC),
            TextNode(" in the middle", TextType.TEXT),
        ])

    def test_split_delimiter4(self):
        node_list = [TextNode("This is text with one _italic phrase_ in the middle and second _one_ in the end", TextType.TEXT)]
        self.assertEqual(split_nodes_delimiter(node_list, "_", TextType.ITALIC), [
            TextNode("This is text with one ", TextType.TEXT),
            TextNode("italic phrase", TextType.ITALIC),
            TextNode(" in the middle and second ", TextType.TEXT),
            TextNode("one", TextType.ITALIC),
            TextNode(" in the end", TextType.TEXT),
        ])

    def test_split_delimiter5(self):
        node_list = [TextNode("This is text with a `code phrase` in the middle", TextType.TEXT)]
        self.assertEqual(split_nodes_delimiter(node_list, "`", TextType.CODE), [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code phrase", TextType.CODE),
            TextNode(" in the middle", TextType.TEXT),
        ])

    def test_split_delimiter6(self):
        node_list = [TextNode("This is text with one `code phrase` in the middle and second `one` in the end", TextType.TEXT)]
        self.assertEqual(split_nodes_delimiter(node_list, "`", TextType.CODE), [
            TextNode("This is text with one ", TextType.TEXT),
            TextNode("code phrase", TextType.CODE),
            TextNode(" in the middle and second ", TextType.TEXT),
            TextNode("one", TextType.CODE),
            TextNode(" in the end", TextType.TEXT),
        ])

# Tests for extracting images and links from md file

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images2(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to my blog](https://www.rumen.soontobeblog)"
        )
        self.assertListEqual([("to my blog", "https://www.rumen.soontobeblog")], matches)

    def test_extract_markdown_links2(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

# Tests for spliting the image and link md into TextNodes

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

#Tests for raw md text to textnodes conversion

    def test_text_to_textnodes(self):
        raw_text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(raw_text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )


#Tests for md to blocks


    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type(self):
        blocks = [
            "This is **bolded** paragraph",
            "# This is a heading with _italic_ text and `code` here",
            "- This is an unordered list\n- with items",
            "1. This is an ordered list\n2. with items",
            "```\ncode\n```",
            ">quote line 1\n> line 2\n>quote line 3",
            ]
        block_types = []
        for block in blocks:
            block_types.append(block_to_block_type(block))
        self.assertEqual(
            block_types,
            [
                BlockType.PARAGRAPH,
                BlockType.HEADING,
                BlockType.UNORDERED_LIST,
                BlockType.ORDERED_LIST,
                BlockType.CODE,
                BlockType.QUOTE,
            ],
        )

    def test_block_to_block_type2(self):
        blocks = [
            "This is **bolded** paragraph",
            "## This is a heading with _italic_ text and `code` here",
            "- This is an unordered list\n- with items",
            "1. This is an ordered list\n2. with items",
            "```\ncode\n```",
            "```\nmore\ncode\n```",
            "```\neven\nmore\ncode\n```",
            "```\nthe\nmost\namount\nof\ncode\never\n```",
            ">quote line 1\n> line 2\n>quote line 3",
            ]
        block_types = []
        for block in blocks:
            block_types.append(block_to_block_type(block))
        self.assertEqual(
            block_types,
            [
                BlockType.PARAGRAPH,
                BlockType.HEADING,
                BlockType.UNORDERED_LIST,
                BlockType.ORDERED_LIST,
                BlockType.CODE,
                BlockType.CODE,
                BlockType.CODE,
                BlockType.CODE,
                BlockType.QUOTE,
            ],
        )

    def test_unordered_list(self):
        md = """
    - first item
    - second item
    - third item
    """
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>first item</li><li>second item</li><li>third item</li></ul></div>",
        )

    def test_unordered_list2(self):
        md = """
    - first item
    - **second** item
    - third _item_

    - fourth item
    - fifth item is `code`
    """
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>first item</li><li><b>second</b> item</li><li>third <i>item</i></li></ul><ul><li>fourth item</li><li>fifth item is <code>code</code></li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
    1. first item
    2. second item
    3. third item
    """
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>first item</li><li>second item</li><li>third item</li></ol></div>",
        )

    def test_ordered_list2(self):
        md = """
    1. first item
    2. **second** item
    3. third _item_

    1. fourth item
    2. fifth item is `code`
    """
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>first item</li><li><b>second</b> item</li><li>third <i>item</i></li></ol><ol><li>fourth item</li><li>fifth item is <code>code</code></li></ol></div>",
        )


    def test_heading(self):
        md = """
    # Heading first size
    """
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading first size</h1></div>",
        )
    def test_heading2(self):
        md = """
    ### Heading third size
    """
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h3>Heading third size</h3></div>",
        )

    def test_heading3(self):
        md = """
    #### Heading **fourth** _size_ with `code`
    """
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h4>Heading <b>fourth</b> <i>size</i> with <code>code</code></h4></div>",
        )

    def test_quote(self):
        md = """
    >quote line 1
    > line 2
    >quote line 3
    """
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>quote line 1\nline 2\nquote line 3\n</blockquote></div>",
        )

    def test_quote2(self):
        md = """
    >quote _line_ 1
    > line 2 with `code`
    >quote line 3

    > another **quote** with
    > `code`
    """
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>quote <i>line</i> 1\nline 2 with <code>code</code>\nquote line 3\n</blockquote><blockquote>another <b>quote</b> with\n<code>code</code>\n</blockquote></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

#Tests for markdown to html function

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

#needs of a lot more tests of course