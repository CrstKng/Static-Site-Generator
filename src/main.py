from functions import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node
import os
import shutil
import re
import sys

def copy_dir(source_dir_path, destination_dir_path):
    if not os.path.exists(destination_dir_path):
        raise Exception("the path to the directory chosen to receive the copy is wrong or nonexistant")
    elif not os.path.exists(source_dir_path):
        raise Exception("The path to the initial directory chosen to copy from is wrong or nonexistant")
    else:
        list_source_paths = os.listdir(source_dir_path)
        for path in list_source_paths:
            combined_source_path = os.path.join(source_dir_path, path)
            if os.path.isfile(combined_source_path):
                shutil.copy(combined_source_path, destination_dir_path)
            else:
                combined_destination_dir_path = os.path.join(destination_dir_path, path)
                os.mkdir(combined_destination_dir_path)
                copy_dir(combined_source_path, combined_destination_dir_path)


def move_dir_contents(source_dir_path, destination_dir_path):
    if not os.path.exists(destination_dir_path):
        raise Exception("the path to the directory chosen to receive the copy is wrong or nonexistant")
    elif not os.path.exists(source_dir_path):
        raise Exception("The path to the initial directory chosen to copy from is wrong or nonexistant")
    else:
        shutil.rmtree(destination_dir_path)
        os.mkdir(destination_dir_path)
        copy_dir(source_dir_path, destination_dir_path)


def extract_title(markdown):
    blocks_md = markdown_to_blocks(markdown)
    for block_md in blocks_md:
        block_type = block_to_block_type(block_md)
        if block_type == BlockType.HEADING:
            hashtag_string = re.findall(r'^(#)', block_md)
            number_heading = len(hashtag_string[0])
            if number_heading == 1:
                heading_text = re.findall(r'#\s(.+)', block_md)
                return heading_text[0]
    raise Exception("No title provided")

def generate_page(from_path, template_path, dest_path, basepath):

    print(f"Generating page form {from_path} to {dest_path} using {template_path}")
    with open (from_path, "r") as f:
        read_from_path = f.read()
    with open (template_path, "r") as f:
        read_template = f.read()
    html_node = markdown_to_html_node(read_from_path)
    html_string = html_node.to_html()
    title = extract_title(read_from_path)
    template_correct_title = read_template.replace("{{ Title }}", title)
    corrected_template = template_correct_title.replace("{{ Content }}", html_string)
    enhanced_corrected_template = corrected_template.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')
    dest_dir_name = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir_name):
        os.makedirs(dest_dir_name)
    with open (dest_path, "w") as f:
        f.write(enhanced_corrected_template)

def generate_pages_recursively(dir_path_content, template_path, dest_dir_path, basepath):
    content_items = os.listdir(dir_path_content)
    for content_item in content_items:
        item_path = os.path.join(dir_path_content, content_item)
        dest_path = os.path.join(dest_dir_path, content_item)
        if os.path.isfile(item_path):
            file_name = content_item.split('.')[0] + '.html'
 #           print(file_name)
            dest_file_path = os.path.join(dest_dir_path, file_name)
            generate_page(item_path, template_path, dest_file_path, basepath)
        else:
            generate_pages_recursively(item_path, template_path, dest_path, basepath)


def main():

    if len(sys.argv) == 1:
        basepath = '/'
    else:
        basepath = sys.argv[1]

    move_dir_contents('./static', './docs')
    generate_pages_recursively('./content', 'template.html', './docs', basepath)


main()