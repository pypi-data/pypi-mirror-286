"""
Tools for notebooks appearance.
"""

def set_container_width(width_pct: int):
    """
    Changes the Jupyter notebook HTML container width.

    Useful on widescreens to use available screen space.

    Arguments
    ---------
    width_pct (int) -- Expand the notebook width to this much of the view. Eg.
        to take up 95% of the page, use `width_pct=95`.
    """
    from IPython.core.display import display, HTML
    assert width_pct > 0 and width_pct <= 100, f'Argument `width_pct={width_pct}` must be 0<width_pct<=100'
    display(HTML(f'<style>.container {{ width:{width_pct}% !important; }}</style>'))

def vstack(*dfs, margin=10):
    from IPython.core.display import HTML
    raw_html = '<div style="display:flex; flex-direction:column;">'
    for df in dfs:
        raw_html += f'<div style="margin:{margin}px">'
        raw_html += df._repr_html_()
        raw_html += '</div>'
    raw_html += '</div>'
    return HTML(raw_html)

def hstack(*dfs, margin=10):
    from IPython.core.display import HTML
    raw_html = '<div style="display:flex">'
    for df in dfs:
        raw_html += f'<div style="margin:{margin}px">'
        raw_html += df._repr_html_()
        raw_html += '</div>'
    raw_html += '</div>'
    return HTML(raw_html)
