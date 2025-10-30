import reflex as rx
from app.states.dashboard_state import DashboardState


def nav_item(text: str, icon: str, href: str) -> rx.Component:
    is_active = DashboardState.router.page.path == href
    active_style = rx.cond(
        DashboardState.color_scheme == "moonlit_clearing",
        "flex items-center px-3 py-2.5 text-sm font-semibold bg-purple-600/20 text-purple-300 rounded-lg group",
        "flex items-center px-3 py-2.5 text-sm font-semibold bg-green-600/20 text-green-300 rounded-lg group",
    )
    inactive_style = rx.cond(
        DashboardState.color_scheme == "moonlit_clearing",
        "flex items-center px-3 py-2.5 text-sm font-medium text-[#8B8BBF] hover:bg-[#1A1A3F] rounded-lg group",
        "flex items-center px-3 py-2.5 text-sm font-medium text-[#80A886] hover:bg-[#15351B] rounded-lg group",
    )
    return rx.el.a(
        rx.el.div(
            rx.icon(
                tag=icon,
                class_name=rx.cond(
                    is_active,
                    rx.cond(
                        DashboardState.color_scheme == "moonlit_clearing",
                        "text-purple-400",
                        "text-green-400",
                    ),
                    "group-hover:text-[#C4C4D6]",
                ),
            ),
            rx.el.span(
                text,
                class_name=rx.cond(
                    DashboardState.is_sidebar_open, "opacity-100", "opacity-0"
                ),
            ),
            class_name="flex items-center gap-3 transition-all duration-200",
        ),
        class_name=rx.cond(is_active, active_style, inactive_style),
        href=href,
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        tag="command",
                        class_name=rx.cond(
                            DashboardState.color_scheme == "moonlit_clearing",
                            "text-purple-500",
                            "text-green-500",
                        ),
                    ),
                    rx.el.h2(
                        "WardrobeWizard",
                        class_name=rx.cond(
                            DashboardState.is_sidebar_open,
                            "font-bold text-xl transition-opacity duration-200 opacity-100",
                            "font-bold text-xl transition-opacity duration-200 opacity-0",
                        ),
                    ),
                    class_name=rx.cond(
                        DashboardState.color_scheme == "moonlit_clearing",
                        "flex items-center gap-3 h-16 border-b border-[#2F2F50] px-4",
                        "flex items-center gap-3 h-16 border-b border-[#295931] px-4",
                    ),
                ),
                rx.el.nav(
                    nav_item("Dashboard", "layout-dashboard", "/"),
                    nav_item("Images", "image", "/images"),
                    nav_item("API Logs", "scroll-text", "#"),
                    nav_item("Settings", "settings", "#"),
                    class_name="flex-1 flex flex-col gap-1 p-2",
                ),
            ),
            rx.el.div(
                rx.el.div(
                    class_name=rx.cond(
                        DashboardState.color_scheme == "moonlit_clearing",
                        "flex-1 border-t border-[#2F2F50]",
                        "flex-1 border-t border-[#295931]",
                    )
                ),
                rx.el.div(
                    nav_item("Help", "life-buoy", "#"),
                    rx.el.div(
                        rx.image(
                            src="https://api.dicebear.com/9.x/notionists/svg?seed=Admin",
                            class_name="w-8 h-8 rounded-full",
                        ),
                        rx.el.div(
                            rx.el.p("Admin User", class_name="text-sm font-semibold"),
                            rx.el.p(
                                "admin@example.com",
                                class_name=rx.cond(
                                    DashboardState.color_scheme == "moonlit_clearing",
                                    "text-xs text-[#8B8BBF]",
                                    "text-xs text-[#80A886]",
                                ),
                            ),
                            class_name=rx.cond(
                                DashboardState.is_sidebar_open,
                                "flex flex-col transition-opacity duration-200 opacity-100",
                                "flex flex-col transition-opacity duration-200 opacity-0",
                            ),
                        ),
                        class_name="flex items-center gap-3 p-2",
                    ),
                    class_name="p-2",
                ),
            ),
            class_name="flex flex-col justify-between h-full",
        ),
        class_name=rx.cond(
            DashboardState.color_scheme == "moonlit_clearing",
            rx.cond(
                DashboardState.is_sidebar_open,
                "bg-[#1A1A3F]/80 backdrop-blur-sm border-r border-[#2F2F50] flex flex-col transition-all duration-300 ease-in-out w-64",
                "bg-[#1A1A3F]/80 backdrop-blur-sm border-r border-[#2F2F50] flex flex-col transition-all duration-300 ease-in-out w-20",
            ),
            rx.cond(
                DashboardState.is_sidebar_open,
                "bg-[#15351B]/80 backdrop-blur-sm border-r border-[#295931] flex flex-col transition-all duration-300 ease-in-out w-64",
                "bg-[#15351B]/80 backdrop-blur-sm border-r border-[#295931] flex flex-col transition-all duration-300 ease-in-out w-20",
            ),
        ),
    )