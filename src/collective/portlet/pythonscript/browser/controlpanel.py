from Products.Five import BrowserView
from collective.portlet.pythonscript.content.scriptmanager import IPythonScriptManager

class PythonScriptControlPanel(BrowserView):
    """Form for managing Python Scripts TTW."""

    def getScripts(self):
        """Return list of available scripts descriptions."""
        manager = IPythonScriptManager(self.context)
        for path, script in manager.getScripts():
            yield {
                'path': path,
                'title': script.title,
                'enabled': script.enabled
            }
