collective.portlet.pythonscript
===============================

This add-on product adds ability to use 'Script (Python)' objects as source
of items to display in a 'Python Script Portlet'.

Usage
=====
Manager adds 'Script (Python)' objects to the Plone site. The scripts need to
return an iterable of portal catalog brains (or objects adaptable to
IPythonScriptPortletItem).

Manager goes into control panel and in 'Scriptable Portlets' selects option to
rescan site for 'Script (Python)' objects. Now the control panel section should
list the added scripts.

Manager enables scripts for use in portlets.

User edits portlets assigned in any place in the site. He can add new
'Python Script' portlet. Each portlet has a title and script used to render results.
User can limit number of shown results.

Site displays results of the query inside the portlet.
