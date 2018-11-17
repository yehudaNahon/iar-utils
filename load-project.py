#!/usr/bin/python3
from elements import *
import argparse
from pathlib import Path
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

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='scan the project working directory and build a matching file tree representation in the iar project configuration')
    parser.add_argument(
        'file', type=str, help='a .ewp file of the project to load')

    args = parser.parse_args()

    root_path = Path().cwd()
    file_tree = build_working_tree(root_path, lambda file_path: get_path_from_workspace(root_path, file_path))
    
    

    with open("test.xml", 'w') as f:
        f.write(prettify(file_tree))



