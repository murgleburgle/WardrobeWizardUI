import reflex as rx
from app.states.dashboard_state import DashboardState


def control_panel() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Server Control",
                class_name=rx.cond(
                    DashboardState.color_scheme == "moonlit_clearing",
                    "text-lg font-semibold text-[#E0E0FF]",
                    "text-lg font-semibold text-[#E6F5E8]",
                ),
            ),
            rx.el.p(
                "Manage the state of the AI enrichment server.",
                class_name=rx.cond(
                    DashboardState.color_scheme == "moonlit_clearing",
                    "text-sm text-[#8B8BBF]",
                    "text-sm text-[#80A886]",
                ),
            ),
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    class_name=rx.match(
                        DashboardState.server_status,
                        ("online", "w-3 h-3 rounded-full bg-green-500 animate-pulse"),
                        ("offline", "w-3 h-3 rounded-full bg-red-500"),
                        ("starting", "w-3 h-3 rounded-full bg-yellow-500 animate-spin"),
                        "w-3 h-3 rounded-full bg-red-500",
                    )
                ),
                rx.el.p(
                    DashboardState.server_status.capitalize(),
                    class_name="text-sm font-medium",
                ),
                class_name="flex items-center gap-2",
            ),
            rx.el.div(
                rx.el.button(
                    "Process All Pending",
                    on_click=DashboardState.process_all_pending,
                    disabled=DashboardState.server_status != "online",
                    class_name=rx.cond(
                        DashboardState.color_scheme == "moonlit_clearing",
                        "text-sm font-semibold px-4 py-2 rounded-lg border border-[#2F2F50] bg-[#1A1A3F] hover:bg-[#2F2F50] transition-colors disabled:opacity-50 disabled:cursor-not-allowed",
                        "text-sm font-semibold px-4 py-2 rounded-lg border border-[#295931] bg-[#15351B] hover:bg-[#295931] transition-colors disabled:opacity-50 disabled:cursor-not-allowed",
                    ),
                ),
                rx.el.button(
                    rx.icon(
                        tag=rx.cond(
                            DashboardState.server_status == "online",
                            "power-off",
                            "power",
                        ),
                        class_name="mr-2 h-4 w-4",
                    ),
                    rx.cond(
                        DashboardState.server_status == "online",
                        "Stop Server",
                        "Start Server",
                    ),
                    on_click=DashboardState.toggle_server_status,
                    class_name=rx.cond(
                        DashboardState.server_status == "online",
                        "flex items-center text-sm font-semibold px-4 py-2 rounded-lg bg-red-500 text-white hover:bg-red-600 transition-colors",
                        rx.cond(
                            DashboardState.color_scheme == "moonlit_clearing",
                            "flex items-center text-sm font-semibold px-4 py-2 rounded-lg bg-purple-600 text-white hover:bg-purple-700 transition-colors",
                            "flex items-center text-sm font-semibold px-4 py-2 rounded-lg bg-green-600 text-white hover:bg-green-700 transition-colors",
                        ),
                    ),
                ),
                class_name="flex items-center gap-3",
            ),
        ),
        class_name=rx.cond(
            DashboardState.color_scheme == "moonlit_clearing",
            "flex flex-col md:flex-row items-start md:items-center justify-between gap-4 p-6 bg-[#1A1A3F] border border-[#2F2F50] rounded-xl shadow-sm",
            "flex flex-col md:flex-row items-start md:items-center justify-between gap-4 p-6 bg-[#15351B] border border-[#295931] rounded-xl shadow-sm",
        ),
    )