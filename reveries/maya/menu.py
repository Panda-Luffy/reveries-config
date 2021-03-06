import sys
import logging
from avalon import api
from avalon.vendor.Qt import QtCore
from maya import cmds

from . import PYMEL_MOCK_FLAG

self = sys.modules[__name__]
self._menu = api.Session.get("AVALON_LABEL", "Avalon") + "menu"

log = logging.getLogger(__name__)


def _arnold_update_full_scene(*args):
    try:
        from . import arnold
    except RuntimeError:
        return

    arnold.utils.update_full_scene()


def install():
    from . import interactive

    def deferred():
        # Append to Avalon's menu
        cmds.menuItem(divider=True)

        cmds.menuItem("Snap!", command=interactive.active_view_snapshot)

        # Rendering tools
        cmds.menuItem("Menu_Render",
                      label="Render",
                      tearOff=True,
                      subMenu=True,
                      parent=self._menu)

        cmds.menuItem(divider=True, dividerLabel="Arnold")

        cmds.menuItem("ArnoldUpdateFullScene",
                      label="Update Full Scene",
                      parent="Menu_Render",
                      image="playbackLoopingContinuous.png",
                      command=_arnold_update_full_scene)

        # LookDev tools
        cmds.menuItem("Menu_LookDev",
                      label="LookDev",
                      tearOff=True,
                      subMenu=True,
                      parent=self._menu)

#        cmds.menuItem("V-Ray Attributes", command="""
# import reveries.maya.tools
# reveries.maya.tools.show('vray_attrs_setter')
# """)
        cmds.menuItem("Look Assigner", parent="Menu_LookDev", command="""
import reveries.maya.tools
reveries.maya.tools.show('mayalookassigner')
""")

        cmds.menuItem("Set AvalonUUID", parent="Menu_LookDev",
                      command=interactive.apply_avalon_uuid)

        cmds.menuItem("Swap Modle", parent="Menu_LookDev",
                      command=interactive.swap_to_published_model)

        # XGen tools
        cmds.menuItem("Menu_XGen",
                      label="XGen",
                      tearOff=True,
                      subMenu=True,
                      parent=self._menu)

        cmds.menuItem(divider=True, dividerLabel="XGen Legacy")

        cmds.menuItem("Bind Legacy",
                      parent="Menu_XGen",
                      command=interactive.bind_xgen_legacy_by_selection)
        cmds.menuItem("Bake All Descriptions",
                      parent="Menu_XGen",
                      command=interactive.bake_all_xgen_legacy_descriptions)
        cmds.menuItem("Bake All Modifiers",
                      parent="Menu_XGen",
                      command=interactive.bake_all_xgen_legacy_modifiers)
        cmds.menuItem("Link Hair System",
                      parent="Menu_XGen",
                      command=interactive.link_palettes_to_hair_system)
        cmds.menuItem("Set RefWire Frame",
                      parent="Menu_XGen",
                      command=interactive.set_refwires_frame_by_nucleus)

        cmds.menuItem(divider=True, dividerLabel="XGen Interactive Groom")

        cmds.menuItem("Bind Interactive Groom",
                      parent="Menu_XGen",
                      command=interactive.bind_xgen_interactive_by_selection)

        # System
        cmds.menuItem("Load PyMel", parent="System", command="""
import sys, os
MOCK_FLAG = {!r}
if os.path.isfile(MOCK_FLAG):
    os.remove(MOCK_FLAG)
if "pymel.core" in sys.modules:
    del sys.modules["pymel.core"]
import pymel.core
""".format(PYMEL_MOCK_FLAG))

        cmds.menuItem("Mock PyMel", parent="System", command="""
with open({!r}, "w") as flag:
    flag.write("")
""".format(PYMEL_MOCK_FLAG))

    # Allow time for uninstallation to finish.
    QtCore.QTimer.singleShot(200, deferred)


def uninstall():
    pass
