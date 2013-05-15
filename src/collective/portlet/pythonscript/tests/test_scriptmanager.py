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
        ps = self.addPythonScript('first', u'First', 'return []')
        
        # Script should not be visible until rescan.
        self.testEmpty()
        
        manager = self.getScriptManager()
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
        return ps
    
    def testGetInfoSingleScript(self):
        """Test retrieving script metadata."""
        self.testSingleScript()
        manager = self.getScriptManager()
        self.assertRaises(KeyError, manager.getInfo, '/plone/nonexisting')
        info = manager.getInfo('/plone/first')
        self.assertEqual(info.title, u'First')
        self.assertEqual(info.enabled, False)
        self.assertEqual(info.timing, False)
        self.assertEqual(info.times, None)
    
    def testGetScriptSingleScript(self):
        """Test retrieving script."""
        ps = self.testSingleScript()
        manager = self.getScriptManager()
        self.assertRaises(AssertionError, manager.getScript, '/plone/nonexisting')
        script = manager.getScript('/plone/first')
        self.assertEqual(script, ps)

    def testMoreScripts(self):
        """Test adding more scripts."""
        first = self.testSingleScript()
        second = self.addPythonScript('second', None, 'return []')
        third = self.addPythonScript('third', u'A Third Script', 'return []')
        
        # Scripts are not visible until rescan.
        manager = self.getScriptManager()
        scripts = manager.getScripts()
        name, info = scripts.next()
        self.assertEqual(name, '/plone/first')
        self.assertRaises(StopIteration, scripts.next)
        
        manager.rescanScripts()
        scripts = manager.getScripts()
        # Scripts should be ordered by title.
        name, info = scripts.next()
        self.assertEqual(name, '/plone/third')
        name, info = scripts.next()
        self.assertEqual(name, '/plone/first')
        name, info = scripts.next()
        self.assertEqual(name, '/plone/second')
        self.assertRaises(StopIteration, scripts.next)
        
        enabled = manager.getEnabledScripts()
        self.assertRaises(StopIteration, enabled.next)
        
        return [first, second, third]
    
    def testEnableScript(self):
        """Test enabling script."""
        self.testMoreScripts()
        
        manager = self.getScriptManager()
        manager.enableScript('/plone/third')
        
        enabled = manager.getEnabledScripts()
        name, info = enabled.next()
        self.assertEqual(name, '/plone/third')
        self.assertRaises(StopIteration, enabled.next)
