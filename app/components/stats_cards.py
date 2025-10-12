import reflex as rx
from app.states.dashboard_state import DashboardState


def stat_card(
    icon: str, title: str, value: rx.Var[str | int], color: str
) -> rx.Component:
    icon_container_class = rx.match(
        color,
        ("green", "p-3 rounded-xl bg-green-500/10 text-green-400"),
        ("yellow", "p-3 rounded-xl bg-yellow-500/10 text-yellow-400"),
        ("red", "p-3 rounded-xl bg-red-500/10 text-red-400"),
        "p-3 rounded-xl bg-gray-500/10 text-gray-400",
    )
    return rx.el.div(
        rx.el.div(
            rx.icon(tag=icon, class_name="w-6 h-6"), class_name=icon_container_class
        ),
        rx.el.div(
            rx.el.p(
                title,
                class_name=rx.cond(
                    DashboardState.color_scheme == "moonlit_clearing",
                    "text-sm font-medium text-[#8B8BBF]",
                    "text-sm font-medium text-[#80A886]",
                ),
            ),
            rx.el.p(value, class_name="text-2xl font-bold"),
            class_name="flex flex-col",
        ),
        class_name=rx.cond(
            DashboardState.color_scheme == "moonlit_clearing",
            "flex items-center gap-4 p-6 bg-[#1A1A3F] border border-[#2F2F50] rounded-xl shadow-sm hover:shadow-lg transition-shadow duration-200",
            "flex items-center gap-4 p-6 bg-[#15351B] border border-[#295931] rounded-xl shadow-sm hover:shadow-lg transition-shadow duration-200",
        ),
    )


def stats_overview() -> rx.Component:
    return rx.el.div(
        stat_card(
            "square_check",
            "Images Processed",
            DashboardState.stats["processed"],
            "green",
        ),
        stat_card("clock", "In Queue", DashboardState.stats["in_queue"], "yellow"),
        stat_card(
            "flag_triangle_right",
            "Processing Errors",
            DashboardState.stats["errors"],
            "red",
        ),
        class_name="grid grid-cols-1 md:grid-cols-3 gap-6",
    )