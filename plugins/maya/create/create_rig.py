from maya import cmds
import avalon.maya


class RigCreator(avalon.maya.Creator):
    """Animatable Controller"""

    name = "rigDefault"
    label = "Rig"
    family = "reveries.rig"
    icon = "sitemap"

    rig_subsets = [
        name,
        "rigXGen",
        "rigCloth",
    ]

    def process(self):
        subset_name = self.data["subset"]

        # Check subset name, prevent typo
        if subset_name not in self.rig_subsets:
            err_msg = "Invalid subset name: {}".format(subset_name)
            raise RuntimeError(err_msg)

        container = super(RigCreator, self).process()
        self.log.info("Creating Rig instance set up ...")

        sub_object_sets = ["OutSet", "ControlSet"]

        for set_name in sub_object_sets:
            cmds.sets(cmds.sets(name=set_name, empty=True),
                      forceElement=container)
