import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(tag = "title", value = "Why Frontend Development Sucks")
        node2 = HTMLNode(tag = "title", value = "Why Frontend Development Sucks")
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = HTMLNode(tag = "a", children = [HTMLNode(tag = "title", value = "Why Frontend Development Sucks")])
        node2 = HTMLNode(tag = "a", children = [HTMLNode(tag = "title", value = "Why Frontend Development Sucks")])
        self.assertEqual(node, node2)

    def test_eq3(self):
        node = HTMLNode(tag = "a", value = "backend", children = [HTMLNode(tag = "title", value = "Why Frontend Development Sucks")], props ={"href":"https://www.boot.dev"})
        node2 = HTMLNode(tag = "a", value = "backend", children = [HTMLNode(tag = "title", value = "Why Frontend Development Sucks")], props ={"href":"https://www.boot.dev"})
        self.assertEqual(node, node2)

    def test_neq(self):
        node = HTMLNode(tag = "title", value = "Why Frontend Development Sucks")
        node2 = HTMLNode(tag = "a", value = "backend", props ={"href":"https://www.boot.dev"})
        self.assertNotEqual(node, node2)

    def test_neq2(self):
        node = HTMLNode(tag = "a", value = "backend", props ={"href":"https://www.boot.dev"})
        node2 = HTMLNode(tag = "a", value = "backend", children = [HTMLNode(tag = "title", value = "Why Frontend Development Sucks")], props ={"href":"https://www.boot.dev"})
        self.assertNotEqual(node, node2)

    def test_neq3(self):
        node = HTMLNode(tag = "title", value = "Why Frontend Development Sucks", children = [HTMLNode(tag = "a", value = "backend", props ={"href":"https://www.boot.dev"})])
        node2 = HTMLNode(tag = "a", value = "backend", children = [HTMLNode(tag = "title", value = "Why Frontend Development Sucks")], props ={"href":"https://www.boot.dev"})
        self.assertNotEqual(node, node2)

    def test_neq4(self):
        node = HTMLNode(tag = "title", value = "Why Frontend Development Sucks", children = [HTMLNode(tag = "a", value = "backend", props ={"href":"https://www.boot.dev"})])
        node2 = HTMLNode(tag = "titla", value = "Why Frontend Development Sucks", children = [HTMLNode(tag = "a", value = "backend")], props = {"href":"https://www.boot.dev"})
        self.assertNotEqual(node, node2)

# Tests for LeafNodes

    def test_leaf_to_html_p(self):
        node = LeafNode(tag = "p", value = "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_p2(self):
        node = LeafNode(tag = None, value = "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_to_html_p3(self):
        node = LeafNode(tag = "head", value = "site", props ={"href":"https://www.boot.dev"})
        self.assertEqual(node.to_html(), '<head href="https://www.boot.dev">site</head>')

# Tests for ParentNodes

    def test_to_html_with_children(self):
        child_node = LeafNode(tag = "span", value = "child")
        parent_node = ParentNode(tag = "div", children = [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode(tag = "b", value = "grandchild")
        child_node = ParentNode(tag = "span", children = [grandchild_node])
        parent_node = ParentNode(tag = "div", children = [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    def test_parent_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode(tag = "b", value = "Bold text"),
                LeafNode(tag = None, value = "Normal text"),
                LeafNode(tag = "i", value = "italic text"),
                LeafNode(tag = None, value = "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

#needs more test here

if __name__ == "__main__":
    unittest.main()