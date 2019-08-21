




import sys
import os

# import sphinx.environment



sys.path.insert(0, os.path.abspath('..'))
print(os.path.abspath('..'))
# sys.path.insert(0, os.path.abspath('../sphinx_src'))
project = 'brutils'
author = 'Amelia Brown'



html_theme = 'sphinx_rtd_theme'

html_show_sourcelink = True

# html_theme = 'nature'

# html_theme = 'sphinxdoc'

# html_theme = 'classic'

# html_theme = 'python-docs-theme'


# html_theme = 'sphinx_scipy_theme'
# html_theme_path = [os.path.abspath('../sphinx_src')]

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.mathjax',
    'sphinx.ext.intersphinx',
]



mathjax_path = ('https://cdn.mathjax.org/mathjax/latest/MathJax.js?'
                'config=TeX-AMS-MML_HTMLorMML')



intersphinx_mapping = {
    'numpy': ('http://docs.scipy.org/doc/numpy/', None),
    'scipy': ('http://docs.scipy.org/doc/scipy/reference/', None),
    'python': ('http://docs.python.org/3.7', None)
}



autodoc_default_flags = ['members']

source_suffix = '.rst'
add_module_names = False

master_doc = 'index'


pygments_style = 'sphinx'




# Extensions to theme docs
def setup(app):
    from sphinx.domains.python import PyField
    from sphinx.util.docfields import Field

    app.add_object_type(
        'confval',
        'confval',
        objname='configuration value',
        indextemplate='pair: %s; configuration value',
        doc_field_types=[
            PyField(
                'type',
                label=('Type',),
                has_arg=False,
                names=('type',),
                bodyrolename='class'
            ),
            Field(
                'default',
                label=('Default',),
                has_arg=False,
                names=('default',),
            ),
        ]
    )