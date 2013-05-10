from zope.interface import Interface, implements
from BTrees import OOBTree

class IPythonScriptManager(Interface):
    """Interface of PythonScript store and manager."""

    def addScript(self, script):
        """Adds new Python Script to store and returns ID of saved script."""

    def getScript(self, id):
        """Retrieves script of given name from store."""

    def getScripts(self):
        """Yields tuples of (scriptId, script) for all scripts in store.
        Scripts are returned ordered by titles.
        """

    def removeScript(self, id):
        """Removes script of given name from store."""

class PythonScriptManager(OOBTree.OOBTree):
    """Store and manager of Python Scripts."""
    
    implements(IPythonScriptManager)

# Key under which the script manager will be stored in the PloneSite.
PLONESITE_KEY = '__python_script_manager__'

def PythonScriptManagerAdapter(ploneSite):
    """Returns Python Script Manager for given Plone site."""
    if PLONESITE_KEY not in ploneSite:
        ploneSite[PLONESITE_KEY] = PythonScriptManager()
    return ploneSite[PLONESITE_KEY]