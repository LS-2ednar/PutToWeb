import unittest

from htmlnode import ParentNode, LeafNode

class TestParentNode(unittest.TestCase):

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_greatgrandchildren(self):
        greatgradchild_node = LeafNode("a","greatgradchild")
        grandchild_node = ParentNode("b", [greatgradchild_node])
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b><a>greatgradchild</a></b></span></div>",
        )

    def test_to_html_with_greatgrandchildren_with_img(self):
        greatgradchild_node = LeafNode("a","greatgradchild",{"href": "www.google.com"})
        grandchild_node = ParentNode("b", [greatgradchild_node])
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            '<div><span><b><a href="www.google.com">greatgradchild</a></b></span></div>',
        )

    