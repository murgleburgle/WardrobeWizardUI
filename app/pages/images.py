import reflex as rx
from app.states.dashboard_state import DashboardState
from app.states.image_state import ImageState
from app.components.sidebar import sidebar
from app.components.header import header
from app.components.image_grid import image_grid


def filter_and_sort_controls() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.select(
                rx.foreach(
                    ["date_desc", "date_asc", "name_asc", "name_desc"],
                    lambda option: rx.el.option(
                        option.replace("_", " ").capitalize(), value=option
                    ),
                ),
                on_change=ImageState.set_sort_by,
                value=ImageState.sort_by,
                class_name=rx.cond(
                    DashboardState.color_scheme == "moonlit_clearing",
                    "bg-[#1A1A3F] border border-[#2F2F50] rounded-lg px-3 py-2 text-sm",
                    "bg-[#15351B] border border-[#295931] rounded-lg px-3 py-2 text-sm",
                ),
            ),
            rx.el.select(
                rx.foreach(
                    ["all", "completed", "processing", "pending", "error"],
                    lambda option: rx.el.option(option.capitalize(), value=option),
                ),
                on_change=ImageState.set_status_filter,
                value=ImageState.status_filter,
                class_name=rx.cond(
                    DashboardState.color_scheme == "moonlit_clearing",
                    "bg-[#1A1A3F] border border-[#2F2F50] rounded-lg px-3 py-2 text-sm",
                    "bg-[#15351B] border border-[#295931] rounded-lg px-3 py-2 text-sm",
                ),
            ),
            class_name="flex items-center gap-4",
        ),
        rx.el.div(class_name="flex items-center gap-2"),
        class_name="flex items-center justify-between mb-4",
    )


def images() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            header(),
            rx.el.main(
                rx.el.div(
                    rx.el.h1("Image Library", class_name="text-2xl font-bold mb-4"),
                    filter_and_sort_controls(),
                    image_grid(),
                ),
                class_name="p-4 md:p-6 lg:p-8",
            ),
            on_mount=ImageState.on_load,
            class_name="flex-1 overflow-auto",
        ),
        class_name=rx.cond(
            DashboardState.color_scheme == "moonlit_clearing",
            "flex h-screen bg-[#0F0F28] text-[#C4C4D6] font-['Lato']",
            "flex h-screen bg-[#0A1F0D] text-[#D4EAD6] font-['Lato']",
        ),
    )