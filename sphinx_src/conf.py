# -*- coding: utf-8 -*-
#


import inspect
import sys
import os
import sphinx.environment
from docutils.utils import get_source_line
# from mock import Mock as MagicMock
from sphinx.ext.autodoc import cut_lines

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
sys.path.insert(0, os.path.abspath('../..'))
# sys.path.insert(0, os.path.abspath('..'))


# -- General configuration ------------------------------------------------

project = 'brutils'
copyright = '2018, Amelia Brown'
author = 'Amelia Brown'

#
#
# # on_rtd is whether we are on readthedocs.org
# on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
#
# if not on_rtd:  # only import and set the theme if we're building docs locally
#     import sphinx_rtd_theme
#     html_theme = 'sphinx_rtd_theme'
#     html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

# html_theme = 'python_docs_theme'
html_theme = 'sphinx_rtd_theme'
# html_theme_path = [python_docs]

extensions = [
    'sphinx.ext.autodoc',
    # 'sphinx_autodoc_annotation',

    'sphinx.ext.doctest',
    'sphinx.ext.napoleon',
    'sphinx.ext.todo',
    'sphinx.ext.mathjax',
    'sphinx.ext.graphviz',
    'sphinx.ext.intersphinx',
    'sphinx.ext.linkcode'
]

mathjax_path = ('https://cdn.mathjax.org/mathjax/latest/MathJax.js?'
                'config=TeX-AMS-MML_HTMLorMML')

intersphinx_mapping = {
    'theano': ('http://theano.readthedocs.org/en/latest/', None),
    'numpy': ('http://docs.scipy.org/doc/numpy/', None),
    'scipy': ('http://docs.scipy.org/doc/scipy/reference/', None),
    'python': ('http://docs.python.org/3.7', None)
}
#
autodoc_member_order = 'groupwise' #'bysource'
autoclass_content = 'both'
autodoc_default_flags = ['members','undoc-members']

# autoclass_content = 'both'

#
# class Mock(MagicMock):
#     @classmethod
#     def __getattr__(cls, name):
#             return Mock()
#
#
# MOCK_MODULES = ['fuel']
# sys.modules.update((mod_name, Mock()) for mod_name in MOCK_MODULES)

graphviz_dot_args = ['-Gbgcolor=#fcfcfc']  # To match the RTD theme
graphviz_output_format = 'svg'  # To produce SVG figures

# Render todo lists
todo_include_todos = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
# source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'

# General information about the project.
# project = u'Blocks'
# copyright = u'2014-2015, Université de Montréal'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
# import blocks
# version = '.'.join(blocks.__version__.split('.')[:2])
# # The full version, including alpha/beta/rc tags.
# release = blocks.__version__

exclude_patterns = ['_build']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# html_static_path = ['_static']
#
#
# htmlhelp_basename = 'Blocksdoc'


# -- Options for LaTeX output ---------------------------------------------








def setup(app):
    app.connect('autodoc-process-docstring', cut_lines(2, what=['module']))


def linkcode_resolve(domain, info):
    """
    Determine the URL corresponding to Python object
    """
    if domain != 'py':
        return None

    modname = info['module']
    fullname = info['fullname']

    submod = sys.modules.get(modname)
    if submod is None:
        return None

    obj = submod
    for part in fullname.split('.'):
        try:
            obj = getattr(obj, part)
        except:
            return None

    try:
        fn = inspect.getsourcefile(obj)
    except:
        fn = None
    if not fn:
        return None

    try:
        source, lineno = inspect.findsource(obj)
    except:
        lineno = None

    if lineno:
        linespec = "#L%d" % (lineno + 1)
    else:
        linespec = ""

    # fn = os.path.relpath(fn, start=os.path.dirname(blocks.__file__))

    #github = "https://github.com/mila-udem/blocks/blob/master/blocks/{}{}"
    # return github.format(fn, linespec)


# Suppress "nonlocal image URI" warnings
# http://stackoverflow.com/questions/12772927
def _warn_node(self, msg, node, **kwargs):
    if not msg.startswith('nonlocal image URI found:'):
        self._warnfunc(msg, '%s:%s' % get_source_line(node), **kwargs)

sphinx.environment.BuildEnvironment.warn_node = _warn_node
