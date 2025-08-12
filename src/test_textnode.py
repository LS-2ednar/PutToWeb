import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        return self.assertEqual(node, node2)

    def test_uneq_different_TextType(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        node2 = TextNode("This is a text node", TextType.BOLD)
        return self.assertNotEqual(node, node2)

    def test_uneq_different_Text(self):
        node = TextNode("This is a text node!!!", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        return self.assertNotEqual(node, node2)

    def test_uneq_URL(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD,"www.google.com")
        return self.assertNotEqual(node, node2)

    def test_wrong_texttype(self):
        with self.assertRaises(Exception):
            TextNode("This is a text node", "banana")

    def test_non_string_text(self):
        with self.assertRaises(TypeError):
            TextNode(1234,TextType.BOLD)

    def test_non_string_URL(self):
        with self.assertRaises(TypeError):
            TextNode("Bananenbrot",TextType.BOLD,1234)
    


if __name__ == "__main__":
    unittest.main()