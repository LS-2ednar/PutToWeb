from textnode import TextNode, TextType

class HTMLNode:
    def __init__(self, TAG=None, VALUE=None, CHILDREN=None, PROPS=None):
        if TAG:
            if not isinstance(TAG,str):
                raise TypeError(f"TAG of type {type(TAG)}! Required Type: String")

        if VALUE:
            if not isinstance(VALUE,str):
                raise TypeError(f"VALUE of type {type(VALUE)}! Required Type: String")
        elif VALUE == None and CHILDREN == None:
            raise ValueError(f"Expected to have CHILDREN if no VALUE provided or vice versa!!!")

        if CHILDREN:
            if not isinstance(CHILDREN,list):
                raise TypeError(f"CHILDREN of type {type(CHILDREN)}! Required Type: LIST")
            elif not isinstance(CHILDREN[0],HTMLNode):
                raise TypeError(f"CHILDREN List Element of type {type(CHILDREN[0])}! Required Type: HTMLNode")

        if PROPS:
            if not isinstance(PROPS,dict):
                raise TypeError(f"PROPS of type {type(PROPS)}! Required Type: Dict")
         
        self.tag = TAG
        self.value = VALUE
        self.children = CHILDREN
        self.props = PROPS

    def __repr__(self):
        return f"TAG: {self.tag}\nVALUE: {self.value}\nChildren: {self.children}\nProps: {self.props_to_html}"

    def to_html(self):
        inner ="".join(child.to_html() for child in self.children)
        return f'<{self.tag}>{inner}</{self.tag}>'.replace("<None>","").replace("</None>","")
    
    def props_to_html(self):
        return_string = ""
        for key in self.props.keys():
            return_string +=f' {key}="{self.props[key]}"'
        return return_string

class LeafNode(HTMLNode):
    def __init__(self, TAG=None, VALUE=None, PROPS=None):
        if VALUE is None:
            raise ValueError("LeafNode must have a VALUE")

        if not isinstance(VALUE, str):
            raise TypeError(f"VALUE of type {type(VALUE)}! Required Type: str")

        super().__init__(TAG=TAG, VALUE=VALUE,CHILDREN=None,PROPS=PROPS)

    def to_html(self):
        if self.props != None:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        elif self.tag == None:
            return f'{self.value}'
        else:
            return f'<{self.tag}>{self.value}</{self.tag}>'

class ParentNode(HTMLNode):
    def __init__(self, TAG=None, CHILDREN=None, PROPS=None):
        if TAG is None:
            raise ValueError("TAG is required")
        if CHILDREN is None:
            raise ValueError("CHILDREN are required")

        super().__init__(TAG=TAG, VALUE=None,CHILDREN=CHILDREN,PROPS=PROPS)

    def to_html(self):
        if self.tag == None:
            raise ValueError("TAG is required")
        if self.children == None:
            raise ValueError("CHILDREN are required")

        inner ="".join(child.to_html() for child in self.children)
        return f'<{self.tag}>{inner}</{self.tag}>'

