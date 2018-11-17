#!/usr/bin/python3
from elements import *
import argparse
from pathlib import Path
from logging import error

from xml.etree.ElementTree import ElementTree

def build_working_tree(path: Path, to_relative):
    suffixes = ['.h', '.c', '.hpp', '.cpp']
    if path.is_file() and path.suffix in suffixes:
        return FileElement(to_relative(path))

    if path.is_dir():
        element = FolderElement(path.name)
        for child_path in path.glob('*'):
            sub_element = build_working_tree(child_path, to_relative)
            if sub_element is None:
                continue
            element.append(sub_element)

        # check the len if there is no other elements it will be 1
        if len(element) == 1:
            return None
        return element
    return None

def get_path_from_workspace(workspace: Path, path: Path):
    """
        return a iar path from workspace to the path specified
    """
    return "$WS_DIR$\\" + str(path.relative_to(workspace))

def remove_all_files_and_folders(element: Element):
    for folder_elem in element.findall('group'):
        ewp_root.remove(folder_elem)

    for file_elem in element.findall('file'):
        ewp_root.remove(file_elem)

def strip_xml(element: Element):
    element.tail = None
    if element.text is not None:
        element.text = element.text.strip()

    for sub in element:
        strip_xml(sub)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='scan the project working directory and build a matching file tree representation in the iar project configuration')
    parser.add_argument(
        'file', type=str, help='a .ewp file of the project to load')

    args = parser.parse_args()

    ewp_file = Path(args.file)
    if not ewp_file.exists() or ewp_file.suffix != '.ewp':
        error(f"could not find {ewp_file}")

    ewp_root = ElementTree(file=ewp_file).getroot()

    remove_all_files_and_folders(ewp_root)

    strip_xml(ewp_root)

    root_path = ewp_file.parent
    for child in build_working_tree(root_path, lambda path: get_path_from_workspace(root_path, path)):
        ewp_root.append(child) 

    ewp_file.write_text(prettify(ewp_root))



