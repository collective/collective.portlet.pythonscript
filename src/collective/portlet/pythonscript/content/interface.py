from zope.interface import Interface, Attribute

class IPythonScriptManager(Interface):
    """Interface of PythonScript store and manager."""

    def rescanScripts(self):
        """Reset information about scripts."""

    def addScript(self, script):
        """Add information about a script."""

    def enableScript(self, name):
        """Enable given script."""

    def disableScript(self, name):
        """Disable given script."""

    def enableTiming(self, name):
        """Enable gathering execution times."""

    def disableTiming(self, name):
        """Disable gathering execution times."""

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

class IScriptInfo(Interface):
    """Interface for objects containing meta information about scripts."""

    title = Attribute(u'Script title')
    enabled = Attribute(u'Whether script is enabled for use in portlets')
    timing = Attribute(u'Whether script has executing time gathering turned on')

    def addTiming(self, seconds):
        """Store execution time of a script.

        Parameter must be a float with number of seconds.
        """

    def getTiming(self):
        """Calculate executing time summaries.

        Returns a dictionary: {
            'min_time': minimal execution time,
            'max_time': maximal execution time,
            'avg_time': average execution time,
            'samples': number of timing samples gathered
        }
        """
