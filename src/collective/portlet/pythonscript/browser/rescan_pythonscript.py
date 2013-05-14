from Products.CMFPlone import PloneMessageFactory as _
from Products.Five.browser import BrowserView
from collective.portlet.pythonscript.content.scriptmanager import IPythonScriptManager
from Products.statusmessages.interfaces import IStatusMessage

class RescanPythonScriptView(BrowserView):

    def __call__(self):
        """Rescan and redirect."""
        manager = IPythonScriptManager(self.context)
        manager.rescanScripts()
        IStatusMessage(self.request).addStatusMessage(_(u'Rescanned'))
        self.request.response.redirect(self.context.absolute_url() + '/@@manage_pythonscript')