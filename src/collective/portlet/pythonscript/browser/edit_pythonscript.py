import urllib
from urlparse import urlparse, parse_qs

from plone.directives import form
from Products.CMFPlone import PloneMessageFactory as _

from collective.portlet.pythonscript.content.pythonscript import IPythonScript
from collective.portlet.pythonscript.content.scriptmanager import IPythonScriptManager

class EditPythonScriptForm(form.SchemaEditForm):
    """Form for editing Python Scripts."""

    schema = IPythonScript

    # TODO: i18n
    label = _(u"Edit Python Script")
    description = _(u"Edit Python Script that can be used as catalog query in Python Script portlet")

    def getContent(self):
        """Get edited object."""
        if 'id' in self.request.form:
            # Normal request.
            name = self.request.form['id']
        else:
            # KSS validation will not pass the 'id' parameter, we can extract it
            # from referrer.
            referer = self.request.get_header('Referer')
            # Example: 'http://localhost:8080/Plone/@@edit_pythonscript?id=gowno-zolwia'
            url = urlparse(referer)
            params = parse_qs(url.query)
            name = params['id'][0]
        manager = IPythonScriptManager(self.context)
        script = manager.getScript(name)
        return script

    @property
    def action(self):
        """Change the form action to include the Python Script name."""
        name = self.request.form['id']
        encoded = urllib.quote_plus(name.encode('utf-8'))
        return self.context.absolute_url() + '/@@edit_pythonscript?id=%s' % encoded
    
    def __call__(self):
        """Default implementation would redirect to Plone Site view, but we
        want to show the Python Scripts management interface instead.
        """
        result = super(EditPythonScriptForm, self).__call__()
        if result == u'':
            self.request.response.redirect(self.context.absolute_url() + '/@@manage_pythonscript')
        return result
