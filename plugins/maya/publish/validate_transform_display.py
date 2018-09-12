
import pyblish.api

from reveries.maya.plugins import MayaSelectInvalidAction


class ValidateTransformDisplay(pyblish.api.InstancePlugin):
    """All transform node must be visible

    This ensures all transform node is not hidden.

    """

    order = pyblish.api.ValidatorOrder + 0.45
    hosts = ["maya"]
    label = "Hidden Transform"
    families = ["reveries.model"]
    actions = [
        pyblish.api.Category("Select"),
        MayaSelectInvalidAction,
    ]

    @staticmethod
    def get_invalid(instance):

        from maya import cmds

        invalid = list()

        display_attrs = {
            ".visibility": True,
            ".lodVisibility": True,
            ".template": False,
            ".hideOnPlayback": False,
            ".hiddenInOutliner": False,
            ".ghosting": False
        }

        for node in instance:
            if not cmds.nodeType(node) == "transforms":
                continue
            # Ensure transform shape is not hidden
            not_hidden = (
                all([cmds.getAttr(node + attr) is display_attrs[attr]
                    for attr in display_attrs.keys()])
            )

            if not not_hidden:
                invalid.append(node)

        return invalid

    def process(self, instance):

        invalid = self.get_invalid(instance)
        if invalid:
            self.log.error(
                "'%s' has hidden transforms:\n%s" % (
                    instance,
                    ",\n".join(
                        "'" + member + "'" for member in invalid))
            )
            raise Exception("<Hidden Transform> Failed.")

        self.log.info("%s <Hidden Transform> Passed." % instance)