from collective.portlet.pythonscript.tests.base import TestBase

class TestSetup(TestBase):
    """Test if installation completes correctly."""

    def test_product_is_installed(self):
        """Validate that our products GS profile has been run and the product
        installed
        """
        pid = 'collective.portlet.pythonscript'
        installed = [p['id'] for p in self.qi_tool.listInstalledProducts()]
        self.assertTrue(pid in installed, 'package appears not to have been installed')
