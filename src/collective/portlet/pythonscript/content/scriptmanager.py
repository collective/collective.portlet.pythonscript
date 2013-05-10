from Acquisition import Explicit
from zope.interface import Interface, implements
from zope.annotation.interfaces import IAnnotations
from BTrees import OOBTree
from plone.app.content.namechooser import NormalizingNameChooser
from zope.container.interfaces import INameChooser
from zope.container.contained import NameChooser
from zope.container import folder
from collective.portlet.pythonscript.content.pythonscript import IPythonScript
from zope.component._api import getUtility
from plone.i18n.normalizer.interfaces import IURLNormalizer
from plone.app.content.interfaces import INameFromTitle

class IPythonScriptManager(Interface):
    """Interface of PythonScript store and manager."""

    def addScript(self, script):
        """Adds new Python Script to store and returns ID of saved script."""

    def getScript(self, name):
        """Retrieves script of given name from store."""

    def getScripts(self):
        """Yields tuples of (scriptId, script) for all scripts in store.
        Scripts are returned ordered by titles.
        """

    def removeScript(self, name):
        """Removes script of given name from store."""

class ScriptNameChooser(NormalizingNameChooser):
    """Name chooser for Python Scripts."""
    
    def chooseName(self, name, object):
        if not name:
            nameFromTitle = INameFromTitle(object, None)
            if nameFromTitle is not None:
                name = nameFromTitle.title
            if not name:
                name = object.__class__.__name__
  
        if not isinstance(name, unicode):
            name = unicode(name, 'utf-8')
  
        name = getUtility(IURLNormalizer).normalize(name)
  
        return self._findUniqueName(name, object)
    
    def _getCheckId(self, object):
        """Return a function that can act as the check_id script.
        """
        return lambda id_, required: id_ in self.context

class PythonScriptManager(folder.Folder):
    """Store and manager of Python Scripts."""
    
    implements(IPythonScriptManager)
    
    def addScript(self, script):
        """Adds new Python Script to store and returns ID of saved script."""
        assert IPythonScript.providedBy(script)
        name_chooser = INameChooser(self)
        name = name_chooser.chooseName(None, script)
        self[name] = script
        return name

    def getScript(self, name):
        """Retrieves script of given name from store."""
        script = self[name]
        assert IPythonScript.providedBy(script)
        return script
    
    def removeScript(self, name):
        """Removes script of given name from store."""
        script = self[name]
        assert IPythonScript.providedBy(script)
        del self[name]
        return script

    def getScripts(self):
        """Yields tuples of (scriptId, script) for all scripts in store.
        Scripts are returned ordered by titles.
        """
        by_title = [(self[name].title, name) for name in self]
        # Sort by titles.
        by_title.sort(key=lambda t: t[0])
        for _title, name in by_title:
            yield name, self[name]

# Key under which the script manager will be stored in the PloneSite.
ANNOTATION_KEY = 'collective.portlet.pythonscript.manager'

def pythonScriptManagerAdapter(ploneSite):
    """Returns Python Script Manager for given Plone site."""
    # Manager is stored in annotations.
    annotations = IAnnotations(ploneSite)
    return annotations.setdefault(ANNOTATION_KEY, PythonScriptManager())
