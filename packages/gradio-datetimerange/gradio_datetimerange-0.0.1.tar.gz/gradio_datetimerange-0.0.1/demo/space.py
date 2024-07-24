
import gradio as gr
from app import demo as app
import os

_docs = {'DateTimeRange': {'description': 'Component to select range of time.', 'members': {'__init__': {'value': {'type': 'tuple[float | str | datetime, float | str | datetime] | None', 'default': 'None', 'description': 'default value for datetime.'}, 'include_time': {'type': 'bool', 'default': 'True', 'description': 'If True, the component will include time selection. If False, only date selection will be available.'}, 'type': {'type': 'Literal["timestamp", "datetime", "string"]', 'default': '"timestamp"', 'description': 'The type of the value. Can be "timestamp", "datetime", or "string". If "timestamp", the value will be a number representing the start and end date in seconds since epoch. If "datetime", the value will be a datetime object. If "string", the value will be the date entered by the user.'}, 'timezone': {'type': 'str | None', 'default': 'None', 'description': 'The timezone to use for timestamps, such as "US/Pacific" or "Europe/Paris". If None, the timezone will be the local timezone.'}, 'quick_ranges': {'type': 'list[str] | None', 'default': 'None', 'description': 'List of strings representing quick ranges to display, such as ["30s", "1h", "24h", "7d"]. Set to [] to clear.'}, 'label': {'type': 'str | None', 'default': 'None', 'description': 'The label for this component. Appears above the component and is also used as the header if there are a table of examples for this component. If None and used in a `gr.Interface`, the label will be the name of the parameter this component is assigned to.'}, 'show_label': {'type': 'bool | None', 'default': 'None', 'description': 'if True, will display label.'}, 'info': {'type': 'str | None', 'default': 'None', 'description': 'additional component description.'}, 'every': {'type': 'float | None', 'default': 'None', 'description': "If `value` is a callable, run the function 'every' number of seconds while the client connection is open. Has no effect otherwise. The event can be accessed (e.g. to cancel it) via this component's .load_event attribute."}, 'scale': {'type': 'int | None', 'default': 'None', 'description': 'relative size compared to adjacent Components. For example if Components A and B are in a Row, and A has scale=2, and B has scale=1, A will be twice as wide as B. Should be an integer. scale applies in Rows, and to top-level Components in Blocks where fill_height=True.'}, 'min_width': {'type': 'int', 'default': '160', 'description': 'minimum pixel width, will wrap if not sufficient screen space to satisfy this value. If a certain scale value results in this Component being narrower than min_width, the min_width parameter will be respected first.'}, 'visible': {'type': 'bool', 'default': 'True', 'description': 'If False, component will be hidden.'}, 'elem_id': {'type': 'str | None', 'default': 'None', 'description': None}, 'elem_classes': {'type': 'list[str] | str | None', 'default': 'None', 'description': 'An optional list of strings that are assigned as the classes of this component in the HTML DOM. Can be used for targeting CSS styles.'}, 'render': {'type': 'bool', 'default': 'True', 'description': 'If False, component will not render be rendered in the Blocks context. Should be used if the intention is to assign event listeners now but render the component later.'}, 'key': {'type': 'int | str | None', 'default': 'None', 'description': 'if assigned, will be used to assume identity across a re-render. Components that have the same key across a re-render will have their value preserved.'}}, 'postprocess': {'value': {'type': 'tuple[float | datetime | str, float | datetime | str] | None', 'description': 'Expects a tuple pair of datetimes.'}}, 'preprocess': {'return': {'type': 'tuple[str | float | datetime, str | float | datetime] | None', 'description': 'Passes text value as a {str} into the function.'}, 'value': None}}, 'events': {'change': {'type': None, 'default': None, 'description': 'Triggered when the value of the DateTimeRange changes either because of user input (e.g. a user types in a textbox) OR because of a function update (e.g. an image receives a value from the output of an event trigger). See `.input()` for a listener that is only triggered by user input.'}}}, '__meta__': {'additional_interfaces': {}, 'user_fn_refs': {'DateTimeRange': []}}}

abs_path = os.path.join(os.path.dirname(__file__), "css.css")

with gr.Blocks(
    css=abs_path,
    theme=gr.themes.Default(
        font_mono=[
            gr.themes.GoogleFont("Inconsolata"),
            "monospace",
        ],
    ),
) as demo:
    gr.Markdown(
"""
# `gradio_datetimerange`

<div style="display: flex; gap: 7px;">
<img alt="Static Badge" src="https://img.shields.io/badge/version%20-%200.0.1%20-%20orange">  
</div>

Component to create time ranges.
""", elem_classes=["md-custom"], header_links=True)
    app.render()
    gr.Markdown(
"""
## Installation

```bash
pip install gradio_datetimerange
```

## Usage

```python

import gradio as gr
from gradio_datetimerange import DateTimeRange
import pandas as pd
from random import randint

temp_sensor_data = pd.DataFrame(
    {
        "time": pd.date_range("2021-01-01", end="2021-01-05", periods=200),
        "temperature": [randint(50 + 10 * (i % 2), 65 + 15 * (i % 2)) for i in range(200)],
        "humidity": [randint(50 + 10 * (i % 2), 65 + 15 * (i % 2)) for i in range(200)],
        "location": ["indoor", "outdoor"] * 100,
    }
)

with gr.Blocks() as demo:
    date = DateTimeRange(["2021-01-01 00:00:00", "2021-01-07 00:00:00"])
    merged_temp_plot = gr.LinePlot(
        temp_sensor_data,
        x="time",
        y="temperature",
    )
    split_temp_plot = gr.LinePlot(
        temp_sensor_data,
        x="time",
        y="temperature",
        color="location",
    )
    with gr.Row():
        humidity_bar_plot = gr.BarPlot(
            temp_sensor_data,
            x="time",
            y="humidity",
            color="location",
            x_bin="1h",
        )
        humidity_scatter_plot = gr.ScatterPlot(
            temp_sensor_data,
            x="time",
            y="humidity",
            color="location",
        )
    
    date.bind([merged_temp_plot, split_temp_plot, humidity_bar_plot, humidity_scatter_plot])


if __name__ == "__main__":
    demo.launch()

```
""", elem_classes=["md-custom"], header_links=True)


    gr.Markdown("""
## `DateTimeRange`

### Initialization
""", elem_classes=["md-custom"], header_links=True)

    gr.ParamViewer(value=_docs["DateTimeRange"]["members"]["__init__"], linkify=[])


    gr.Markdown("### Events")
    gr.ParamViewer(value=_docs["DateTimeRange"]["events"], linkify=['Event'])




    gr.Markdown("""

### User function

The impact on the users predict function varies depending on whether the component is used as an input or output for an event (or both).

- When used as an Input, the component only impacts the input signature of the user function.
- When used as an output, the component only impacts the return signature of the user function.

The code snippet below is accurate in cases where the component is used as both an input and an output.

- **As input:** Is passed, passes text value as a {str} into the function.
- **As output:** Should return, expects a tuple pair of datetimes.

 ```python
def predict(
    value: tuple[str | float | datetime, str | float | datetime] | None
) -> tuple[float | datetime | str, float | datetime | str] | None:
    return value
```
""", elem_classes=["md-custom", "DateTimeRange-user-fn"], header_links=True)




    demo.load(None, js=r"""function() {
    const refs = {};
    const user_fn_refs = {
          DateTimeRange: [], };
    requestAnimationFrame(() => {

        Object.entries(user_fn_refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}-user-fn`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })

        Object.entries(refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })
    })
}

""")

demo.launch()
