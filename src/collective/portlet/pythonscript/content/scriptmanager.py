from zope.interface import implements
from zope.annotation.interfaces import IAnnotations
from BTrees import OOBTree
import persistent
from persistent.list import PersistentList

from collective.portlet.pythonscript.content.interface import IScriptInfo, IPythonScriptManager

class ScriptInfo(persistent.Persistent):
    """Meta-information about a Python Script."""

    implements(IScriptInfo)

    title = u""
    enabled = False
    timing = False
    times = None

    def __init__(self, title, enabled=False, timing=False):
        """Intialize."""
        self.title = title
        self.enabled = enabled
        self.timing = timing
        self.times = None

    def addTiming(self, seconds):
        """Store execution time of a script.

        Parameter must be a float with number of seconds.
        """
        assert self.timing, u'Timing must be turned on to add timing data'
        assert isinstance(seconds, float), u'Time must be float number of seconds'
        self.times.append(seconds)

    def getTiming(self):
        """Calculate executing time summaries."""
        assert self.timing, u'Timing must be turned on to get timing data'
        times = self.times
        if not len(times):
            return {
                'min_time': 0.0,
                'max_time': 0.0,
                'avg_time': 0.0,
                'samples': 0
            }
        else:
            return {
                'min_time': min(times),
                'max_time': max(times),
                'avg_time': sum(times) / len(times),
                'samples': len(times)
            }

class PythonScriptManager(object):
    """Store and manager of Python Scripts.

    Keeps data in annotations on context object (Plone site).
    """

    implements(IPythonScriptManager)

    # Key under which the script manager will be stored in the PloneSite.
    ANNOTATION_KEY = 'collective.portlet.pythonscript.manager'

    # ZODB path separator.
    PATH_SEPARATOR = '/'

    def __init__(self, context):
        """Intialize."""
        self.context = context
        annotations = IAnnotations(context)
        # 'data' stores information about found scripts:
        # data = {
        #     '/PloneSite/scriptX': ScriptInfo(u'My Script'),
        #     '/PloneSite/checkId': ScriptInfo(u'Internal')
        # }
        self.data = annotations.setdefault(self.ANNOTATION_KEY, OOBTree.OOBTree())

    # Where to search for Python script objects in the Plone site.
    SEARCHABLE_CONTAINER_PATHS = [
        (), # Plone Site
        ('portal_skins', 'custom') # "custom" directory.
    ]

    SEARCHABLE_SCRIPT_TYPES = [
        'Script (Python)',
        'Filesystem Script (Python)',
    ]

    def getScriptContainers(self):
        """Yield containers that the scripts should be searched in."""
        for path in self.SEARCHABLE_CONTAINER_PATHS:
            context = self.context
            for path_element in path:
                context = context[path_element]
            yield context

    def scanScripts(self):
        """Find scripts in given context."""
        for context in self.getScriptContainers():
            # Find all Script (Python) objects in each container.
            for item in context.objectValues(self.SEARCHABLE_SCRIPT_TYPES):
                yield item

    def getScriptTitle(self, script):
        """Generate title of the script."""
        if script.title:
            return u'%s (%s)' % (script.id, script.title)
        return script.id

    def addScript(self, script):
        """Add information about a script."""
        self._addScript(self.data, self.data, script)

    def _addScript(self, read_store, write_store, script):
        """Internal procedure for updating script information."""
        # Convert path from tuple to dot-separated list.
        path = self.PATH_SEPARATOR.join(script.getPhysicalPath())
        title = self.getScriptTitle(script)
        # And save information about all found.
        if path in read_store:
            info = read_store[path]
            info.title = title # Updated cached script title.
        else:
            info = ScriptInfo(title)
        write_store[path] = info

    def rescanScripts(self):
        """Reset information about scripts."""
        data = self.data
        # We need to keep information about enabled scripts.
        enabled = {}
        for path, info in data.iteritems():
            if info.enabled:
                enabled[path] = info
        # Clear previous data.
        data.clear()
        # Now we scan for scripts.
        for script in self.scanScripts():
            self._addScript(enabled, data, script)

    def getInfo(self, name):
        """Retrieve information about the script."""
        info = self.data[name]
        return info

    def getScript(self, name):
        """Retrieves script of given name from store."""
        if name not in self.data:
            raise KeyError(name)
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
        info.timing = False
        info.times = None

    def enableTiming(self, name):
        """Enable gathering execution times."""
        info = self.data[name]
        info.timing = True
        info.times = PersistentList()

    def disableTiming(self, name):
        """Disable gathering execution times.

        Also resets any stored execution times.
        """
        info = self.data[name]
        info.timing = False
        info.times = None

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
