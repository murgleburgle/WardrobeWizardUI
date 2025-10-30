import reflex as rx
from app.states.dashboard_state import DashboardState
from app.states.image_detail_state import ImageDetailState, Image
from app.components.sidebar import sidebar
from app.components.header import header


def metadata_section(title: str, children: list[rx.Component]) -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            title,
            class_name=rx.cond(
                DashboardState.color_scheme == "moonlit_clearing",
                "text-md font-semibold text-[#E0E0FF] border-b border-[#2F2F50] pb-2 mb-3",
                "text-md font-semibold text-[#E6F5E8] border-b border-[#295931] pb-2 mb-3",
            ),
        ),
        *children,
        class_name="flex flex-col gap-2",
    )


def tag_display(tag: str) -> rx.Component:
    return rx.el.div(
        tag,
        rx.el.button(
            rx.icon(tag="x", class_name="h-3 w-3"),
            on_click=lambda: ImageDetailState.remove_tag(tag),
            class_name=rx.cond(
                DashboardState.color_scheme == "moonlit_clearing",
                "ml-2 text-purple-300 hover:text-purple-100",
                "ml-2 text-green-300 hover:text-green-100",
            ),
        ),
        class_name=rx.cond(
            DashboardState.color_scheme == "moonlit_clearing",
            "flex items-center bg-[#2F2F50] text-[#C4C4D6] text-xs font-medium px-2.5 py-1 rounded-full",
            "flex items-center bg-[#295931] text-[#D4EAD6] text-xs font-medium px-2.5 py-1 rounded-full",
        ),
    )


def image_detail() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            header(),
            rx.el.main(
                rx.cond(
                    ImageDetailState.is_loading,
                    rx.el.div(
                        rx.el.div(
                            class_name="h-full w-3/5 animate-pulse bg-gray-500/10 rounded-lg"
                        ),
                        rx.el.div(
                            class_name="h-full w-2/5 animate-pulse bg-gray-500/10 rounded-lg"
                        ),
                        class_name="flex h-full gap-6",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.image(
                                src=ImageDetailState.selected_image.url,
                                class_name="max-h-[80vh] w-auto h-auto object-contain transition-transform duration-300",
                                style={
                                    "transform": f"scale({ImageDetailState.zoom_level})"
                                },
                            ),
                            class_name="w-3/5 flex items-center justify-center overflow-hidden rounded-lg bg-black/20 p-4",
                        ),
                        rx.el.div(
                            rx.el.div(
                                metadata_section(
                                    "Details",
                                    [
                                        rx.el.p(
                                            rx.el.strong("Name: "),
                                            ImageDetailState.selected_image.name,
                                        ),
                                        rx.el.p(
                                            rx.el.strong("Size: "),
                                            f"{ImageDetailState.selected_image.size_kb} KB",
                                        ),
                                    ],
                                ),
                                metadata_section(
                                    "Tags",
                                    [
                                        rx.el.div(
                                            rx.foreach(
                                                ImageDetailState.selected_image.tags,
                                                tag_display,
                                            ),
                                            class_name="flex flex-wrap gap-2",
                                        ),
                                        rx.el.form(
                                            rx.el.input(
                                                name="new_tag",
                                                placeholder="Add a tag...",
                                                class_name=rx.cond(
                                                    DashboardState.color_scheme
                                                    == "moonlit_clearing",
                                                    "w-full bg-[#0F0F28] border border-[#2F2F50] rounded-md px-2 py-1 text-sm",
                                                    "w-full bg-[#0A1F0D] border border-[#295931] rounded-md px-2 py-1 text-sm",
                                                ),
                                            ),
                                            on_submit=ImageDetailState.add_tag,
                                            reset_on_submit=True,
                                            class_name="mt-2",
                                        ),
                                    ],
                                ),
                                metadata_section(
                                    "AI Analysis",
                                    [
                                        rx.el.button(
                                            "Trigger Object Detection",
                                            on_click=lambda: ImageDetailState.trigger_analysis(
                                                "detection"
                                            ),
                                        ),
                                        rx.el.button(
                                            "Trigger Classification",
                                            on_click=lambda: ImageDetailState.trigger_analysis(
                                                "classification"
                                            ),
                                        ),
                                    ],
                                ),
                                class_name="flex flex-col gap-6",
                            ),
                            class_name=rx.cond(
                                DashboardState.color_scheme == "moonlit_clearing",
                                "w-2/5 p-6 bg-[#1A1A3F] border border-[#2F2F50] rounded-xl shadow-sm overflow-y-auto",
                                "w-2/5 p-6 bg-[#15351B] border border-[#295931] rounded-xl shadow-sm overflow-y-auto",
                            ),
                        ),
                        class_name="flex h-full gap-6",
                    ),
                ),
                class_name="p-6 h-[calc(100vh-4rem)]",
            ),
            on_mount=ImageDetailState.load_image_details,
            class_name="flex-1 overflow-auto",
        ),
        class_name=rx.cond(
            DashboardState.color_scheme == "moonlit_clearing",
            "flex h-screen bg-[#0F0F28] text-[#C4C4D6] font-['Lato']",
            "flex h-screen bg-[#0A1F0D] text-[#D4EAD6] font-['Lato']",
        ),
    )