from setuptools import setup, find_packages
import os

version = '1.0'

long_description = (
    open('README.md').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    open('CONTRIBUTORS.txt').read()
    + '\n' +
    open('CHANGES.txt').read()
    + '\n')

setup(name='collective.portlet.pythonscript',
      version=version,
      description="Portlet rendering collection of items returned by customizable Python scripts",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Tomasz Mackowiak',
      author_email='tomasz.mackowiak@stxnext.pl',
      url='https://github.com/stxnext/collective.portlet.pythonscript',
      license='gpl',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['collective', 'collective.portlet'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'Plone',
          'plone.app.testing'
      ],

      entry_points="""
      # -*- Entry points: -*-
        [z3c.autoinclude.plugin]
        target = plone
      """,
      )
