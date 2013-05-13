import urllib

from zope.interface import Interface
from Products.CMFPlone import PloneMessageFactory as _

from collective.portlet.pythonscript.content.scriptmanager import IPythonScriptManager
from collective.portlet.pythonscript.browser.edit_pythonscript import EditPythonScriptForm

class DeletePythonScriptForm(EditPythonScriptForm):
    """Form for deleting Python Scripts."""

    schema = Interface

    label = _(u"Delete Python Script")

    @property
    def description(self):
        """Render script title in form header."""
        content = self.getContent()
        return _(u"Delete Python Script '${title}'?", mapping={u'title': content.title})

    @property
    def action(self):
        """Change the form action to include the Python Script name."""
        name = self.request.form['id']
        encoded = urllib.quote_plus(name.encode('utf-8'))
        return self.context.absolute_url() + '/@@delete_pythonscript?id=%s' % encoded

    def applyChanges(self, data):
        """Remove the script."""
        name = self.request.form['id']
        manager = IPythonScriptManager(self.context)
        manager.removeScript(name)

    def updateActions(self):
        super(DeletePythonScriptForm, self).updateActions()
        saveAction = self.actions["save"]
        saveAction.title = _(u'Delete')
    