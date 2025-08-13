import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_as_expected_1(self):
        self.assertIsInstance(HTMLNode("<a>","Magic"),HTMLNode)
    
    def test_as_expected_2(self):
        self.assertIsInstance(HTMLNode("<a>",VALUE=None,CHILDREN=[HTMLNode("a","Spell")]),HTMLNode)

    def test_as_expected_3(self):
        self.assertIsInstance(HTMLNode("<a>","Magic",CHILDREN=None),HTMLNode)

    def test_as_expected_4(self):
        self.assertIsInstance(HTMLNode("<a>","Magic",[HTMLNode("a","Spell")],{"a":"Alakazam!"}),HTMLNode)
            
    def test_TAG_wrong_type(self):
        with self.assertRaises(TypeError):
            HTMLNode(123)

    def test_VALUE_wrong_type(self):
        with self.assertRaises(TypeError):
            HTMLNode("a",123)
    
    def test_CHILDREN_wrong_type(self):
        with self.assertRaises(TypeError):
            HTMLNode("a","magic",123)

    def test_CHILDREN_ELEMENT_wrong_type(self):
        with self.assertRaises(TypeError):
            HTMLNode("a","magic",[123])

    def test_PROPS_wrong_type(self):
        with self.assertRaises(TypeError):
            HTMLNode("a","magic",[HTMLNode("a","b")],123)

    def test_VALUE_and_CHILDREN_equal_None(self):
        with self.assertRaises(ValueError):
            HTMLNode("a",VALUE=None,CHILDREN=None)
