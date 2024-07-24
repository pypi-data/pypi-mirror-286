
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
