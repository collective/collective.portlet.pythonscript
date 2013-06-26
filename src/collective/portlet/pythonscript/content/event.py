from Products.PythonScripts.PythonScript import PythonScript
from Products.CMFCore.utils import getToolByName
from collective.portlet.pythonscript.content.interface import IPythonScriptManager

def onPythonScriptAdded(script):
    """Handle adding Python script item - register it with script manager."""
    portal_url = getToolByName(script, 'portal_url')
    plone_site = portal_url.getPortalObject()
    manager = IPythonScriptManager(plone_site)
    manager.addScript(script)

def onObjectAdded(obj, event):
    """PythonScripts don't implement any interfaces, so we need to check with isinstance."""
    if isinstance(obj, PythonScript):
        onPythonScriptAdded(obj)
