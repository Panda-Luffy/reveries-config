
import pyblish.api
from reveries.maya.utils import Identifier, get_id_status
from reveries.maya.plugins import MayaSelectInvalidInstanceAction


class SelectMissing(MayaSelectInvalidInstanceAction):

    label = "Select ID Missing"


class ValidateAvalonUUIDProvided(pyblish.api.InstancePlugin):
    """Ensure upstream nodes have Avalon UUID
    """

    order = pyblish.api.ValidatorOrder
    hosts = ["maya"]
    label = "Avalon UUID Provided"
    families = [
        "reveries.look",
        "reveries.animation",
        "reveries.pointcache",
    ]
    actions = [
        pyblish.api.Category("Select"),
        SelectMissing,
    ]

    @classmethod
    def get_invalid(cls, instance):
        invalid = list()
        for node in instance.data["requireAvalonUUID"]:
            if get_id_status(node) == Identifier.Untracked:
                invalid.append(node)

        return invalid

    def process(self, instance):
        invalid = self.get_invalid(instance)
        if invalid:
            raise Exception("Found untracked node, require upstream to fix.")