"""gr.DateTime() component."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal, TYPE_CHECKING, cast

from gradio.components import DateTime
from gradio.events import Events, SelectData, on
from gradio.helpers import skip

if TYPE_CHECKING:
    from gradio.components.native_plot import NativePlot


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

        self.change(update_plots, self, plots, show_api=False)  # type: ignore
