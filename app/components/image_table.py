import reflex as rx
from app.states.dashboard_state import DashboardState, Image


def status_badge(status: rx.Var[str]) -> rx.Component:
    base_class = "inline-flex items-center gap-1.5 w-fit rounded-full px-2 py-1 text-xs font-medium"
    color_map = {
        "completed": "bg-green-500/10 text-green-400",
        "processing": "bg-blue-500/10 text-blue-400",
        "pending": "bg-yellow-500/10 text-yellow-400",
        "error": "bg-red-500/10 text-red-400",
    }
    return rx.el.div(
        rx.el.div(
            class_name=rx.match(
                status,
                ("completed", "w-2 h-2 rounded-full bg-green-500"),
                ("processing", "w-2 h-2 rounded-full bg-blue-500 animate-pulse"),
                ("pending", "w-2 h-2 rounded-full bg-yellow-500"),
                ("error", "w-2 h-2 rounded-full bg-red-500"),
                "w-2 h-2 rounded-full bg-gray-500",
            )
        ),
        rx.el.p(status.capitalize()),
        class_name=rx.match(
            status,
            ("completed", f"{base_class} {color_map['completed']}"),
            ("processing", f"{base_class} {color_map['processing']}"),
            ("pending", f"{base_class} {color_map['pending']}"),
            ("error", f"{base_class} {color_map['error']}"),
            f"{base_class} bg-gray-500/10 text-gray-400",
        ),
    )


def skeleton_row() -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                class_name=rx.cond(
                    DashboardState.color_scheme == "moonlit_clearing",
                    "h-5 w-5 bg-[#2F2F50] rounded-md",
                    "h-5 w-5 bg-[#295931] rounded-md",
                )
            ),
            class_name="px-6 py-4",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.div(
                    class_name=rx.cond(
                        DashboardState.color_scheme == "moonlit_clearing",
                        "h-10 w-10 bg-[#2F2F50] rounded-md",
                        "h-10 w-10 bg-[#295931] rounded-md",
                    )
                ),
                class_name="flex items-center gap-3",
            ),
            class_name="px-6 py-4",
        ),
        rx.el.td(
            rx.el.div(
                class_name=rx.cond(
                    DashboardState.color_scheme == "moonlit_clearing",
                    "h-4 w-40 bg-[#2F2F50] rounded",
                    "h-4 w-40 bg-[#295931] rounded",
                )
            ),
            class_name="px-6 py-4",
        ),
        rx.el.td(
            rx.el.div(
                class_name=rx.cond(
                    DashboardState.color_scheme == "moonlit_clearing",
                    "h-6 w-20 bg-[#2F2F50] rounded-full",
                    "h-6 w-20 bg-[#295931] rounded-full",
                )
            ),
            class_name="px-6 py-4",
        ),
        rx.el.td(
            rx.el.div(
                class_name=rx.cond(
                    DashboardState.color_scheme == "moonlit_clearing",
                    "h-4 w-24 bg-[#2F2F50] rounded",
                    "h-4 w-24 bg-[#295931] rounded",
                )
            ),
            class_name="px-6 py-4",
        ),
        rx.el.td(
            rx.el.div(
                class_name=rx.cond(
                    DashboardState.color_scheme == "moonlit_clearing",
                    "h-6 w-6 bg-[#2F2F50] rounded-full",
                    "h-6 w-6 bg-[#295931] rounded-full",
                )
            ),
            class_name="px-6 py-4",
        ),
        class_name="animate-pulse",
    )


def image_table_row(image: Image) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.input(
                type="checkbox",
                class_name=rx.cond(
                    DashboardState.color_scheme == "moonlit_clearing",
                    "h-4 w-4 rounded border-[#2F2F50] bg-transparent text-purple-600 focus:ring-purple-500",
                    "h-4 w-4 rounded border-[#295931] bg-transparent text-green-600 focus:ring-green-500",
                ),
            ),
            class_name="px-6 py-4",
        ),
        rx.el.td(
            rx.el.div(
                rx.image(
                    src=image["url"],
                    class_name="h-10 w-10 rounded-md object-cover bg-gray-500/20",
                ),
                rx.el.div(
                    rx.el.p(image["name"], class_name="font-medium"),
                    rx.el.p(
                        f"{image['size_kb']} KB",
                        class_name=rx.cond(
                            DashboardState.color_scheme == "moonlit_clearing",
                            "text-xs text-[#8B8BBF]",
                            "text-xs text-[#80A886]",
                        ),
                    ),
                ),
            ),
            class_name="px-6 py-4 whitespace-nowrap flex items-center gap-3",
        ),
        rx.el.td(
            status_badge(image["status"]), class_name="px-6 py-4 whitespace-nowrap"
        ),
        rx.el.td(
            rx.el.div(
                rx.foreach(
                    image["tags"],
                    lambda tag: rx.el.span(
                        tag,
                        class_name=rx.cond(
                            DashboardState.color_scheme == "moonlit_clearing",
                            "bg-[#2F2F50] text-[#C4C4D6] text-xs font-medium px-2 py-0.5 rounded-full",
                            "bg-[#295931] text-[#D4EAD6] text-xs font-medium px-2 py-0.5 rounded-full",
                        ),
                    ),
                ),
                class_name="flex flex-wrap gap-1",
            ),
            class_name="px-6 py-4",
        ),
        rx.el.td(
            image["processed_at"],
            class_name=rx.cond(
                DashboardState.color_scheme == "moonlit_clearing",
                "px-6 py-4 whitespace-nowrap text-sm text-[#8B8BBF]",
                "px-6 py-4 whitespace-nowrap text-sm text-[#80A886]",
            ),
        ),
        rx.el.td(
            rx.el.button(
                rx.icon(tag="rotate-cw", class_name="h-4 w-4 mr-2"),
                "Re-process",
                on_click=lambda: DashboardState.process_image_by_id(image["id"]),
                disabled=DashboardState.server_status != "online",
                class_name=rx.cond(
                    DashboardState.color_scheme == "moonlit_clearing",
                    "text-xs font-semibold text-purple-400 hover:text-purple-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center",
                    "text-xs font-semibold text-green-400 hover:text-green-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center",
                ),
            ),
            class_name="px-6 py-4 whitespace-nowrap text-right text-sm font-medium",
        ),
        class_name=rx.cond(
            DashboardState.color_scheme == "moonlit_clearing",
            "hover:bg-[#1A1A3F]/50 transition-colors",
            "hover:bg-[#15351B]/50 transition-colors",
        ),
    )


def image_table() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3("Image Processing Queue", class_name="text-lg font-semibold")
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            rx.el.input(
                                type="checkbox",
                                class_name=rx.cond(
                                    DashboardState.color_scheme == "moonlit_clearing",
                                    "h-4 w-4 rounded border-[#2F2F50] bg-transparent text-purple-600 focus:ring-purple-500",
                                    "h-4 w-4 rounded border-[#295931] bg-transparent text-green-600 focus:ring-green-500",
                                ),
                            ),
                            scope="col",
                            class_name="px-6 py-3",
                        ),
                        rx.el.th(
                            "File",
                            scope="col",
                            class_name="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Status",
                            scope="col",
                            class_name="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Tags",
                            scope="col",
                            class_name="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Last Update",
                            scope="col",
                            class_name="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider",
                        ),
                        rx.el.th("", scope="col", class_name="relative px-6 py-3"),
                        class_name=rx.cond(
                            DashboardState.color_scheme == "moonlit_clearing",
                            "border-b border-[#2F2F50]",
                            "border-b border-[#295931]",
                        ),
                    )
                ),
                rx.el.tbody(
                    rx.cond(
                        DashboardState.is_loading,
                        rx.fragment(
                            skeleton_row(),
                            skeleton_row(),
                            skeleton_row(),
                            skeleton_row(),
                            skeleton_row(),
                        ),
                        rx.foreach(DashboardState.images, image_table_row),
                    ),
                    class_name=rx.cond(
                        DashboardState.color_scheme == "moonlit_clearing",
                        "divide-y divide-[#2F2F50]",
                        "divide-y divide-[#295931]",
                    ),
                ),
                class_name="min-w-full",
            ),
            class_name="overflow-x-auto",
        ),
        class_name=rx.cond(
            DashboardState.color_scheme == "moonlit_clearing",
            "flex flex-col gap-4 p-6 bg-[#1A1A3F] border border-[#2F2F50] rounded-xl shadow-sm",
            "flex flex-col gap-4 p-6 bg-[#15351B] border border-[#295931] rounded-xl shadow-sm",
        ),
    )