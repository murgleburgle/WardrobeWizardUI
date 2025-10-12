import reflex as rx
from app.states.dashboard_state import DashboardState
from app.components.sidebar import sidebar
from app.components.header import header
from app.components.stats_cards import stats_overview
from app.components.control_panel import control_panel
from app.components.image_table import image_table


def index() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            header(),
            rx.el.main(
                rx.el.div(
                    stats_overview(),
                    control_panel(),
                    image_table(),
                    class_name="flex flex-col gap-6",
                ),
                class_name="p-4 md:p-6 lg:p-8",
            ),
            on_mount=DashboardState.on_load,
            class_name="flex-1 overflow-auto",
        ),
        class_name=rx.cond(
            DashboardState.color_scheme == "moonlit_clearing",
            "flex h-screen bg-[#0F0F28] text-[#C4C4D6] font-['Lato']",
            "flex h-screen bg-[#0A1F0D] text-[#D4EAD6] font-['Lato']",
        ),
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Lato:wght@400;700;900&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index)