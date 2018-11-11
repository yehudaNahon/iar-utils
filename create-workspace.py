import argparse
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, ElementTree
import xml.dom.minidom

class ProjectElement(Element):
    """
        A xml Element containing a single project definition in the .eww file
        the element point to the location of the ewp file
    """
    def __init__(self, ewp_file):
        super().__init__('project')
        SubElement(self, 'path').text = ewp_file


class BuildMemberElement(Element):
    """
        A xml Element representing a single build candidate for the iar workbench
    """
    def __init__(self, name: str, configuration: str):
        super().__init__('member')
        SubElement(self, 'project').text = name
        SubElement(self, 'configuration').text = configuration


class BuildGroupElement(Element):
    """
        A xml element representing a build group instance (F8 key in iar)
        it contains a list of projects to build at once
    """
    def __init__(self, name: str, build_members: list):
        super().__init__('batchDefinition')
        SubElement(self, 'name').text = name
        for member in build_members:
            self.append(member)


class BatchBuildElement(Element):
    """
        A xml element on the batch build option for the workspace 
        it contains all the build groups definitions for the workspace
    """
    def __init__(self, build_groups = []):
        super().__init__('batchBuild')
        for build_group in build_groups:
            self.append(build_group)


class WorkspaceElement(Element):
    """
        This is a xml Element managing the logic on a workspace xml 
        this xml is the root xml in the .eww file on the iar project
    """
    def __init__(self, projects = []):
        super().__init__('workspace')
        for project in projects:
            self.append(project)
            

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

    ElementTree(WorkspaceElement(projects)).write(args.name + '.eww')
