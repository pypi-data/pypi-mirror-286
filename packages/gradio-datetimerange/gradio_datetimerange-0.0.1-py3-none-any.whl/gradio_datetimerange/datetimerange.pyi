"""gr.DateTime() component."""

from __future__ import annotations

import re
from datetime import datetime, timedelta
from typing import Any, Literal

import pytz
from gradio_client.documentation import document

from gradio.components.base import FormComponent
from gradio.events import Events


class DateTimeRange(DateTime):
    """
    Component to select range of time.
    """

    EVENTS = [
        Events.change,
    ]

    def __init__(
        self,
        value: tuple[float | str | datetime, float | str | datetime] | None = None,
        *,
        include_time: bool = True,
        type: Literal["timestamp", "datetime", "string"] = "timestamp",
        timezone: str | None = None,
        quick_ranges: list[str] | None = None,
        label: str | None = None,
        show_label: bool | None = None,
        info: str | None = None,
        every: float | None = None,
        scale: int | None = None,
        min_width: int = 160,
        visible: bool = True,
        elem_id: str | None = None,
        elem_classes: list[str] | str | None = None,
        render: bool = True,
        key: int | str | None = None,
    ):
        """
        Parameters:
            value: default value for datetime.
            label: The label for this component. Appears above the component and is also used as the header if there are a table of examples for this component. If None and used in a `gr.Interface`, the label will be the name of the parameter this component is assigned to.
            show_label: if True, will display label.
            include_time: If True, the component will include time selection. If False, only date selection will be available.
            type: The type of the value. Can be "timestamp", "datetime", or "string". If "timestamp", the value will be a number representing the start and end date in seconds since epoch. If "datetime", the value will be a datetime object. If "string", the value will be the date entered by the user.
            timezone: The timezone to use for timestamps, such as "US/Pacific" or "Europe/Paris". If None, the timezone will be the local timezone.
            info: additional component description.
            every: If `value` is a callable, run the function 'every' number of seconds while the client connection is open. Has no effect otherwise. The event can be accessed (e.g. to cancel it) via this component's .load_event attribute.
            scale: relative size compared to adjacent Components. For example if Components A and B are in a Row, and A has scale=2, and B has scale=1, A will be twice as wide as B. Should be an integer. scale applies in Rows, and to top-level Components in Blocks where fill_height=True.
            min_width: minimum pixel width, will wrap if not sufficient screen space to satisfy this value. If a certain scale value results in this Component being narrower than min_width, the min_width parameter will be respected first.
            visible: If False, component will be hidden.
            elem_classes: An optional list of strings that are assigned as the classes of this component in the HTML DOM. Can be used for targeting CSS styles.
            render: If False, component will not render be rendered in the Blocks context. Should be used if the intention is to assign event listeners now but render the component later.
            key: if assigned, will be used to assume identity across a re-render. Components that have the same key across a re-render will have their value preserved.
            quick_ranges: List of strings representing quick ranges to display, such as ["30s", "1h", "24h", "7d"]. Set to [] to clear.
        """
        super().__init__(
            every=every,
            scale=scale,
            min_width=min_width,
            visible=visible,
            label=label,
            show_label=show_label,
            info=info,
            elem_id=elem_id,
            elem_classes=elem_classes,
            render=render,
            key=key,
            value=value,
            type=type,
            include_time=include_time,
            timezone=timezone,
        )

        self.quick_ranges = (
            ["15m", "1h", "24h"] if quick_ranges is None else quick_ranges
        )
        self._init_value = None
        if value:
            init_range = self.postprocess(value)
            self._init_value = (self.get_datetime_from_str(init_range[0]).timestamp(), self.get_datetime_from_str(init_range[1]).timestamp()) if value else None

    def preprocess(self, payload: tuple[str, str] | None) -> tuple[str | float | datetime, str | float | datetime] | None:
        """
        Parameters:
            payload: the text entered in the textarea.
        Returns:
            Passes text value as a {str} into the function.
        """
        if payload is None:
            return None
        start, end = super().preprocess(payload[0]), super().preprocess(payload[1])
        if start is None or end is None:
            return None
        return start, end

    def postprocess(self, value: tuple[float | datetime | str, float | datetime | str]  | None) -> tuple[str, str] | None:
        """
        Parameters:
            value: Expects a tuple pair of datetimes.
        Returns:
            A tuple pair of timestamps.
        """
        if value is None:
            return None

        start, end = super().postprocess(value[0]), super().postprocess(value[1])
        if start is None or end is None:
            return None
        return start, end


    def api_info(self) -> dict[str, Any]:
        return {
            "type": {},
            "description": f"Two strings formatted as YYYY-MM-DD{' HH:MM:SS' if self.include_time else ''}",
        }

    def example_payload(self) -> list[str]:
        return ["2020-10-01 05:20:15", "2020-10-01 06:20:15"]

    def example_value(self) -> list[str]:
        return ["2020-10-01 05:20:15", "2020-10-01 06:20:15"]
    
    def bind(self, plots: NativePlot | list[NativePlot]) -> None:
        from gradio.components.native_plot import NativePlot

        if not isinstance(plots, list):
            plots = [plots]
        plot_count = len(plots)

        def reset_range(select: SelectData):
            if select.selected:
                a, b = cast("tuple[float, float]", select.index)
                dt_a, dt_b = datetime.fromtimestamp(a), datetime.fromtimestamp(b)
                return dt_a, dt_b
            else:
                return skip()

        for plot in plots:
            if self._init_value is not None:
                print(self._init_value)
                plot.x_lim = self._init_value
            plot.select(reset_range, None, self, show_api=False)

        def update_plots(domain: tuple[int, int]):
            changes = [
                NativePlot(x_lim=domain)
                for _ in range(plot_count)
            ]
            return changes if len(changes) > 1 else changes[0]

        self.change(update_plots, self, plots, show_api=False)

    
    def change(self,
        fn: Callable | None = None,
        inputs: Block | Sequence[Block] | set[Block] | None = None,
        outputs: Block | Sequence[Block] | None = None,
        api_name: str | None | Literal[False] = None,
        scroll_to_output: bool = False,
        show_progress: Literal["full", "minimal", "hidden"] = "full",
        queue: bool | None = None,
        batch: bool = False,
        max_batch_size: int = 4,
        preprocess: bool = True,
        postprocess: bool = True,
        cancels: dict[str, Any] | list[dict[str, Any]] | None = None,
        every: Timer | float | None = None,
        trigger_mode: Literal["once", "multiple", "always_last"] | None = None,
        js: str | None = None,
        concurrency_limit: int | None | Literal["default"] = "default",
        concurrency_id: str | None = None,
        show_api: bool = True) -> Dependency:
        """
        Parameters:
            fn: the function to call when this event is triggered. Often a machine learning model's prediction function. Each parameter of the function corresponds to one input component, and the function should return a single value or a tuple of values, with each element in the tuple corresponding to one output component.
            inputs: List of gradio.components to use as inputs. If the function takes no inputs, this should be an empty list.
            outputs: List of gradio.components to use as outputs. If the function returns no outputs, this should be an empty list.
            api_name: Defines how the endpoint appears in the API docs. Can be a string, None, or False. If False, the endpoint will not be exposed in the api docs. If set to None, the endpoint will be exposed in the api docs as an unnamed endpoint, although this behavior will be changed in Gradio 4.0. If set to a string, the endpoint will be exposed in the api docs with the given name.
            scroll_to_output: If True, will scroll to output component on completion
            show_progress: If True, will show progress animation while pending
            queue: If True, will place the request on the queue, if the queue has been enabled. If False, will not put this event on the queue, even if the queue has been enabled. If None, will use the queue setting of the gradio app.
            batch: If True, then the function should process a batch of inputs, meaning that it should accept a list of input values for each parameter. The lists should be of equal length (and be up to length `max_batch_size`). The function is then *required* to return a tuple of lists (even if there is only 1 output component), with each list in the tuple corresponding to one output component.
            max_batch_size: Maximum number of inputs to batch together if this is called from the queue (only relevant if batch=True)
            preprocess: If False, will not run preprocessing of component data before running 'fn' (e.g. leaving it as a base64 string if this method is called with the `Image` component).
            postprocess: If False, will not run postprocessing of component data before returning 'fn' output to the browser.
            cancels: A list of other events to cancel when this listener is triggered. For example, setting cancels=[click_event] will cancel the click_event, where click_event is the return value of another components .click method. Functions that have not yet run (or generators that are iterating) will be cancelled, but functions that are currently running will be allowed to finish.
            every: Continously calls `value` to recalculate it if `value` is a function (has no effect otherwise). Can provide a Timer whose tick resets `value`, or a float that provides the regular interval for the reset Timer.
            trigger_mode: If "once" (default for all events except `.change()`) would not allow any submissions while an event is pending. If set to "multiple", unlimited submissions are allowed while pending, and "always_last" (default for `.change()` and `.key_up()` events) would allow a second submission after the pending event is complete.
            js: Optional frontend js method to run before running 'fn'. Input arguments for js method are values of 'inputs' and 'outputs', return should be a list of values for output components.
            concurrency_limit: If set, this is the maximum number of this event that can be running simultaneously. Can be set to None to mean no concurrency_limit (any number of this event can be running simultaneously). Set to "default" to use the default concurrency limit (defined by the `default_concurrency_limit` parameter in `Blocks.queue()`, which itself is 1 by default).
            concurrency_id: If set, this is the id of the concurrency group. Events with the same concurrency_id will be limited by the lowest set concurrency_limit.
            show_api: whether to show this event in the "view API" page of the Gradio app, or in the ".view_api()" method of the Gradio clients. Unlike setting api_name to False, setting show_api to False will still allow downstream apps as well as the Clients to use this event. If fn is None, show_api will automatically be set to False.
        """
        ...
