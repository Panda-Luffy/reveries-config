
import pyblish.api
from reveries.maya import pipeline
from reveries.plugins import RepairInstanceAction
from reveries import utils


class SetRenderRange(RepairInstanceAction):

    label = "Set Render Range"


def get_render_range(instance):
    project = instance.context.data["projectDoc"]
    asset_name = pipeline.has_turntable()
    proj_start, proj_end, _ = utils.compose_timeline_data(project,
                                                          asset_name)
    return proj_start, proj_end


def asset_has_frame_range(context):
    asset = context.data["assetDoc"]
    return "edit_in" in asset["data"]


class ValidateRenderRange(pyblish.api.InstancePlugin):
    """Ensure render setttings has been set correctly

        This plugin validate the rendering range (strict)

    """

    label = "Render Range"
    order = pyblish.api.ValidatorOrder + 0.2
    hosts = ["maya"]
    families = [
        "reveries.imgseq.render",
    ]
    actions = [
        pyblish.api.Category("Fix It"),
        SetRenderRange,
    ]

    @classmethod
    def get_invalid(cls, instance):
        """Rendering range should be the same as pre-defined range"""
        proj_start, proj_end = get_render_range(instance)
        render_start = instance.data["startFrame"]
        render_end = instance.data["endFrame"]

        if proj_start != render_start or proj_end != render_end:
            cls.log.error("Invalid frame range: {0} - {1}"
                          "".format(render_start, render_end))
            cls.log.error("start and end frame should be {0} - {1}."
                          "".format(proj_start, proj_end))
            return True

    def process(self, instance):

        if not asset_has_frame_range(instance.context):
            self.log.info("No range been set on this asset, skipping..")
            return True

        self.log.info("Validating frame range..")
        if self.get_invalid(instance):
            raise Exception("Rendering frame range is not correct.")

    @classmethod
    def fix_invalid(cls, instance):
        from maya import cmds

        proj_start, proj_end = get_render_range(instance)
        cmds.setAttr("defaultRenderGlobals.startFrame", proj_start)
        cmds.setAttr("defaultRenderGlobals.endFrame", proj_end)
