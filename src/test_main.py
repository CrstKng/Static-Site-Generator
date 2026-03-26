import unittest

from main import extract_title

class TestMain(unittest.TestCase):
    def test_extract_files(self):
        md = """
    # This is the title

    ## This is not the title
    
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """
        
        title = extract_title(md)
        self.assertEqual(
            title,
            "This is the title",
        )