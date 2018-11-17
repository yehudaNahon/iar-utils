import argparse
from pathlib import Path
from xml.etree.ElementTree import ElementTree
from elements import *

def get_path_from_workspace(workspace: Path, path: Path):
    """
        return a iar path from workspace to the path specified
    """
    return "$WS_DIR$\\" + str(path.relative_to(workspace))


def create_workspace(projects: list):
    """
        Return a new workspace Element 
    """
    workspace = WorkspaceElement()
    for project in projects:
        workspace.append(project)
    return workspace

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='create a new iar workspace in the current working directory and add all iar project in all subdirectories to it')
    parser.add_argument('name', type=str, help='the workspace name')

    args = parser.parse_args()

    projects = Path().cwd().glob('**/*.ewp')

    projects = [ProjectElement(get_path_from_workspace(
        Path.cwd(), project)) for project in projects]

    workspace = WorkspaceElement(projects)

    with open(args.name + '.eww', 'w') as f:
        f.write(prettify(workspace))
