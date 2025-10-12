import reflex as rx
from app.states.dashboard_state import DashboardState


def header() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.button(
                rx.icon(
                    tag="panel-left",
                    class_name=rx.cond(
                        DashboardState.color_scheme == "moonlit_clearing",
                        "text-[#8B8BBF]",
                        "text-[#80A886]",
                    ),
                ),
                on_click=DashboardState.toggle_sidebar,
                class_name=rx.cond(
                    DashboardState.color_scheme == "moonlit_clearing",
                    "p-2 rounded-md hover:bg-[#1A1A3F] transition-colors",
                    "p-2 rounded-md hover:bg-[#15351B] transition-colors",
                ),
            ),
            rx.el.div(
                rx.el.p(
                    "Overview",
                    class_name=rx.cond(
                        DashboardState.color_scheme == "moonlit_clearing",
                        "text-sm text-[#8B8BBF] font-medium",
                        "text-sm text-[#80A886] font-medium",
                    ),
                ),
                rx.el.p("Dashboard", class_name="text-lg font-semibold"),
                class_name="hidden md:block",
            ),
        ),
        rx.el.div(
            rx.el.button(
                rx.icon(tag="search", class_name="mr-2 h-4 w-4"),
                "Search...",
                rx.el.kbd(
                    "⌘K",
                    class_name=rx.cond(
                        DashboardState.color_scheme == "moonlit_clearing",
                        "ml-4 bg-[#2F2F50]/80 p-1 rounded-md text-xs",
                        "ml-4 bg-[#295931]/80 p-1 rounded-md text-xs",
                    ),
                ),
                class_name=rx.cond(
                    DashboardState.color_scheme == "moonlit_clearing",
                    "flex items-center text-sm text-[#8B8BBF] bg-[#1A1A3F]/80 border border-[#2F2F50]/80 px-3 py-1.5 rounded-lg w-40 md:w-64 hover:bg-[#2F2F50]/80 transition-colors",
                    "flex items-center text-sm text-[#80A886] bg-[#15351B]/80 border border-[#295931]/80 px-3 py-1.5 rounded-lg w-40 md:w-64 hover:bg-[#295931]/80 transition-colors",
                ),
            ),
            rx.el.button(
                rx.icon(
                    tag=rx.cond(
                        DashboardState.color_scheme == "moonlit_clearing", "moon", "sun"
                    ),
                    class_name="h-5 w-5",
                ),
                on_click=DashboardState.toggle_color_scheme,
                class_name=rx.cond(
                    DashboardState.color_scheme == "moonlit_clearing",
                    "p-2 rounded-full hover:bg-[#1A1A3F] transition-colors",
                    "p-2 rounded-full hover:bg-[#15351B] transition-colors",
                ),
            ),
            rx.el.button(
                rx.icon(tag="bell", class_name="h-5 w-5"),
                class_name=rx.cond(
                    DashboardState.color_scheme == "moonlit_clearing",
                    "p-2 rounded-full hover:bg-[#1A1A3F] transition-colors",
                    "p-2 rounded-full hover:bg-[#15351B] transition-colors",
                ),
            ),
            class_name="flex items-center gap-2",
        ),
        class_name=rx.cond(
            DashboardState.color_scheme == "moonlit_clearing",
            "sticky top-0 z-10 bg-[#0F0F28]/50 backdrop-blur-sm flex items-center justify-between h-16 px-4 border-b border-[#2F2F50]",
            "sticky top-0 z-10 bg-[#0A1F0D]/50 backdrop-blur-sm flex items-center justify-between h-16 px-4 border-b border-[#295931]",
        ),
    )