
import avalon.api
from reveries.maya.plugins import ReferenceLoader


class ModelLoader(ReferenceLoader, avalon.api.Loader):
    """Load the model"""

    label = "Reference Model"
    order = -10
    icon = "code-fork"
    color = "orange"

    hosts = ["maya"]

    families = ["reveries.model"]

    representations = [
        "mayaBinary",
    ]

    def process_reference(self, context, name, namespace, group, options):

        import maya.cmds as cmds
        from avalon import maya

        representation = context["representation"]

        entry_path = self.file_path(representation)

        with maya.maintained_selection():
            nodes = cmds.file(entry_path,
                              namespace=namespace,
                              ignoreVersion=True,
                              reference=True,
                              returnNewNodes=True,
                              groupReference=True,
                              groupName=group)
        self[:] = nodes

    def switch(self, container, representation):
        self.update(container, representation)
