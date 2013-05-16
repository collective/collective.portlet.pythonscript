from collective.portlet.pythonscript.content.interface import IPythonScriptManager
from plone.protect import CheckAuthenticator, PostOnly
from collective.portlet.pythonscript.browser.controlpanel import PythonScriptControlPanel

class CheckSyntaxPythonScriptView(PythonScriptControlPanel):
    """List scripts for Syntax Errors in all scripts."""

    def __call__(self):
        """Render."""
        # Check against CSRF.
        CheckAuthenticator(self.request)
        PostOnly(self.request)

        return super(CheckSyntaxPythonScriptView, self).__call__()

    def checkSyntax(self, script):
        """Check syntax of given Python Script.

        Returns sequence of error messages or empty tuple if no error is found.
        """
        script._compile()
        errors = script.errors
        return errors

    def getScripts(self):
        """Return list of available scripts descriptions."""
        manager = IPythonScriptManager(self.context)
        for path, info in manager.getScripts():
            script = manager.getScript(path)
            yield {
                'path': path,
                'title': info.title,
                'enabled': info.enabled,
                'errors': self.checkSyntax(script)
            }