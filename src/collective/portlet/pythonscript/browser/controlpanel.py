from Products.Five import BrowserView
from collective.portlet.pythonscript.content.interface import IPythonScriptManager

class PythonScriptControlPanel(BrowserView):
    """Form for managing Python Scripts TTW."""

    def getScripts(self):
        """Return list of available scripts descriptions."""
        manager = IPythonScriptManager(self.context)
        for path, info in manager.getScripts():
            data = {
                'path': path,
                'title': info.title,
                'enabled': info.enabled,
                'timing': info.timing
            }
            if info.timing:
                data.update(info.getTiming())
            yield data
