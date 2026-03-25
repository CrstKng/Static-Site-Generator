class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
#        if not self.tag:
#            if not self.value:
 #               raise Error("Not valid html code")
  #      if not self.value:
  #          if not self.tag and not self.children:
  #              raise Error("Not valid html code")
 #       if not self.children:
 #           if not self.value:
 #               raise Error("Not valid html code")

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        string = ""
        if self.props:
            for key in self.props:
                string += f' {key}="{self.props[key]}"'
        return string
    
    def children_to_html(self):
        string = ""
        i = 1
        if self.children:
            for child in self.children:
                string += f"child{i} tag = {child.tag}, child{i} value = {child.value}, child{i} attributes = {child.props_to_html()}"
        return string

    def __repr__(self):
        return f"tag = {self.tag}, value = {self.value}, children = {self.children_to_html()}, attributes = {self.props_to_html()}"

    def __eq__(self, other):
        return (self.tag == other.tag and self.value == other.value and self.children_to_html() == other.children_to_html() and self.props_to_html() == other.props_to_html())
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, children=None, props=None):
        super().__init__(tag, value, children, props)
        if self.children:
            raise Exception("leaf node does not have children!")

    def to_html(self):
        if not self.value:
            raise ValueError
        if not self.tag:
            return self.value
        else:
            if self.tag == 'code_block':
                return f"<pre><code>{self.value}</code></pre>" #could be done easier perhaps
            if self.props:
                return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
            else:
                return f"<{self.tag}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"tag = {self.tag}, value = {self.value}, attributes = {self.props_to_html()}"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, value=None, props=None):
        super().__init__(tag, value, children, props)
        if self.value:
            raise Exception("parent node does not have value!")

    def to_html(self):
        if not self.tag:
            raise ValueError("parent node must have a tag")
        if not self.children:
            raise ValueError("parent node must have children")
        else:
            string = ""
            for child in self.children:
                string += child.to_html()
            if self.props:
                return f"<{self.tag}{self.props_to_html()}>{string}</{self.tag}>"
            else: 
                return f"<{self.tag}>{string}</{self.tag}>"
        