import unittest2 as unittest

from Products.CMFCore.utils import getToolByName
from Products.PythonScripts.PythonScript import PythonScript

from collective.portlet.pythonscript.testing import\
    COLLECTIVE_PORTLET_PYTHONSCRIPT_INTEGRATION

class TestBase(unittest.TestCase):
    """Base test case."""

    layer = COLLECTIVE_PORTLET_PYTHONSCRIPT_INTEGRATION

    def setUp(self):
        """Setup fixture."""
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.qi_tool = getToolByName(self.portal, 'portal_quickinstaller')
        self.ploneSite = self.app.plone

    def createPythonScript(self, title, code):
        """Creare new Python Script object."""
        ps = PythonScript('ps')
        ps.ZPythonScript_setTitle(title)
        ps.write(code)
        ps._makeFunction()
        return ps

    def addPS(self, id_, title, code):
        """Add new Python Script to Plone Site."""
        ps = self.createPythonScript(title, code)
        self.ploneSite._setOb(id_, ps)
        return ps
