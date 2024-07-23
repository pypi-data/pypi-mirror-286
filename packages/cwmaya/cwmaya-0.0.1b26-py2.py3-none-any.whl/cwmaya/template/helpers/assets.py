import os
import maya.cmds as cmds
import pymel.core as pm

import cwmaya.helpers.const as k
from cwmaya.template.helpers.scrapers import scrape_maya


def scrape_all(node):
    """Scrape all assets."""
    assets = scrape_maya_assets(node)
    assets += scrape_remote_module(node)
    return assets


def scrape_maya_assets(node):
    """Scrape Maya assets."""
    return scrape_maya.run(node)


def scrape_remote_module(node):
    """Scrape the remote tools."""
    modpath = cmds.moduleInfo(path=True, moduleName=k.MODULE_NAME)
    packagedir = os.path.dirname(modpath)
    remotemodule = os.path.join(packagedir, "storm_remote")
    return [remotemodule]


# Generate the executor files for all outScript attributes.
def scrape_py_executors(node):
    """Scrape the py executor."""

    TEMPLATE_MEL_PROC = "pyPayloadExecutor"

    modpath = pm.moduleInfo(path=True, moduleName=k.MODULE_NAME)
    packagedir = os.path.dirname(modpath)
    remotemodule = os.path.join(packagedir, "storm_remote")
    template_mel_script = os.path.join(
        remotemodule, "scripts", f"{TEMPLATE_MEL_PROC}.mel"
    )

    assets = []

    all_script_attrs = pm.listAttr(node)
    matching_attrs = [attr for attr in all_script_attrs if attr.endswith("OutScript")]
    for script_attr in matching_attrs:
        script_attr = pm.PyNode(node).attr(script_attr)
        payload_attr = pm.Attribute(f"{script_attr}Payload")

        pm.dgdirty(payload_attr)
        pm.dgdirty(script_attr)

        script = script_attr.get()
        payload = payload_attr.get()

        mel_proc_name = script.split()[-1].strip("\"' ")

        project = pm.workspace(query=True, rootDirectory=True)
        out_mel_path = os.path.join(project, "scripts", f"{mel_proc_name}.mel")

        with open(template_mel_script, "r") as file:
            mel_content = file.read()

        modified_content = mel_content.replace(TEMPLATE_MEL_PROC, mel_proc_name)
        global_string_declaration = f'global string $b64Payload = "{payload}";\n'
        modified_content = global_string_declaration + modified_content

        with open(out_mel_path, "w") as file:
            file.write(modified_content)
        assets.append(out_mel_path)

    return assets
