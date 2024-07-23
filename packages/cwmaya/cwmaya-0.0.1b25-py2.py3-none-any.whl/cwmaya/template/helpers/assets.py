import os
import maya.cmds as cmds

import cwmaya.helpers.const as k
from cwmaya.template.helpers.scrapers import scrape_maya


def scrape_maya_assets():
    """Scrape Maya assets."""
    return scrape_maya.run()


def scrape_remote_module():
    """Scrape the remote tools."""
    modpath = cmds.moduleInfo(path=True, moduleName=k.MODULE_NAME)
    packagedir = os.path.dirname(modpath)
    remotemodule = os.path.join(packagedir, "storm_remote")
    return [remotemodule]


def scrape_all():
    """Scrape all assets."""
    assets = scrape_maya_assets()
    assets += scrape_remote_module()
    return assets
