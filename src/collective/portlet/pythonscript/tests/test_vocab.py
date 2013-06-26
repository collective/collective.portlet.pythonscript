from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory

from collective.portlet.pythonscript.tests.test_scriptmanager import TestScriptManager

class TestVocabulary(TestScriptManager):
    """Test enabled scripts vocabulary."""

    def assertVocabulary(self, expectedTokens):
        """Check if vocabulary returns expected tokens."""
        factory = getUtility(IVocabularyFactory, 'python-scripts')
        vocabulary = factory(self.ploneSite)
        tokens = [(term.token, term.title) for term in vocabulary]
        self.assertEqual(tokens, expectedTokens)

    def testEmpty(self):
        """Test if by default no scripts are listed."""
        result = super(TestVocabulary, self).testEmpty()
        self.assertVocabulary([])
        return result

    def testEmptyRescan(self):
        """Test if after rescanning an empty site, no scripts are listed."""
        result = super(TestVocabulary, self).testEmptyRescan()
        self.assertVocabulary([])
        return result

    def testSingleScript(self):
        """Test if after rescanning a single script is find."""
        result = super(TestVocabulary, self).testSingleScript()
        self.assertVocabulary([])
        return result

    def testMoreScripts(self):
        """Test adding more scripts."""
        result = super(TestVocabulary, self).testMoreScripts()
        self.assertVocabulary([])
        return result

    def testEnableScript(self):
        """Test enabling script."""
        result = super(TestVocabulary, self).testEnableScript()
        self.assertVocabulary([
            ('/plone/third', u'third (A Third Script)')
        ])
        return result

    def testEnableMoreScripts(self):
        """Test enabling more scripts."""
        result = super(TestVocabulary, self).testEnableMoreScripts()
        self.assertVocabulary([
            ('/plone/first', u'first (First)'),
            ('/plone/third', u'third (A Third Script)')
        ])
        return result

    def testDisableScript(self):
        """Test disabling scripts."""
        result = super(TestVocabulary, self).testDisableScript()
        self.assertVocabulary([
            ('/plone/first', u'first (First)')
        ])
        return result

    def testUntitledScript(self):
        """Test if ID is used for untitled scripts."""
        self.testEnableScript()
        ps = self.addPythonScript('four', None, 'return []')
        manager = self.getScriptManager()
        manager.enableScript('/plone/second')
        self.assertVocabulary([
            ('/plone/second', u'second'),
            ('/plone/third', u'third (A Third Script)')
        ])
