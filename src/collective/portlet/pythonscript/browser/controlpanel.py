from Products.Five import BrowserView

class PythonScriptControlPanel(BrowserView):
    """
    Form for managing Python Scripts TTW.
    """

    def getScripts(self):
        """Return list of available scripts descriptions."""
        return [
            {
                'id': u'xxx',
                'title': u'XXX',
                'enabled': True
            },
            {
                'id': u'yyy',
                'title': u'YYY',
                'enabled': False
            }
        ]