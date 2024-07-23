from ._element import _Block, _Control, _Element
from ._element import html as html
from .page import Page as Page

class text(_Control):
    _ELEMENT_NAME: str
    def __init__(
        self,
        value=...,
        raw=...,
        mode=...,
        format=...,
        id=...,
        properties=...,
        class_name=...,
        hover_text=...,
    ) -> None:
        """### Arguments:
        value (dynamic(any)): The value displayed as text by this control. (default: "")
        raw (bool): If set to True, the component renders as an HTML \<span\> element without any default style. (default: False)
        mode (str): Define the way the text is processed:* "raw": synonym for setting the \*raw\* property to True
        * "pre": keeps spaces and new lines
        * "markdown" or "md": basic support for Markdown.

        format (str): The format to apply to the value.See below.
        id (str): The identifier that will be assigned to the rendered HTML component.
        properties (dict[str, any]): Bound to a dictionary that contains additional properties for this element.
        class_name (dynamic(str)): The list of CSS class names that will be associated with the generated HTML Element.These class names will be added to the default `taipy-<element_type>`.
        hover_text (dynamic(str)): The information that is displayed when the user hovers over this element.
        """
        ...

class button(_Control):
    _ELEMENT_NAME: str
    def __init__(
        self,
        label=...,
        on_action=...,
        active=...,
        id=...,
        properties=...,
        class_name=...,
        hover_text=...,
    ) -> None:
        """### Arguments:
        label (dynamic(str|Icon)): The label displayed in the button. (default: "")
        on_action (Callback): The name of a function that is triggered when the button is pressed.The parameters of that function are all optional:
         * state (`State^`): the state instance.
        * id (optional\[str]): the identifier of the button.
        * payload (dict): a dictionary that contains the key "action" set to the name of the action that triggered this callback.

        active (dynamic(bool)): Indicates if this component is active.An inactive component allows no user interaction. (default: True)
        id (str): The identifier that will be assigned to the rendered HTML component.
        properties (dict[str, any]): Bound to a dictionary that contains additional properties for this element.
        class_name (dynamic(str)): The list of CSS class names that will be associated with the generated HTML Element.These class names will be added to the default `taipy-<element_type>`.
        hover_text (dynamic(str)): The information that is displayed when the user hovers over this element.
        """
        ...

class input(_Control):
    _ELEMENT_NAME: str
    def __init__(
        self,
        value=...,
        password=...,
        label=...,
        multiline=...,
        lines_shown=...,
        type=...,
        change_delay=...,
        on_action=...,
        action_keys=...,
        on_change=...,
        propagate=...,
        active=...,
        id=...,
        properties=...,
        class_name=...,
        hover_text=...,
    ) -> None:
        """### Arguments:
        value (dynamic(any)): The value represented by this control. (default: None)
        password (bool): If True, the text is obscured: all input characters are displayed as an asterisk ('\*'). (default: False)
        label (str): The label associated with the input. (default: None)
        multiline (bool): If True, the text is presented as a multi line input. (default: False)
        lines_shown (int): The height of the displayed element if multiline is True. (default: 5)
        type (str): TODO: The type of input: text, tel, email ... as defined in HTML standards https://developer.mozilla.org/en\-US/docs/Web/HTML/Element/input\#input\_types  (default: "text")
        change_delay (int): Minimum time between triggering two calls to the on\_change callback.The default value is defined at the application configuration level by the **change\_delay** configuration option. if None, the delay is set to 300 ms.If set to \-1, the input change is triggered only when the user presses the Enter key. (default: *App config*)
        on_action (Callback): Name of a function that is triggered when a specific key is pressed.The parameters of that function are all optional:
         * state (`State^`): the state instance.
        * id (str): the identifier of the input.
        * payload (dict): the details on this callback's invocation.
         This dictionary has the following keys:
                + action: the name of the action that triggered this callback.
                + args (list):
                        - key name
                        - variable name
                        - current value

        action_keys (str): Semicolon (';')\-separated list of supported key names.Authorized values are Enter, Escape, F1, F2, F3, F4, F5, F6, F7, F8, F9, F10, F11, F12\. (default: "Enter")
        on_change (Callback): The name of a function that is triggered when the value is updated.The parameters of that function are all optional:
         * state (`State^`): the state instance.
        * var\_name (str): the variable name.
        * value (any): the new value.

        propagate (bool): Allows the control's main value to be automatically propagated.The default value is defined at the application configuration level.If True, any change to the control's value is immediately reflected in the bound application variable. (default: *App config*)
        active (dynamic(bool)): Indicates if this component is active.An inactive component allows no user interaction. (default: True)
        id (str): The identifier that will be assigned to the rendered HTML component.
        properties (dict[str, any]): Bound to a dictionary that contains additional properties for this element.
        class_name (dynamic(str)): The list of CSS class names that will be associated with the generated HTML Element.These class names will be added to the default `taipy-<element_type>`.
        hover_text (dynamic(str)): The information that is displayed when the user hovers over this element.
        """
        ...

class number(_Control):
    _ELEMENT_NAME: str
    def __init__(
        self,
        value=...,
        label=...,
        step=...,
        step_multiplier=...,
        min=...,
        max=...,
        change_delay=...,
        on_action=...,
        action_keys=...,
        on_change=...,
        propagate=...,
        active=...,
        id=...,
        properties=...,
        class_name=...,
        hover_text=...,
    ) -> None:
        """### Arguments:
        value (dynamic(any)): The numerical value represented by this control.
        label (str): The label associated with the input. (default: None)
        step (dynamic(int|float)): The amount by which the value is incremented or decremented when the user clicks one of the arrow buttons. (default: 1)
        step_multiplier (dynamic(int|float)): A factor that multiplies *step* when the user presses the Shift key while clicking one of the arrow buttons. (default: 10)
        min (dynamic(int|float)): The minimum value to accept for this input.
        max (dynamic(int|float)): The maximum value to accept for this input.
        change_delay (int): Minimum time between triggering two calls to the on\_change callback.The default value is defined at the application configuration level by the **change\_delay** configuration option. if None, the delay is set to 300 ms.If set to \-1, the input change is triggered only when the user presses the Enter key. (default: *App config*)
        on_action (Callback): Name of a function that is triggered when a specific key is pressed.The parameters of that function are all optional:
         * state (`State^`): the state instance.
        * id (str): the identifier of the input.
        * payload (dict): the details on this callback's invocation.
         This dictionary has the following keys:
                + action: the name of the action that triggered this callback.
                + args (list):
                        - key name
                        - variable name
                        - current value

        action_keys (str): Semicolon (';')\-separated list of supported key names.Authorized values are Enter, Escape, F1, F2, F3, F4, F5, F6, F7, F8, F9, F10, F11, F12\. (default: "Enter")
        on_change (Callback): The name of a function that is triggered when the value is updated.The parameters of that function are all optional:
         * state (`State^`): the state instance.
        * var\_name (str): the variable name.
        * value (any): the new value.

        propagate (bool): Allows the control's main value to be automatically propagated.The default value is defined at the application configuration level.If True, any change to the control's value is immediately reflected in the bound application variable. (default: *App config*)
        active (dynamic(bool)): Indicates if this component is active.An inactive component allows no user interaction. (default: True)
        id (str): The identifier that will be assigned to the rendered HTML component.
        properties (dict[str, any]): Bound to a dictionary that contains additional properties for this element.
        class_name (dynamic(str)): The list of CSS class names that will be associated with the generated HTML Element.These class names will be added to the default `taipy-<element_type>`.
        hover_text (dynamic(str)): The information that is displayed when the user hovers over this element.
        """
        ...

class slider(_Control):
    _ELEMENT_NAME: str
    def __init__(
        self,
        value=...,
        min=...,
        max=...,
        step=...,
        text_anchor=...,
        labels=...,
        continuous=...,
        change_delay=...,
        width=...,
        height=...,
        orientation=...,
        lov=...,
        adapter=...,
        type=...,
        value_by_id=...,
        on_change=...,
        propagate=...,
        active=...,
        id=...,
        properties=...,
        class_name=...,
        hover_text=...,
    ) -> None:
        """### Arguments:
        value (dynamic(int|float|int[]|float[]|str|str[])): The value that is set for this slider.If this slider is based on a *lov* then this property can be set to the lov element.This value can also hold an array of numbers to indicate that the slider reflects a range (within the \[*min*,*max*] domain) defined by several knobs that the user can set independently.If this slider is based on a *lov* then this property can be set to an array of lov elements. The slider is then represented with several knobs, one for each lov value.
        min (int|float): The minimum value.This is ignored when *lov* is defined. (default: 0)
        max (int|float): The maximum value.This is ignored when *lov* is defined. (default: 100)
        step (int|float): The step value: the gap between two consecutive values the slider set. It is a good practice to have (*max*\-*min*) being divisible by *step*.This property is ignored when *lov* is defined. (default: 1)
        text_anchor (str): When the *lov* property is used, this property indicates the location of the label.Possible values are:
         * "bottom"
        * "top"
        * "left"
        * "right"
        * "none" (no label is displayed)
         (default: "bottom")
        labels (bool|dict): The labels for specific points of the slider.If set to True, this slider uses the labels of the *lov* if there are any.If set to a dictionary, the slider uses the dictionary keys as a *lov* key or index, and the associated value as the label.
        continuous (bool): If set to False, the control emits an on\_change notification only when the mouse button is released, otherwise notifications are emitted during the cursor movements.If *lov* is defined, the default value is False. (default: True)
        change_delay (int): Minimum time between triggering two on\_change callbacks.The default value is defined at the application configuration level by the **change\_delay** configuration option. if None or 0, there's no delay. (default: *App config*)
        width (str): The width, in CSS units, of this element. (default: "300px")
        height (str): The height, in CSS units, of this element.It defaults to the *width* value when using the vertical orientation.
        orientation (str): The orientation of this slider.Valid values are "horizontal" or "vertical". (default: "horizontal")
        lov (dict[str, any]): The list of values. See the [section on List of Values](https://docs.taipy.io/en/develop/manuals/userman/gui/viselements/generic/slider/../../binding/#list-of-values) for details.
        adapter (Function): The function that transforms an element of *lov* into a *tuple(id:str, label:str\|Icon)*. (default: \`lambda x: str(x)\`)
        type (str): Must be specified if *lov* contains a non\-specific type of data (ex: dict).*value* must be of that type, *lov* must be an iterable on this type, and the adapter function will receive an object of this type. (default: *Type name of the lov element*)
        value_by_id (bool): If False, the selection value (in *value*) is the selected element in *lov*. If set to True, then *value* is set to the id of the selected element in *lov*. (default: False)
        on_change (Callback): The name of a function that is triggered when the value is updated.The parameters of that function are all optional:
         * state (`State^`): the state instance.
        * var\_name (str): the variable name.
        * value (any): the new value.

        propagate (bool): Allows the control's main value to be automatically propagated.The default value is defined at the application configuration level.If True, any change to the control's value is immediately reflected in the bound application variable. (default: *App config*)
        active (dynamic(bool)): Indicates if this component is active.An inactive component allows no user interaction. (default: True)
        id (str): The identifier that will be assigned to the rendered HTML component.
        properties (dict[str, any]): Bound to a dictionary that contains additional properties for this element.
        class_name (dynamic(str)): The list of CSS class names that will be associated with the generated HTML Element.These class names will be added to the default `taipy-<element_type>`.
        hover_text (dynamic(str)): The information that is displayed when the user hovers over this element.
        """
        ...

class toggle(_Control):
    _ELEMENT_NAME: str
    def __init__(
        self,
        value=...,
        theme=...,
        allow_unselect=...,
        unselected_value=...,
        mode=...,
        lov=...,
        adapter=...,
        type=...,
        value_by_id=...,
        on_change=...,
        propagate=...,
        active=...,
        id=...,
        properties=...,
        class_name=...,
        hover_text=...,
    ) -> None:
        """### Arguments:

        theme (bool): If set, this toggle control acts as a way to set the application Theme (dark or light). (default: False)
        allow_unselect (bool): If set, this allows de\-selection and the value is set to unselected\_value. (default: False)
        unselected_value (any): Value assigned to *value* when no item is selected. (default: None)
        mode (str): Define the way the toggle is displayed:* "theme": synonym for setting the \*theme\* property to True

        lov (dict[str, any]): The list of values. See the [section on List of Values](https://docs.taipy.io/en/develop/manuals/userman/gui/viselements/generic/toggle/../../binding/#list-of-values) for details.
        adapter (Function): The function that transforms an element of *lov* into a *tuple(id:str, label:str\|Icon)*. (default: \`lambda x: str(x)\`)
        type (str): Must be specified if *lov* contains a non\-specific type of data (ex: dict).*value* must be of that type, *lov* must be an iterable on this type, and the adapter function will receive an object of this type. (default: *Type name of the lov element*)
        value_by_id (bool): If False, the selection value (in *value*) is the selected element in *lov*. If set to True, then *value* is set to the id of the selected element in *lov*. (default: False)
        on_change (Callback): The name of a function that is triggered when the value is updated.The parameters of that function are all optional:
         * state (`State^`): the state instance.
        * var\_name (str): the variable name.
        * value (any): the new value.

        propagate (bool): Allows the control's main value to be automatically propagated.The default value is defined at the application configuration level.If True, any change to the control's value is immediately reflected in the bound application variable. (default: *App config*)
        active (dynamic(bool)): Indicates if this component is active.An inactive component allows no user interaction. (default: True)
        id (str): The identifier that will be assigned to the rendered HTML component.
        properties (dict[str, any]): Bound to a dictionary that contains additional properties for this element.
        class_name (dynamic(str)): The list of CSS class names that will be associated with the generated HTML Element.These class names will be added to the default `taipy-<element_type>`.
        hover_text (dynamic(str)): The information that is displayed when the user hovers over this element.
        """
        ...

class date(_Control):
    _ELEMENT_NAME: str
    def __init__(
        self,
        date=...,
        with_time=...,
        format=...,
        editable=...,
        label=...,
        min=...,
        max=...,
        on_change=...,
        propagate=...,
        active=...,
        id=...,
        properties=...,
        class_name=...,
        hover_text=...,
    ) -> None:
        """### Arguments:
        date (dynamic(datetime)): The date that this control represents and can modify.It is typically bound to a `datetime` object.
        with_time (bool): Whether or not to show the time part of the date. (default: False)
        format (str): The format to apply to the value.See below.
        editable (dynamic(bool)): Shows the date as a formatted string if not editable. (default: True)
        label (str): The label associated with the input.
        min (dynamic(datetime)): The minimum date to accept for this input.
        max (dynamic(datetime)): The maximum date to accept for this input.
        on_change (Callback): The name of a function that is triggered when the value is updated.The parameters of that function are all optional:
         * state (`State^`): the state instance.
        * var\_name (str): the variable name.
        * value (any): the new value.

        propagate (bool): Allows the control's main value to be automatically propagated.The default value is defined at the application configuration level.If True, any change to the control's value is immediately reflected in the bound application variable. (default: *App config*)
        active (dynamic(bool)): Indicates if this component is active.An inactive component allows no user interaction. (default: True)
        id (str): The identifier that will be assigned to the rendered HTML component.
        properties (dict[str, any]): Bound to a dictionary that contains additional properties for this element.
        class_name (dynamic(str)): The list of CSS class names that will be associated with the generated HTML Element.These class names will be added to the default `taipy-<element_type>`.
        hover_text (dynamic(str)): The information that is displayed when the user hovers over this element.
        """
        ...

class date_range(_Control):
    _ELEMENT_NAME: str
    def __init__(
        self,
        dates=...,
        with_time=...,
        format=...,
        editable=...,
        label_start=...,
        label_end=...,
        on_change=...,
        propagate=...,
        active=...,
        id=...,
        properties=...,
        class_name=...,
        hover_text=...,
    ) -> None:
        """### Arguments:
        dates (dynamic(list(datetime))): The dates that this control represents and can modify.It is typically bound to a list of two `datetime` object.
        with_time (bool): Whether or not to show the time part of the date. (default: False)
        format (str): The format to apply to the value.See below.
        editable (dynamic(bool)): Shows the date as a formatted string if not editable. (default: True)
        label_start (str): The label associated with the first input.
        label_end (str): The label associated with the second input.
        on_change (Callback): The name of a function that is triggered when the value is updated.The parameters of that function are all optional:
         * state (`State^`): the state instance.
        * var\_name (str): the variable name.
        * value (any): the new value.

        propagate (bool): Allows the control's main value to be automatically propagated.The default value is defined at the application configuration level.If True, any change to the control's value is immediately reflected in the bound application variable. (default: *App config*)
        active (dynamic(bool)): Indicates if this component is active.An inactive component allows no user interaction. (default: True)
        id (str): The identifier that will be assigned to the rendered HTML component.
        properties (dict[str, any]): Bound to a dictionary that contains additional properties for this element.
        class_name (dynamic(str)): The list of CSS class names that will be associated with the generated HTML Element.These class names will be added to the default `taipy-<element_type>`.
        hover_text (dynamic(str)): The information that is displayed when the user hovers over this element.
        """
        ...

class chart(_Control):
    _ELEMENT_NAME: str
    def __init__(
        self,
        data=...,
        type=...,
        mode=...,
        x=...,
        y=...,
        z=...,
        lon=...,
        lat=...,
        r=...,
        theta=...,
        high=...,
        low=...,
        open=...,
        close=...,
        measure=...,
        locations=...,
        values=...,
        labels=...,
        parents=...,
        text=...,
        base=...,
        title=...,
        render=...,
        on_range_change=...,
        columns=...,
        label=...,
        name=...,
        selected=...,
        color=...,
        selected_color=...,
        marker=...,
        line=...,
        selected_marker=...,
        layout=...,
        plot_config=...,
        options=...,
        orientation=...,
        text_anchor=...,
        xaxis=...,
        yaxis=...,
        width=...,
        height=...,
        template=...,
        decimator=...,
        rebuild=...,
        figure=...,
        on_change=...,
        propagate=...,
        active=...,
        id=...,
        properties=...,
        class_name=...,
        hover_text=...,
    ) -> None:
        """### Arguments:
        data (dynamic(any)): The data object bound to this chart control.See the section on the [*data* property](https://docs.taipy.io/en/develop/manuals/userman/gui/viselements/generic/chart/#the-data-property) below for details.
        type (indexed(str)): Chart type.See the Plotly [chart type](https://plotly.com/javascript/reference/) documentation for details. (default: scatter)
        mode (indexed(str)): Chart mode.See the Plotly [chart mode](https://plotly.com/javascript/reference/scatter/#scatter-mode) documentation for details. (default: lines\+markers)
        x (indexed(str)): Column name for the *x* axis.
        y (indexed(str)): Column name for the *y* axis.
        z (indexed(str)): Column name for the *z* axis.
        lon (indexed(str)): Column name for the *longitude* value, for 'scattergeo' charts. See [Plotly Map traces](https://plotly.com/javascript/reference/scattergeo/#scattergeo-lon).
        lat (indexed(str)): Column name for the *latitude* value, for 'scattergeo' charts. See [Plotly Map traces](https://plotly.com/javascript/reference/scattergeo/#scattergeo-lat).
        r (indexed(str)): Column name for the *r* value, for 'scatterpolar' charts. See [Plotly Polar charts](https://plotly.com/javascript/polar-chart/).
        theta (indexed(str)): Column name for the *theta* value, for 'scatterpolar' charts. See [Plotly Polar charts](https://plotly.com/javascript/polar-chart/).
        high (indexed(str)): Column name for the *high* value, for 'candlestick' charts. See [Plotly Candlestick charts](https://plotly.com/javascript/reference/candlestick/#candlestick-high).
        low (indexed(str)): Column name for the *low* value, for 'candlestick' charts. See [Ploty Candlestick charts](https://plotly.com/javascript/reference/candlestick/#candlestick-low).
        open (indexed(str)): Column name for the *open* value, for 'candlestick' charts. See [Plotly Candlestick charts](https://plotly.com/javascript/reference/candlestick/#candlestick-open).
        close (indexed(str)): Column name for the *close* value, for 'candlestick' charts. See [Plotly Candlestick charts](https://plotly.com/javascript/reference/candlestick/#candlestick-close).
        measure (indexed(str)): Column name for the *measure* value, for 'waterfall' charts. See [Plotly Waterfall charts](https://plotly.com/javascript/reference/waterfall/#waterfall-measure).
        locations (indexed(str)): Column name for the *locations* value. See [Plotly Choropleth maps](https://plotly.com/javascript/choropleth-maps/).
        values (indexed(str)): Column name for the *values* value. See [Plotly Pie charts](https://plotly.com/javascript/reference/pie/#pie-values) or [Plotly Funnel Area charts](https://plotly.com/javascript/reference/funnelarea/#funnelarea-values).
        labels (indexed(str)): Column name for the *labels* value. See [Plotly Pie charts](https://plotly.com/javascript/reference/pie/#pie-labels).
        parents (indexed(str)): Column name for the *parents* value. See [Plotly Treemap charts](https://plotly.com/javascript/reference/treemap/#treemap-parents).
        text (indexed(str)): Column name for the text associated to the point for the indicated trace.This is meaningful only when *mode* has the *text* option.
        base (indexed(str)): Column name for the *base* value. Used in bar charts only.See the Plotly [bar chart base](https://plotly.com/javascript/reference/bar/#bar-base) documentation for details."
        title (str): The title of this chart control.
        render (dynamic(bool)): If True, this chart is visible on the page. (default: True)
        on_range_change (Callback): The callback function that is invoked when the visible part of the x axis changes.The function receives three parameters:
         * state (`State^`): the state instance.
        * id (optional\[str]): the identifier of the chart control.
        * payload (dict\[str, any]): the full details on this callback's invocation, as emitted by [Plotly](https://plotly.com/javascript/plotlyjs-events/#update-data).

        columns (str|list[str]|dict[str, dict[str, str]]): The list of column names
         * str: ;\-separated list of column names
        * list\[str]: list of names
        * dict: {"column\_name": {format: "format", index: 1}} if index is specified, it represents the display order of the columns.
         If not, the list order defines the index
         (default: *All columns*)
        label (indexed(str)): The label for the indicated trace.This is used when the mouse hovers over a trace.
        name (indexed(str)): The name of the indicated trace.
        selected (indexed(dynamic(list[int]|str))): The list of the selected point indices .
        color (indexed(str)): The color of the indicated trace (or a column name for scattered).
        selected_color (indexed(str)): The color of the selected points for the indicated trace.
        marker (indexed(dict[str, any])): The type of markers used for the indicated trace.See [marker](https://plotly.com/javascript/reference/scatter/#scatter-marker) for details.Color, opacity, size and symbol can be column name.
        line (indexed(str|dict[str, any])): The configuration of the line used for the indicated trace.See [line](https://plotly.com/javascript/reference/scatter/#scatter-line) for details.If the value is a string, it must be a dash type or pattern (see [dash style of lines](https://plotly.com/python/reference/scatter/#scatter-line-dash) for details).
        selected_marker (indexed(dict[str, any])): The type of markers used for selected points in the indicated trace.See [selected marker for details.](https://plotly.com/javascript/reference/scatter/#scatter-selected-marker)
        layout (dynamic(dict[str, any])): The *plotly.js* compatible [layout object](https://plotly.com/javascript/reference/layout/).
        plot_config (dict[str, any]): The *plotly.js* compatible  [configuration options object](https://plotly.com/javascript/configuration-options/).
        options (indexed(dict[str, any])): The *plotly.js* compatible [data object where dynamic data will be overridden.](https://plotly.com/javascript/reference/).
        orientation (indexed(str)): The orientation of the indicated trace.
        text_anchor (indexed(str)): Position of the text relative to the point.Valid values are: *top*, *bottom*, *left*, and *right*.
        xaxis (indexed(str)): The *x* axis identifier for the indicated trace.
        yaxis (indexed(str)): The *y* axis identifier for the indicated trace.
        width (str|int|float): The width, in CSS units, of this element. (default: "100%")
        height (str|int|float): The height, in CSS units, of this element.
        template (dict): The Plotly [layout template](https://plotly.com/javascript/layout-template/).
        decimator (indexed(taipy.gui.data.Decimator)): A decimator instance for the indicated trace that will reduce the size of the data being sent back and forth.If defined as indexed, it will impact only the indicated trace; if not, it will apply only the first trace.
        rebuild (dynamic(bool)): Allows dynamic config refresh if set to True. (default: False)
        figure (dynamic(plotly.graph_objects.Figure)): A figure as produced by plotly.
        on_change (Callback): The name of a function that is triggered when the value is updated.The parameters of that function are all optional:
         * state (`State^`): the state instance.
        * var\_name (str): the variable name.
        * value (any): the new value.

        propagate (bool): Allows the control's main value to be automatically propagated.The default value is defined at the application configuration level.If True, any change to the control's value is immediately reflected in the bound application variable. (default: *App config*)
        active (dynamic(bool)): Indicates if this component is active.An inactive component allows no user interaction. (default: True)
        id (str): The identifier that will be assigned to the rendered HTML component.
        properties (dict[str, any]): Bound to a dictionary that contains additional properties for this element.
        class_name (dynamic(str)): The list of CSS class names that will be associated with the generated HTML Element.These class names will be added to the default `taipy-<element_type>`.
        hover_text (dynamic(str)): The information that is displayed when the user hovers over this element.
        """
        ...

class table(_Control):
    _ELEMENT_NAME: str
    def __init__(
        self,
        data=...,
        page_size=...,
        allow_all_rows=...,
        show_all=...,
        auto_loading=...,
        selected=...,
        page_size_options=...,
        columns=...,
        date_format=...,
        number_format=...,
        style=...,
        tooltip=...,
        width=...,
        height=...,
        filter=...,
        nan_value=...,
        editable=...,
        on_edit=...,
        on_delete=...,
        on_add=...,
        on_action=...,
        size=...,
        rebuild=...,
        downloadable=...,
        on_compare=...,
        active=...,
        id=...,
        properties=...,
        class_name=...,
        hover_text=...,
    ) -> None:
        """### Arguments:
        data (dynamic(any)): The data to be represented in this table. This property can be indexed to define other data for comparison.
        page_size (int): For a paginated table, the number of visible rows. (default: 100)
        allow_all_rows (bool): For a paginated table, adds an option to show all the rows. (default: False)
        show_all (bool): For a paginated table, show all the rows. (default: False)
        auto_loading (bool): If True, the data will be loaded on demand. (default: False)
        selected (list[int]|str): The list of the indices of the rows to be displayed as selected.
        page_size_options (list[int]|str): The list of available page sizes that users can choose from. (default: \[50, 100, 500])
        columns (str|list[str]|dict[str, dict[str, str|int]]): The list of the column names to display.
         * str: Semicolon (';')\-separated list of column names.
        * list\[str]: The list of column names.
        * dict: A dictionary with entries matching: {"col name": {format: "format", index: 1}}.
         if *index* is specified, it represents the display order of the columns.
         If *index* is not specified, the list order defines the index.
         If *format* is specified, it is used for numbers or dates.
         (default: *shows all columns when empty*)
        date_format (str): The date format used for all date columns when the format is not specifically defined. (default: "MM/dd/yyyy")
        number_format (str): The number format used for all number columns when the format is not specifically defined.
        style (str): Allows the styling of table lines.See [below](https://docs.taipy.io/en/develop/manuals/userman/gui/viselements/generic/table/#dynamic-styling) for details.
        tooltip (str): The name of the function that must return a tooltip text for a cell.See [below](https://docs.taipy.io/en/develop/manuals/userman/gui/viselements/generic/table/#cell-tooltips) for details.
        width (str): The width, in CSS units, of this table control. (default: "100%")
        height (str): The height, in CSS units, of this table control. (default: "80vh")
        filter (bool): Indicates, if True, that all columns can be filtered. (default: False)
        nan_value (str): The replacement text for NaN (not\-a\-number) values. (default: "")
        editable (dynamic(bool)): Indicates, if True, that all columns can be edited. (default: False)
        on_edit (Callback): TODO: Default implementation and False value. The name of a function that is triggered when a cell edition is validated.All parameters of that function are optional:
         * state (`State^`): the state instance.
        * var\_name (str): the name of the tabular data variable.
        * payload (dict): the details on this callback's invocation.
         This dictionary has the following keys:
                + index (int): the row index.
                + col (str): the column name.
                + value (any): the new cell value cast to the type of the column.
                + user\_value (str): the new cell value, as it was provided by the user.
                + tz (str): the timezone if the column type is date.

        If this property is not set, the user cannot edit cells.
        on_delete (Callback): TODO: Default implementation and False value. The name of a function that is triggered when a row is deleted.All parameters of that function are optional:
         * state (`State^`): the state instance.
        * var\_name (str): the name of the tabular data variable.
        * payload (dict): the details on this callback's invocation.
         This dictionary has the following keys:
                + index (int): the row index.

        If this property is not set, the user cannot delete rows.
        on_add (Callback): TODO: Default implementation and False value. The name of a function that is triggered when the user requests a row to be added.All parameters of that function are optional:
         * state (`State^`): the state instance.
        * var\_name (str): the name of the tabular data variable.
        * payload (dict): the details on this callback's invocation.This dictionary has the following keys:
                + index (int): the row index.

        If this property is not set, the user cannot add rows.
        on_action (Callback): The name of a function that is triggered when the user selects a row.All parameters of that function are optional:
         * state (`State^`): the state instance.
        * var\_name (str): the name of the tabular data variable.
        * payload (dict): the details on this callback's invocation.This dictionary has the following keys:
                + action: the name of the action that triggered this callback.
                + index (int): the row index.
                + col (str): the column name.
                + reason (str): the origin of the action: "click", or "button" if the cell contains a Markdown link syntax.
                + value (str): the \*link value\* indicated in the cell when using a Markdown link syntax (that is, *reason* is set to "button").

        .
        size (str): The size of the rows.Valid values are "small" and "medium". (default: "small")
        rebuild (dynamic(bool)): If set to True, this allows to dynamically refresh the columns. (default: False)
        downloadable (boolean): If True, a clickable icon is shown so the user can download the data as CSV.
        on_compare (Callback): A data comparison function that would return a structure that identifies the differences between the different data passed as name. The default implementation compares the default data with the data\[1] value.
        active (dynamic(bool)): Indicates if this component is active.An inactive component allows no user interaction. (default: True)
        id (str): The identifier that will be assigned to the rendered HTML component.
        properties (dict[str, any]): Bound to a dictionary that contains additional properties for this element.
        class_name (dynamic(str)): The list of CSS class names that will be associated with the generated HTML Element.These class names will be added to the default `taipy-<element_type>`.
        hover_text (dynamic(str)): The information that is displayed when the user hovers over this element.
        """
        ...

class selector(_Control):
    _ELEMENT_NAME: str
    def __init__(
        self,
        value=...,
        label=...,
        mode=...,
        dropdown=...,
        multiple=...,
        filter=...,
        width=...,
        height=...,
        lov=...,
        adapter=...,
        type=...,
        value_by_id=...,
        on_change=...,
        propagate=...,
        active=...,
        id=...,
        properties=...,
        class_name=...,
        hover_text=...,
    ) -> None:
        """### Arguments:
        value (dynamic(any)): Bound to the selection value.
        label (str): The label associated with the selector when in dropdown mode. (default: None)
        mode (str): Define the way the selector is displayed:* "radio": list of radio buttons
        * "check": list of check buttons
        * any other value: selector as usual.

        dropdown (bool): If True, the list of items is shown in a dropdown menu.You cannot use the filter in that situation. (default: False)
        multiple (bool): If True, the user can select multiple items. (default: False)
        filter (bool): If True, this control is combined with a filter input area. (default: False)
        width (str|int): The width, in CSS units, of this element. (default: "360px")
        height (str|int): The height, in CSS units, of this element.
        lov (dict[str, any]): The list of values. See the [section on List of Values](https://docs.taipy.io/en/develop/manuals/userman/gui/viselements/generic/selector/../../binding/#list-of-values) for details.
        adapter (Function): The function that transforms an element of *lov* into a *tuple(id:str, label:str\|Icon)*. (default: \`lambda x: str(x)\`)
        type (str): Must be specified if *lov* contains a non\-specific type of data (ex: dict).*value* must be of that type, *lov* must be an iterable on this type, and the adapter function will receive an object of this type. (default: *Type name of the lov element*)
        value_by_id (bool): If False, the selection value (in *value*) is the selected element in *lov*. If set to True, then *value* is set to the id of the selected element in *lov*. (default: False)
        on_change (Callback): The name of a function that is triggered when the value is updated.The parameters of that function are all optional:
         * state (`State^`): the state instance.
        * var\_name (str): the variable name.
        * value (any): the new value.

        propagate (bool): Allows the control's main value to be automatically propagated.The default value is defined at the application configuration level.If True, any change to the control's value is immediately reflected in the bound application variable. (default: *App config*)
        active (dynamic(bool)): Indicates if this component is active.An inactive component allows no user interaction. (default: True)
        id (str): The identifier that will be assigned to the rendered HTML component.
        properties (dict[str, any]): Bound to a dictionary that contains additional properties for this element.
        class_name (dynamic(str)): The list of CSS class names that will be associated with the generated HTML Element.These class names will be added to the default `taipy-<element_type>`.
        hover_text (dynamic(str)): The information that is displayed when the user hovers over this element.
        """
        ...

class file_download(_Control):
    _ELEMENT_NAME: str
    def __init__(
        self,
        content=...,
        label=...,
        on_action=...,
        auto=...,
        render=...,
        bypass_preview=...,
        name=...,
        active=...,
        id=...,
        properties=...,
        class_name=...,
        hover_text=...,
    ) -> None:
        """### Arguments:
        content (dynamic(path|file|URL|ReadableBuffer|None)): The content to transfer.If this is a string, a URL, or a file, then the content is read from this source.If a readable buffer is provided (such as an array of bytes...), and to prevent the bandwidth from being consumed too much, the way the data is transferred depends on the *data\_url\_max\_size* parameter of the application configuration (which is set to 50kB by default):
         * If the buffer size is smaller than this setting, then the raw content is generated as a data URL, encoded using base64 (i.e. `"data:<mimetype>;base64,<data>"`).
        * If the buffer size exceeds this setting, then it is transferred through a temporary file.

        If this property is set to None, that indicates that dynamic content is generated. Please take a look at the examples below for details on dynamic generation.
        label (dynamic(str)): The label of the button.
        on_action (Callback): The name of a function that is triggered when the download is terminated (or on user action if *content* is None).All the parameters of that function are optional:
         * state (`State^`): the state instance.
        * id (optional\[str]): the identifier of the button.
        * payload (dict): the details on this callback's invocation.
         This dictionary has two keys:
                + action: the name of the action that triggered this callback.
                + args: A list of two elements: *args\[0]* reflects the *name* property and *args\[1]* holds the file URL.

        auto (bool): If True, the download starts as soon as the page is loaded. (default: False)
        render (dynamic(bool)): If True, the control is displayed.If False, the control is not displayed. (default: True)
        bypass_preview (bool): If False, allows the browser to try to show the content in a different tab.The file download is always performed. (default: True)
        name (str): A name proposition for the file to save, that the user can change.
        active (dynamic(bool)): Indicates if this component is active.An inactive component allows no user interaction. (default: True)
        id (str): The identifier that will be assigned to the rendered HTML component.
        properties (dict[str, any]): Bound to a dictionary that contains additional properties for this element.
        class_name (dynamic(str)): The list of CSS class names that will be associated with the generated HTML Element.These class names will be added to the default `taipy-<element_type>`.
        hover_text (dynamic(str)): The information that is displayed when the user hovers over this element.
        """
        ...

class file_selector(_Control):
    _ELEMENT_NAME: str
    def __init__(
        self,
        content=...,
        label=...,
        on_action=...,
        multiple=...,
        extensions=...,
        drop_message=...,
        notify=...,
        active=...,
        id=...,
        properties=...,
        class_name=...,
        hover_text=...,
    ) -> None:
        """### Arguments:
        content (dynamic(str)): The path or the list of paths of the uploaded files.
        label (str): The label of the button.
        on_action (Callback): The name of the function that will be triggered.All the parameters of that function are optional:
         * state (`State^`): the state instance.
        * id (optional\[str]): the identifier of the button.
        * payload (dict): a dictionary that contains the key "action" set to the name of the action that triggered this callback.

        multiple (bool): If set to True, multiple files can be uploaded. (default: False)
        extensions (str): The list of file extensions that can be uploaded. (default: ".csv,.xlsx")
        drop_message (str): The message that is displayed when the user drags a file above the button. (default: "Drop here to Upload")
        notify (bool): If set to False, the user won't be notified of upload finish. (default: True)
        active (dynamic(bool)): Indicates if this component is active.An inactive component allows no user interaction. (default: True)
        id (str): The identifier that will be assigned to the rendered HTML component.
        properties (dict[str, any]): Bound to a dictionary that contains additional properties for this element.
        class_name (dynamic(str)): The list of CSS class names that will be associated with the generated HTML Element.These class names will be added to the default `taipy-<element_type>`.
        hover_text (dynamic(str)): The information that is displayed when the user hovers over this element.
        """
        ...

class image(_Control):
    _ELEMENT_NAME: str
    def __init__(
        self,
        content=...,
        label=...,
        on_action=...,
        width=...,
        height=...,
        active=...,
        id=...,
        properties=...,
        class_name=...,
        hover_text=...,
    ) -> None:
        """### Arguments:
        content (dynamic(path|URL|file|ReadableBuffer)): The image source.If a buffer is provided (string, array of bytes...), and in order to prevent the bandwidth to be consumed too much, the way the image data is transferred depends on the *data\_url\_max\_size* parameter of the application configuration (which is set to 50kB by default):
         * If the size of the buffer is smaller than this setting, then the raw content is generated as a
         data URL, encoded using base64 (i.e. `"data:<mimetype>;base64,<data>"`).
        * If the size of the buffer is greater than this setting, then it is transferred through a temporary
         file.

        label (dynamic(str)): The label for this image.
        on_action (Callback): The name of a function that is triggered when the user clicks on the image.All the parameters of that function are optional:
         * state (`State^`): the state instance.
        * id (optional\[str]): the identifier of the button.
        * payload (dict): a dictionary that contains the key "action" set to the name of the action that triggered this callback.

        width (str|int|float): The width, in CSS units, of this element. (default: "300px")
        height (str|int|float): The height, in CSS units, of this element.
        active (dynamic(bool)): Indicates if this component is active.An inactive component allows no user interaction. (default: True)
        id (str): The identifier that will be assigned to the rendered HTML component.
        properties (dict[str, any]): Bound to a dictionary that contains additional properties for this element.
        class_name (dynamic(str)): The list of CSS class names that will be associated with the generated HTML Element.These class names will be added to the default `taipy-<element_type>`.
        hover_text (dynamic(str)): The information that is displayed when the user hovers over this element.
        """
        ...

class metric(_Control):
    _ELEMENT_NAME: str
    def __init__(
        self,
        value=...,
        type=...,
        title=...,
        min=...,
        max=...,
        delta=...,
        delta_color=...,
        negative_delta_color=...,
        threshold=...,
        show_value=...,
        format=...,
        delta_format=...,
        color_map=...,
        width=...,
        height=...,
        template=...,
        id=...,
        properties=...,
        class_name=...,
        hover_text=...,
    ) -> None:
        """### Arguments:
        value (dynamic(int|float)): The value to display.
        type (str): The type of the gauge.Possible values are:
         * "none"
        * "circular"
        * "linear"

        . (default: "circular")
        title (str): The title of the metric. (default: None)
        min (int|float): The minimum value of this metric control. (default: 0)
        max (int|float): The maximum value of this metric control. (default: 100)
        delta (dynamic(int|float)): The delta value to display.
        delta_color (str): The color that is used to display the value of the *delta* property. If negative\_delta\_color is set, then this property applies for positive values of delta only. If this property is set to "invert", then delta values are represented with the color used for negative values if delta is positive. The value for delta is also represented with the color used for positive values if delta is negative.
        negative_delta_color (str): If set, this represents the color to be used when the value of *delta* is negative (or positive if *delta\_color* is set to "invert")
        threshold (dynamic(int|float)): The threshold value to display.
        show_value (bool): If set to False, the value is not displayed. (default: True)
        format (str): The format to use when displaying the value.This uses the `printf` syntax.
        delta_format (str): The format to use when displaying the delta value.This uses the `printf` syntax.
        color_map (dict): TODO The color\_map is used to display different colors for different ranges of the metric. The color\_map's keys represent the starting point of each range, which is a number, while the values represent the corresponding color for that range. If the value associated with a key is set to None, it implies that the corresponding range will not be assigned any color.
        width (str|number): The width, in CSS units, of the metric. (default: None)
        height (str|number): The height, in CSS units, of the metric. (default: None)
        template (dict): The Plotly [layout template](https://plotly.com/javascript/layout-template/).
        id (str): The identifier that will be assigned to the rendered HTML component.
        properties (dict[str, any]): Bound to a dictionary that contains additional properties for this element.
        class_name (dynamic(str)): The list of CSS class names that will be associated with the generated HTML Element.These class names will be added to the default `taipy-<element_type>`.
        hover_text (dynamic(str)): The information that is displayed when the user hovers over this element.
        """
        ...

class progress(_Control):
    _ELEMENT_NAME: str
    def __init__(self, value=..., linear=..., show_value=..., render=...) -> None:
        """### Arguments:
        value (dynamic(int)): If set, then the value represents the progress percentage that is shown.TODO \- if unset?
        linear (bool): If set to True, the control displays a linear progress indicator instead of a circular one. (default: False)
        show_value (bool): If set to True, the progress value is shown. (default: False)
        render (dynamic(bool)): If False, this progress indicator is hidden from the page.
        """
        ...

class indicator(_Control):
    _ELEMENT_NAME: str
    def __init__(
        self,
        display=...,
        value=...,
        min=...,
        max=...,
        format=...,
        orientation=...,
        width=...,
        height=...,
        id=...,
        properties=...,
        class_name=...,
    ) -> None:
        """### Arguments:
        display (dynamic(any)): The label to be displayed.This can be formatted if it is a numerical value.
        value (dynamic(int,float)): The location of the label on the \[*min*, *max*] range. (default: *min*)
        min (int|float): The minimum value of the range. (default: 0)
        max (int|float): The maximum value of the range. (default: 100)
        format (str): The format to use when displaying the value.This uses the `printf` syntax.
        orientation (str): The orientation of this slider. (default: "horizontal")
        width (str): The width, in CSS units, of the indicator (used when orientation is horizontal). (default: None)
        height (str): The height, in CSS units, of the indicator (used when orientation is vertical). (default: None)
        id (str): The identifier that will be assigned to the rendered HTML component.
        properties (dict[str, any]): Bound to a dictionary that contains additional properties for this element.
        class_name (dynamic(str)): The list of CSS class names that will be associated with the generated HTML Element.These class names will be added to the default `taipy-<element_type>`.
        """
        ...

class menu(_Control):
    _ELEMENT_NAME: str
    def __init__(
        self,
        lov=...,
        adapter=...,
        type=...,
        label=...,
        inactive_ids=...,
        width=...,
        on_action=...,
        active=...,
    ) -> None:
        """### Arguments:
        lov (dynamic(str|list[str|Icon|any])): The list of menu option values.
        adapter (Function): The function that transforms an element of *lov* into a *tuple(id:str, label:str\|Icon)*. (default: \`"lambda x: str(x)"\`)
        type (str): Must be specified if *lov* contains a non specific type of data (ex: dict).*value* must be of that type, *lov* must be an iterable on this type, and the adapter function will receive an object of this type. (default: *Type of the first lov element*)
        label (str): The title of the menu.
        inactive_ids (dynamic(str|list[str])): Semicolon (';')\-separated list or a list of menu items identifiers that are disabled.
        width (str): The width, in CSS units, of the menu when unfolded.Note that when running on a mobile device, the property *width\[active]* is used instead. (default: "15vw")
        on_action (Callback): The name of the function that is triggered when a menu option is selected.All the parameters of that function are optional:
         * state (`State^`): the state instance.
        * id (str): the identifier of the button.
        * payload (dict): the details on this callback's invocation.
         This dictionary has the following keys:
                + action: the name of the action that triggered this callback.
                + args: List where the first element contains the id of the selected option.

        active (dynamic(bool)): Indicates if this component is active.An inactive component allows no user interaction. (default: True)
        """
        ...

class navbar(_Control):
    _ELEMENT_NAME: str
    def __init__(
        self,
        lov=...,
        active=...,
        id=...,
        properties=...,
        class_name=...,
        hover_text=...,
    ) -> None:
        """### Arguments:
        lov (dict[str, any]): The list of pages. The keys should be:
         * page id (start with "/")
        * or full URL


         The values are labels. See the [section on List of Values](../../binding/#list-of-values) for details.
        active (dynamic(bool)): Indicates if this component is active.An inactive component allows no user interaction. (default: True)
        id (str): The identifier that will be assigned to the rendered HTML component.
        properties (dict[str, any]): Bound to a dictionary that contains additional properties for this element.
        class_name (dynamic(str)): The list of CSS class names that will be associated with the generated HTML Element.These class names will be added to the default `taipy-<element_type>`.
        hover_text (dynamic(str)): The information that is displayed when the user hovers over this element.
        """
        ...

class status(_Control):
    _ELEMENT_NAME: str
    def __init__(
        self,
        value=...,
        without_close=...,
        id=...,
        properties=...,
        class_name=...,
        hover_text=...,
    ) -> None:
        """### Arguments:
        value (tuple|dict|list[dict]|list[tuple]): The different status items to represent.See below.
        without_close (bool): If True, the user cannot remove the status items from the list. (default: False)
        id (str): The identifier that will be assigned to the rendered HTML component.
        properties (dict[str, any]): Bound to a dictionary that contains additional properties for this element.
        class_name (dynamic(str)): The list of CSS class names that will be associated with the generated HTML Element.These class names will be added to the default `taipy-<element_type>`.
        hover_text (dynamic(str)): The information that is displayed when the user hovers over this element.
        """
        ...

class login(_Control):
    _ELEMENT_NAME: str
    def __init__(
        self,
        title=...,
        on_action=...,
        message=...,
        id=...,
        properties=...,
        class_name=...,
        hover_text=...,
    ) -> None:
        """### Arguments:
        title (str): The title of the login dialog. (default: "Log in")
        on_action (Callback): The name of the function that is triggered when the dialog button is pressed.All the parameters of that function are optional:
         * state (`State^`): the state instance.
        * id (str): the identifier of the button.
        * payload (dict): the details on this callback's invocation.
         This dictionary has the following keys:
                + action: the name of the action that triggered this callback.
                + args: a list with three elements:
                        - The first element is the username
                        - The second element is the password
                        - The third element is the current page name



        When the button is pressed, and if this property is not set, Taipy will try to find a callback function called *on\_login()* and invoke it with the parameters listed above.
        message (dynamic(str)): The message shown in the dialog.
        id (str): The identifier that will be assigned to the rendered HTML component.
        properties (dict[str, any]): Bound to a dictionary that contains additional properties for this element.
        class_name (dynamic(str)): The list of CSS class names that will be associated with the generated HTML Element.These class names will be added to the default `taipy-<element_type>`.
        hover_text (dynamic(str)): The information that is displayed when the user hovers over this element.
        """
        ...

class chat(_Control):
    _ELEMENT_NAME: str
    def __init__(
        self,
        messages=...,
        users=...,
        on_action=...,
        with_input=...,
        sender_id=...,
        height=...,
        page_size=...,
        active=...,
        id=...,
        properties=...,
        class_name=...,
        hover_text=...,
    ) -> None:
        """### Arguments:
        messages (dynamic(list[str])): The list of messages. Each element is a list composed of an id, a message and an user identifier.
        users (dynamic(list[str|Icon])): The list of users. See the [section on List of Values](https://docs.taipy.io/en/develop/manuals/userman/gui/viselements/generic/chat/../../binding/#list-of-values) for details.
        on_action (Callback): The name of a function that is triggered when the user enters a new message.All parameters of that function are optional:
         * state (`State^`): the state instance.
        * var\_name (str): the name of the messages variable.
        * payload (dict): the details on this callback's invocation.This dictionary has the following keys:
                + action: the name of the action that triggered this callback.
                + args (list): A list composed of a reason (click or Enter), variable name, message, sender id.

        .
        with_input (dynamic(bool)): If True, the input field is visible. (default: True)
        sender_id (str): The user id associated with the message sent from the input (default: "taipy")
        height (str|int|float): The maximum height, in CSS units, of this element.
        page_size (int): The number of rows retrieved on the frontend. (default: 50)
        active (dynamic(bool)): Indicates if this component is active.An inactive component allows no user interaction. (default: True)
        id (str): The identifier that will be assigned to the rendered HTML component.
        properties (dict[str, any]): Bound to a dictionary that contains additional properties for this element.
        class_name (dynamic(str)): The list of CSS class names that will be associated with the generated HTML Element.These class names will be added to the default `taipy-<element_type>`.
        hover_text (dynamic(str)): The information that is displayed when the user hovers over this element.
        """
        ...

class tree(_Control):
    _ELEMENT_NAME: str
    def __init__(
        self,
        value=...,
        expanded=...,
        multiple=...,
        select_leafs_only=...,
        row_height=...,
        label=...,
        mode=...,
        dropdown=...,
        filter=...,
        width=...,
        height=...,
        lov=...,
        adapter=...,
        type=...,
        value_by_id=...,
        on_change=...,
        propagate=...,
        active=...,
        id=...,
        properties=...,
        class_name=...,
        hover_text=...,
    ) -> None:
        """### Arguments:
        value (dynamic(any)): Bound to the selection value.
        expanded (dynamic(bool|str[])): If Boolean and False, only one node can be expanded at one given level. Otherwise this should be set to an array of the node identifiers that need to be expanded. (default: True)
        multiple (bool): If True, the user can select multiple items by holding the `Ctrl` key while clicking on items. (default: False)
        select_leafs_only (bool): If True, the user can only select leaf nodes. (default: False)
        row_height (str): The height, in CSS units, of each row.
        label (str): The label associated with the selector when in dropdown mode. (default: None)
        mode (str): Define the way the selector is displayed:* "radio": list of radio buttons
        * "check": list of check buttons
        * any other value: selector as usual.

        dropdown (bool): If True, the list of items is shown in a dropdown menu.You cannot use the filter in that situation. (default: False)
        filter (bool): If True, this control is combined with a filter input area. (default: False)
        width (str|int): The width, in CSS units, of this element. (default: "360px")
        height (str|int): The height, in CSS units, of this element.
        lov (dict[str, any]): The list of values. See the [section on List of Values](https://docs.taipy.io/en/develop/manuals/userman/gui/viselements/generic/tree/../../binding/#list-of-values) for details.
        adapter (Function): The function that transforms an element of *lov* into a *tuple(id:str, label:str\|Icon)*. (default: \`lambda x: str(x)\`)
        type (str): Must be specified if *lov* contains a non\-specific type of data (ex: dict).*value* must be of that type, *lov* must be an iterable on this type, and the adapter function will receive an object of this type. (default: *Type name of the lov element*)
        value_by_id (bool): If False, the selection value (in *value*) is the selected element in *lov*. If set to True, then *value* is set to the id of the selected element in *lov*. (default: False)
        on_change (Callback): The name of a function that is triggered when the value is updated.The parameters of that function are all optional:
         * state (`State^`): the state instance.
        * var\_name (str): the variable name.
        * value (any): the new value.

        propagate (bool): Allows the control's main value to be automatically propagated.The default value is defined at the application configuration level.If True, any change to the control's value is immediately reflected in the bound application variable. (default: *App config*)
        active (dynamic(bool)): Indicates if this component is active.An inactive component allows no user interaction. (default: True)
        id (str): The identifier that will be assigned to the rendered HTML component.
        properties (dict[str, any]): Bound to a dictionary that contains additional properties for this element.
        class_name (dynamic(str)): The list of CSS class names that will be associated with the generated HTML Element.These class names will be added to the default `taipy-<element_type>`.
        hover_text (dynamic(str)): The information that is displayed when the user hovers over this element.
        """
        ...

class part(_Block):
    _ELEMENT_NAME: str
    def __init__(
        self,
        render=...,
        class_name=...,
        page=...,
        height=...,
        content=...,
        partial=...,
        id=...,
        properties=...,
        hover_text=...,
    ) -> None:
        """### Arguments:
        render (dynamic(bool)): If True, this part is visible on the page.If False, the part is hidden and its content is not displayed. (default: True)
        class_name (dynamic(str)): A list of CSS class names, separated by white spaces, that will be associated with the generated HTML Element.These class names are added to the default `taipy-part`.
        page (dynamic(str)): The page to show as the content of the block (page name if defined or a URL in an *iframe*).This should not be defined if *partial* is set.
        height (dynamic(str)): The height, in CSS units, of this block.
        content (dynamic(any)): The content provided to the part. See the documentation section on content providers.
        partial (Partial): A Partial object that holds the content of the block.This should not be defined if *page* is set.
        id (str): The identifier that will be assigned to the rendered HTML component.
        properties (dict[str, any]): Bound to a dictionary that contains additional properties for this element.
        hover_text (dynamic(str)): The information that is displayed when the user hovers over this element.
        """
        ...

class expandable(_Block):
    _ELEMENT_NAME: str
    def __init__(
        self,
        title=...,
        expanded=...,
        partial=...,
        page=...,
        id=...,
        properties=...,
        class_name=...,
        hover_text=...,
        on_change=...,
    ) -> None:
        """### Arguments:
        title (dynamic(str)): Title of this block element.
        expanded (dynamic(bool)): If True, the block is expanded, and the content is displayed.If False, the block is collapsed and its content is hidden. (default: True)
        partial (Partial): A Partial object that holds the content of the block.This should not be defined if *page* is set.
        page (str): The page name to show as the content of the block.This should not be defined if *partial* is set.
        id (str): The identifier that will be assigned to the rendered HTML component.
        properties (dict[str, any]): Bound to a dictionary that contains additional properties for this element.
        class_name (dynamic(str)): The list of CSS class names that will be associated with the generated HTML Element.These class names will be added to the default `taipy-<element_type>`.
        hover_text (dynamic(str)): The information that is displayed when the user hovers over this element.
        on_change (Callback): The name of a function that is triggered when the value is updated.The parameters of that function are all optional:
         * state (`State^`): the state instance.
        * var\_name (str): the variable name.
        * value (any): the new value.

        """
        ...

class dialog(_Block):
    _ELEMENT_NAME: str
    def __init__(
        self,
        open=...,
        on_action=...,
        close_label=...,
        labels=...,
        width=...,
        height=...,
        partial=...,
        page=...,
        active=...,
        id=...,
        properties=...,
        class_name=...,
        hover_text=...,
    ) -> None:
        """### Arguments:
        open (bool): If True, the dialog is visible. If False, it is hidden. (default: False)
        on_action (Callback): Name of a function triggered when a button is pressed.The parameters of that function are all optional:
         * state (`State^`): the state instance.
        * id (str): the identifier of the dialog.
        * payload (dict): the details on this callback's invocation.This dictionary has the following keys:
                + action: the name of the action that triggered this callback.
                + args: a list where the first element contains the index of the selected label.

        close_label (str): The tooltip of the top\-right close icon button. In the on\_action callback, args will hold \-1\. (default: "Close")
        labels ( str|list[str]): A list of labels to show in a row of buttons at the bottom of the dialog. The index of the button in the list is reported as args in the on\_action callback (that index is \-1 for the *close* icon).
        width (str|int|float): The width, in CSS units, of this dialog.(CSS property)
        height (str|int|float): The height, in CSS units, of this dialog.(CSS property)
        partial (Partial): A Partial object that holds the content of the block.This should not be defined if *page* is set.
        page (str): The page name to show as the content of the block.This should not be defined if *partial* is set.
        active (dynamic(bool)): Indicates if this component is active.An inactive component allows no user interaction. (default: True)
        id (str): The identifier that will be assigned to the rendered HTML component.
        properties (dict[str, any]): Bound to a dictionary that contains additional properties for this element.
        class_name (dynamic(str)): The list of CSS class names that will be associated with the generated HTML Element.These class names will be added to the default `taipy-<element_type>`.
        hover_text (dynamic(str)): The information that is displayed when the user hovers over this element.
        """
        ...

class layout(_Block):
    _ELEMENT_NAME: str
    def __init__(
        self,
        columns=...,
        gap=...,
        id=...,
        properties=...,
        class_name=...,
        hover_text=...,
    ) -> None:
        """### Arguments:
        columns (str): The list of weights for each column.For example, \`"1 2"\` creates a 2 column grid:
         * 1fr
        * 2fr

        The creation of multiple same size columns can be simplified by using the multiply sign eg. "5\*1" is equivalent to "1 1 1 1 1". (default: "1 1")
        gap (str): The size of the gap between the columns. (default: "0\.5rem")
        id (str): The identifier that will be assigned to the rendered HTML component.
        properties (dict[str, any]): Bound to a dictionary that contains additional properties for this element.
        class_name (dynamic(str)): The list of CSS class names that will be associated with the generated HTML Element.These class names will be added to the default `taipy-<element_type>`.
        hover_text (dynamic(str)): The information that is displayed when the user hovers over this element.
        """
        ...

class pane(_Block):
    _ELEMENT_NAME: str
    def __init__(
        self,
        open=...,
        on_close=...,
        anchor=...,
        width=...,
        height=...,
        persistent=...,
        partial=...,
        page=...,
        on_change=...,
        active=...,
        id=...,
        properties=...,
        class_name=...,
        hover_text=...,
    ) -> None:
        """### Arguments:
        open (dynamic(bool)): If True, this pane is visible on the page.If False, the pane is hidden. (default: False)
        on_close (Callback): The name of a function that is triggered when this pane is closed (if the user clicks outside of it or presses the Esc key).All parameters of that function are optional:
         * state (`State^`): the state instance.
        * id (optional\[str]): the identifier of the button.

        If this property is not set, no function is called when this pane is closed.
        anchor (str): Anchor side of the pane.Valid values are "left", "right", "top", or "bottom". (default: "left")
        width (str): Width, in CSS units, of this pane.This is used only if *anchor* is "left" or "right". (default: "30vw")
        height (str): Height, in CSS units, of this pane.This is used only if *anchor* is "top" or "bottom". (default: "30vh")
        persistent (bool): If False, the pane covers the page where it appeared and disappears if the user clicks in the page.If True, the pane appears next to the page. Note that the parent section of the pane must have the *flex* display mode set.See below for an example using the `persistent` property. (default: False)
        partial (Partial): A Partial object that holds the content of the block.This should not be defined if *page* is set.
        page (str): The page name to show as the content of the block.This should not be defined if *partial* is set.
        on_change (Callback): The name of a function that is triggered when the value is updated.The parameters of that function are all optional:
         * state (`State^`): the state instance.
        * var\_name (str): the variable name.
        * value (any): the new value.

        active (dynamic(bool)): Indicates if this component is active.An inactive component allows no user interaction. (default: True)
        id (str): The identifier that will be assigned to the rendered HTML component.
        properties (dict[str, any]): Bound to a dictionary that contains additional properties for this element.
        class_name (dynamic(str)): The list of CSS class names that will be associated with the generated HTML Element.These class names will be added to the default `taipy-<element_type>`.
        hover_text (dynamic(str)): The information that is displayed when the user hovers over this element.
        """
        ...
