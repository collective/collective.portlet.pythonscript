from plone.directives import form
from z3c.form import button
from collective.portlet.pythonscript.content.pythonscript import IPythonScript,\
    PythonScript
from z3c.form.form import applyChanges
from collective.portlet.pythonscript.content.scriptmanager import IPythonScriptManager

class AddPythonScriptForm(form.SchemaAddForm):
    """Form for adding new Python Scripts."""

    schema = IPythonScript

    label = u"Add new Python Script"
    description = u"Create new Python Script that can be used as catalog query in Python Script portlet"

    def create(self, data):
        """Create new object."""
        script = PythonScript()
        applyChanges(self, script, data)
        return script

    def add(self, script):
        """Add newly created object to the database."""
        manager = IPythonScriptManager(self.context)
        manager.addScript(script)

    def nextURL(self):
        """Redirect to control panel."""
        return self.context.absolute_url() + '/@@manage_pythonscript'