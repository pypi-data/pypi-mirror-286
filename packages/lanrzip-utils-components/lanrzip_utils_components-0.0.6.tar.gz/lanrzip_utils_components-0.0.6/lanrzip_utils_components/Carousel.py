# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Carousel(Component):
    """A Carousel component.
Carousel is an carousel component.
It takes some setting properties
You put how many blocks of divs you want inside it,
and this div turn into slides

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    Your carousel is vertical.

- id (string; optional):
    Id of the element.

- arrows (boolean; optional):
    Arrows to control carousel.

- autoplay (boolean; optional):
    If the carousel will start to play automatically.

- center_mode (boolean; optional):
    To centralize the carousel.

- center_padding (string; optional):
    Padding on the sides.

- className (string; optional):
    Style class of the component.

- dots (boolean; optional):
    Dots under carousel.

- focusOnSelect (boolean; optional):
    If you can focus on the selected slide.

- infinite (boolean; optional):
    If the carousel content will repeat in a loop.

- responsive (list; optional):
    Settings of breakpoints.

- slides_to_scroll (number; optional):
    How many slides will scroll when you swipe the carousel.

- slides_to_show (number; optional):
    How many slides you want to show.

- speed (number; optional):
    Speed of autoplay.

- style (dict; optional):
    Inline style of the component.

- swipe_to_slide (boolean; optional):
    If you can slide to scroll the slides.

- variable_width (boolean; optional):
    The slides width varies according to the screen size.

- vertical (boolean; optional):
    If your carousel is vertical."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'lanrzip_utils_components'
    _type = 'Carousel'
    @_explicitize_args
    def __init__(self, children=None, dots=Component.UNDEFINED, arrows=Component.UNDEFINED, infinite=Component.UNDEFINED, autoplay=Component.UNDEFINED, speed=Component.UNDEFINED, slides_to_show=Component.UNDEFINED, slides_to_scroll=Component.UNDEFINED, center_mode=Component.UNDEFINED, center_padding=Component.UNDEFINED, swipe_to_slide=Component.UNDEFINED, variable_width=Component.UNDEFINED, responsive=Component.UNDEFINED, vertical=Component.UNDEFINED, focusOnSelect=Component.UNDEFINED, style=Component.UNDEFINED, className=Component.UNDEFINED, id=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'arrows', 'autoplay', 'center_mode', 'center_padding', 'className', 'dots', 'focusOnSelect', 'infinite', 'responsive', 'slides_to_scroll', 'slides_to_show', 'speed', 'style', 'swipe_to_slide', 'variable_width', 'vertical']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'arrows', 'autoplay', 'center_mode', 'center_padding', 'className', 'dots', 'focusOnSelect', 'infinite', 'responsive', 'slides_to_scroll', 'slides_to_show', 'speed', 'style', 'swipe_to_slide', 'variable_width', 'vertical']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(Carousel, self).__init__(children=children, **args)
