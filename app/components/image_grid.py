import reflex as rx
from app.states.dashboard_state import DashboardState
from app.states.image_state import ImageState, Image


def image_card(image: Image) -> rx.Component:
    return rx.el.a(
        rx.image(
            src=image["url"], class_name="aspect-square w-full rounded-md object-cover"
        ),
        rx.el.div(
            rx.el.p(image["name"], class_name="text-sm font-medium truncate"),
            class_name=rx.cond(
                DashboardState.color_scheme == "moonlit_clearing",
                "absolute bottom-0 left-0 right-0 p-2 bg-gradient-to-t from-[#1A1A3F] to-transparent",
                "absolute bottom-0 left-0 right-0 p-2 bg-gradient-to-t from-[#15351B] to-transparent",
            ),
        ),
        href=f"/images/{image['id']}",
        class_name=rx.cond(
            DashboardState.color_scheme == "moonlit_clearing",
            "relative group overflow-hidden rounded-lg border border-[#2F2F50] hover:shadow-lg transition-shadow duration-200",
            "relative group overflow-hidden rounded-lg border border-[#295931] hover:shadow-lg transition-shadow duration-200",
        ),
    )


def skeleton_card() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            class_name=rx.cond(
                DashboardState.color_scheme == "moonlit_clearing",
                "aspect-square w-full bg-[#2F2F50]",
                "aspect-square w-full bg-[#295931]",
            )
        ),
        class_name="animate-pulse rounded-lg overflow-hidden",
    )


def image_grid() -> rx.Component:
    return rx.el.div(
        rx.cond(
            ImageState.is_loading,
            rx.el.div(
                rx.foreach(range(25), lambda i: skeleton_card()),
                class_name="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4",
            ),
            rx.el.div(
                rx.foreach(ImageState.filtered_images, image_card),
                class_name="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4",
            ),
        )
    )