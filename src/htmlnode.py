

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
        raise NotImplementedError("NOT IMPLEMENTED YET!")
    
    def props_to_html(self):
        return_string = ""
        for key in self.props:
            return_string.append(f' {key}="{self.props[key]}"')
        return return_string