from collective.portlet.pythonscript.tests.base import TestBase

class TestScriptManager(TestBase):
    """Test script manager functionality."""

    def testEmpty(self):
        """Test if by default no scripts are listed."""
        manager = self.getScriptManager()
        scripts = manager.getScripts()
        self.assertRaises(StopIteration, scripts.next)
        enabled = manager.getEnabledScripts()
        self.assertRaises(StopIteration, enabled.next)
        
    def testEmptyRescan(self):
        """Test if after rescanning an empty site, no scripts are listed."""
        manager = self.getScriptManager()
        manager.rescanScripts()
        scripts = manager.getScripts()
        self.assertRaises(StopIteration, scripts.next)
        enabled = manager.getEnabledScripts()
        self.assertRaises(StopIteration, enabled.next)
    
    def testSingleScript(self):
        """Test if after rescanning a single script is find."""
        self.addPythonScript('first', u'First', 'return []')
        manager = self.getScriptManager()
        
        # Script should not be visible until rescan.
        scripts = manager.getScripts()
        self.assertRaises(StopIteration, scripts.next)
        enabled = manager.getEnabledScripts()
        self.assertRaises(StopIteration, enabled.next)
        
        # After rescan script should be visible...
        manager.rescanScripts()
        scripts = manager.getScripts()
        name, info = scripts.next()
        self.assertEqual(name, '/plone/first')
        self.assertEqual(info.title, u'First')
        self.assertEqual(info.enabled, False)
        self.assertEqual(info.timing, False)
        self.assertEqual(info.times, None)
        self.assertRaises(StopIteration, scripts.next)
        # ...but inactive.
        enabled = manager.getEnabledScripts()
        self.assertRaises(StopIteration, enabled.next)
