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

        # Script should be visible immediately after creation.
        manager = self.getScriptManager()
        scripts = manager.getScripts()
        name, info = scripts.next()
        self.assertEqual(name, '/plone/first')
        self.assertEqual(info.title, u'first (First)')
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
        self.assertEqual(info.title, u'first (First)')
        self.assertEqual(info.enabled, False)
        self.assertEqual(info.timing, False)
        self.assertEqual(info.times, None)

    def testGetScriptSingleScript(self):
        """Test retrieving script."""
        ps = self.testSingleScript()
        manager = self.getScriptManager()
        self.assertRaises(KeyError, manager.getScript, '/plone/nonexisting')
        script = manager.getScript('/plone/first')
        self.assertEqual(script, ps)

    def testMoreScripts(self):
        """Test adding more scripts."""
        first = self.testSingleScript()
        second = self.addPythonScript('second', None, 'return []')
        third = self.addPythonScript('third', u'A Third Script', 'return []')

        # Scripts are visible immediately.
        manager = self.getScriptManager()
        scripts = manager.getScripts()
        # Scripts should be ordered by title.
        name, _info = scripts.next()
        self.assertEqual(name, '/plone/first')
        name, _info = scripts.next()
        self.assertEqual(name, '/plone/second')
        name, _info = scripts.next()
        self.assertEqual(name, '/plone/third')
        self.assertRaises(StopIteration, scripts.next)

        enabled = manager.getEnabledScripts()
        self.assertRaises(StopIteration, enabled.next)

        return [first, second, third]
    
    def testPortalSkinsScripts(self):
        """Test if skins inside portal_skins/custom directory can be scanned."""
        self.addPythonScript('nested', u'Nested', 'return []',
            self.ploneSite.portal_skins.custom)
        
        manager = self.getScriptManager()
        scripts = manager.getScripts()
        name, _info = scripts.next()
        self.assertEqual(name, '/plone/portal_skins/custom/nested')
        self.assertRaises(StopIteration, scripts.next)

    def testEnableScript(self):
        """Test enabling script."""
        self.testMoreScripts()

        manager = self.getScriptManager()
        manager.enableScript('/plone/third')

        enabled = manager.getEnabledScripts()
        name, _info = enabled.next()
        self.assertEqual(name, '/plone/third')
        self.assertRaises(StopIteration, enabled.next)

    def testEnableMoreScripts(self):
        """Test enabling more scripts."""
        self.testEnableScript()

        manager = self.getScriptManager()
        manager.enableScript('/plone/first')

        enabled = manager.getEnabledScripts()
        name, _info = enabled.next()
        self.assertEqual(name, '/plone/first')
        name, _info = enabled.next()
        self.assertEqual(name, '/plone/third')
        self.assertRaises(StopIteration, enabled.next)

    def testDisableScript(self):
        """Test disabling scripts."""
        self.testEnableMoreScripts()

        manager = self.getScriptManager()
        self.assertRaises(KeyError, manager.disableScript, '/plone/nonexisting')

        manager.disableScript('/plone/third')

        enabled = manager.getEnabledScripts()
        name, _info = enabled.next()
        self.assertEqual(name ,'/plone/first')
        self.assertRaises(StopIteration, enabled.next)

    def testEnableTiming(self):
        """Test enable timing."""
        self.testEnableMoreScripts()

        manager = self.getScriptManager()
        info = manager.getInfo('/plone/third')

        # Cannot get or add timing when timing was not enabled.
        self.assertRaises(AssertionError, info.getTiming)
        self.assertRaises(AssertionError, info.addTiming, 0.3)

        # Error is raised when unknown script is tried.
        self.assertRaises(KeyError, manager.enableTiming, '/plone/nonexisting')
        manager.enableTiming('/plone/third')

        self.assertEqual(info.getTiming(), {
            'min_time': 0.0,
            'avg_time': 0.0,
            'max_time': 0.0,
            'samples': 0
        })
        info.addTiming(0.1)
        info.addTiming(0.2)
        info.addTiming(0.3)
        info.addTiming(0.4)
        self.assertEqual(info.getTiming(), {
            'min_time': 0.1,
            'avg_time': 0.25,
            'max_time': 0.4,
            'samples': 4
        })

    def testDisableTiming(self):
        """Test disable timing."""
        self.testEnableTiming()

        manager = self.getScriptManager()
        self.assertRaises(KeyError, manager.disableTiming, '/plone/nonexisting')

        manager.disableTiming('/plone/third')
        info = manager.getInfo('/plone/third')
        # Cannot get or add timing when timing was not enabled.
        self.assertRaises(AssertionError, info.getTiming)
        self.assertRaises(AssertionError, info.addTiming, 0.3)

        # After re-enabling timing timing data should be reset.
        manager.enableTiming('/plone/third')
        self.assertEqual(info.getTiming(), {
            'min_time': 0.0,
            'avg_time': 0.0,
            'max_time': 0.0,
            'samples': 0
        })

    def testDisableScriptTiming(self):
        """Test if timing data is reset when script is disabled."""
        self.testEnableTiming()

        manager = self.getScriptManager()
        manager.disableScript('/plone/third')

        info = manager.getInfo('/plone/third')
        self.assertEqual(info.timing, False)
        # Cannot get or add timing when script is disabled.
        self.assertRaises(AssertionError, info.getTiming)
        self.assertRaises(AssertionError, info.addTiming, 0.3)

        manager.enableScript('/plone/third')
        self.assertEqual(info.timing, False)
        # Cannot get or add timing when timing is disabled.
        self.assertRaises(AssertionError, info.getTiming)
        self.assertRaises(AssertionError, info.addTiming, 0.3)

        # After re-enabling timing timing data should be reset.
        manager.enableTiming('/plone/third')
        self.assertEqual(info.timing, True)
        self.assertEqual(info.getTiming(), {
            'min_time': 0.0,
            'avg_time': 0.0,
            'max_time': 0.0,
            'samples': 0
        })