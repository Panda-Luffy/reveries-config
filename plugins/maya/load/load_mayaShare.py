
from reveries.maya.plugins import ReferenceLoader


class MayaShareLoader(ReferenceLoader):
    """Specific loader for the reveries.mayaShare family"""

    label = "Reference MayaShare"
    order = -10
    icon = "code-fork"
    color = "orange"

    families = ["reveries.mayaShare"]

    representations = [
        "mayaAscii",
    ]

    def process_reference(self, context, name, namespace, options):
        import maya.cmds as cmds

        representation = context["representation"]

        entry_path = self.file_path(representation["data"]["entry_fname"])

        group_name = "{}:{}".format(namespace, name)
        nodes = cmds.file(entry_path,
                          namespace=namespace,
                          sharedReferenceFile=False,
                          groupReference=True,
                          groupName=group_name,
                          reference=True,
                          lockReference=False,
                          returnNewNodes=True)

        self[:] = nodes

    def switch(self, container, representation):
        self.update(container, representation)