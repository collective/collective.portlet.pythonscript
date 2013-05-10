from Products.Five import BrowserView
from collective.portlet.pythonscript.content.scriptmanager import IPythonScriptManager

class PythonScriptControlPanel(BrowserView):
    """Form for managing Python Scripts TTW."""

    def getScripts(self):
        """Return list of available scripts descriptions."""
        manager = IPythonScriptManager(self.context)
        for name, script in manager.getScripts():
            yield {
                'id': name,
                'title': script.title,
                'enabled': script.enabled
            }
