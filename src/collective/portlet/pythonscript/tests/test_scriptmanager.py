from collective.portlet.pythonscript.tests.base import TestBase

class TestScriptManager(TestBase):

    def testX(self):
        self.addPS('empty', 'Empty', 'return []')
