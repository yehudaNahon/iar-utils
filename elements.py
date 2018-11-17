from xml.etree.ElementTree import Element, SubElement, ElementTree, tostring
from xml.dom.minidom import parseString

def prettify(elem: Element):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = tostring(elem, 'utf-8')
    reparsed = parseString(rough_string)
    return reparsed.toprettyxml()

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

    def __init__(self, build_groups=[]):
        super().__init__('batchBuild')
        for build_group in build_groups:
            self.append(build_group)


class WorkspaceElement(Element):
    """
        This is a xml Element managing the logic on a workspace xml 
        this xml is the root xml in the .eww file on the iar project
    """

    def __init__(self, projects=[]):
        super().__init__('workspace')
        for project in projects:
            self.append(project)


class FolderElement(Element):
    """
        A xml representation of a folder in the iar ewp file 
        this folders are referenced as 'groups' and contain files 
        and over folders
    """

    def __init__(self, name: str):
        super().__init__('group')
        SubElement(self, 'name').text = name


class FileElement(Element):
    """
        A xml representation of a file in the iar ewp file
        the file object contains a name which contains in turn the
        path to the file the path can also be expressed with the project symbol
        and the workspace symbol for relative paths
    """

    def __init__(self, path: str):
        super().__init__('file')
        SubElement(self, 'name').text = path
