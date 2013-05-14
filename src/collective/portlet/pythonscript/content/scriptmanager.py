from zope.interface import Interface, implements
from zope.annotation.interfaces import IAnnotations
from BTrees import OOBTree
import persistent

class IPythonScriptManager(Interface):
    """Interface of PythonScript store and manager."""

    def rescanScripts(self):
        """Reset information about scripts."""
        
    def enableScript(self, name):
        """Enable given script."""
    
    def disableScript(self, name):
        """Disable given script."""

    def getInfo(self, name):
        """Retrieve information about the script."""

    def getScript(self, name):
        """Retrieves script of given name from store."""

    def getScripts(self):
        """Yields tuples of (scriptId, script) for all scripts in store.
        Scripts are returned ordered by titles.
        """

    def getEnabledScripts(self):
        """Yield tuples of (scriptId, script) for all enabled scripts in store.
        Scripts are returned ordered by titles.
        """

class ScriptInfo(persistent.Persistent):
    
    def __init__(self, title, enabled):
        self.title = title
        self.enabled = enabled

class PythonScriptManager(object):
    """Store and manager of Python Scripts."""

    implements(IPythonScriptManager)

    # Key under which the script manager will be stored in the PloneSite.
    ANNOTATION_KEY = 'collective.portlet.pythonscript.manager'

    PATH_SEPARATOR = '/'

    def __init__(self, context):
        """Intialize."""
        self.context = context
        annotations = IAnnotations(context)
        # 'data' stores information about found scripts:
        # data = {
        #     '/PloneSite/scriptX': {'title': u'My Script', 'enabled': True},
        #     '/PloneSite/checkId': {'title': u'Internal', 'enabled': False}
        # }
        self.data = annotations.setdefault(self.ANNOTATION_KEY, OOBTree.OOBTree())

    def scanScripts(self, context):
        for item in context.objectValues('Script (Python)'):
            # TODO: recursion?
            yield item

    def rescanScripts(self):
        """Reset information about scripts."""
        data = self.data
        # We need to keep information about enabled scripts.
        enabled = {}
        for path, info in data.iteritems():
            if info.enabled:
                enabled[path] = True
        # Clear previous data.
        data.clear()
        # Now we scan for scripts.
        for script in self.scanScripts(self.context):
            # Convert path from tuple to dot-separated list.
            path = self.PATH_SEPARATOR.join(script.getPhysicalPath())
            # And save information about all found.
            data[path] = ScriptInfo(script.title, path in enabled)
    
    def getInfo(self, name):
        """Retrieve information about the script."""
        info = self.data[name]
        return info
    
    def getScript(self, name):
        """Retrieves script of given name from store."""
        assert name in self.data
        script = self.context.unrestrictedTraverse(name)
        return script
    
    def enableScript(self, name):
        """Enable given script."""
        info = self.data[name]
        info.enabled = True

    def disableScript(self, name):
        """Disable given script."""
        info = self.data[name]
        info.enabled = False

    def getScripts(self):
        """Yields tuples of (scriptId, script) for all scripts in store.
        Scripts are returned ordered by titles.
        """
        data = self.data
        by_title = []
        for path, info in data.iteritems():
            by_title.append((info.title, path))
        # Sort by titles.
        by_title.sort(key=lambda t: t[0])
        for _title, path in by_title:
            yield path, data[path]

    def getEnabledScripts(self):
        """Yield tuples of (scriptId, script) for all enabled scripts in store.
        Scripts are returned ordered by titles.
        """
        for path, info in self.getScripts():
            if not info.enabled:
                continue
            yield path, info
