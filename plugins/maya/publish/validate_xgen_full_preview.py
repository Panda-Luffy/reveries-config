
import pyblish.api


class ValidateXGenFullPreview(pyblish.api.InstancePlugin):
    """Should publish with 100% primitives generated preview

    All primitives must be seen.

    """

    order = pyblish.api.ValidatorOrder
    hosts = ["maya"]
    label = "XGen Full Preview"
    families = [
        "reveries.xgen.legacy",
    ]

    @classmethod
    def get_invalid(cls, instance):
        import xgenm as xg

        invalid = list()

        for description in instance.data["xgenDescriptions"]:
            palette = xg.palette(description)
            percent = float(xg.getAttr("percent",
                                       palette,
                                       description,
                                       "GLRenderer"))
            if not percent == 100:
                invalid.append(description)

        return invalid

    def process(self, instance):
        invalid = self.get_invalid(instance)
        if invalid:
            for i in invalid:
                self.log.error(i)
            raise Exception("These descriptions not preview 100% primitives.")
