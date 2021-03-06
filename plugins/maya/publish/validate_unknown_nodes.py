
import pyblish.api
from reveries.plugins import context_process
from reveries.plugins import RepairContextAction
from reveries.maya.plugins import MayaSelectInvalidContextAction


class SelectUnknownNodes(MayaSelectInvalidContextAction):

    label = "Select Unknown"


class DeleteUnknownNodes(RepairContextAction):

    label = "Delete Unknown"


class ValidateUnknownNodes(pyblish.api.InstancePlugin):
    """Can not publish unknown nodes
    """

    order = pyblish.api.ValidatorOrder - 0.1
    label = "No Unknown Nodes"
    host = ["maya"]
    families = [
        "reveries.model",
        "reveries.rig",
        "reveries.look",
        "reveries.xgen",
    ]

    actions = [
        pyblish.api.Category("Select"),
        SelectUnknownNodes,
        pyblish.api.Category("Fix It"),
        DeleteUnknownNodes,
    ]

    @classmethod
    def get_invalid(cls, context):
        from maya import cmds
        return cmds.ls(type="unknown")

    @context_process
    def process(self, context):
        unknown = self.get_invalid(context)

        for node in unknown:
            self.log.error(node)

        if unknown:
            raise Exception("Scene contain unknown nodes.")

    @classmethod
    def fix_invalid(cls, context):
        """Delete unknown nodes"""
        from maya import cmds
        unknown_nodes = cls.get_invalid(context)
        lock_state = cmds.lockNode(unknown_nodes, query=True)
        for item, locked in zip(unknown_nodes, lock_state):
            if not cmds.objExists(item):
                continue
            if locked:
                cmds.lockNode(item, lock=False)
            cmds.delete(item)
