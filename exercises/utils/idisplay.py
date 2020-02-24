from IPython.display import display_html, HTML
from pygments.formatters import HtmlFormatter
from pygments import lexers, highlight


def display_yaml(yaml_path):
    """ Displays source code from an imported object.
    Parameters
    ----------
    obj: function, class or object from which you want to display the code.
    Returns
    -------
    html: HTML file
    """
    with open(yaml_path, 'r') as f:
        yaml_obj = f.read()
    yaml_lexer = lexers.get_lexer_for_mimetype('text/x-yaml')
    html = HTML(highlight(yaml_obj, yaml_lexer, HtmlFormatter()))
    display_html(html)
    return html


def pygments_css():
    """ Add nice colors to html displayed code (see display_code)
    Note
    -----
    Call this function before starting your notebook.
    """
    css = HtmlFormatter().get_style_defs('.highlight')
    html = HTML(f"""
    <style>
    {css}
    </style>
    """)
    display_html(html)
    return html