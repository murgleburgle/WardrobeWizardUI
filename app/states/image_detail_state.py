import reflex as rx
from typing import TypedDict, Literal, Optional
import asyncio
import random
from datetime import datetime
import logging
from app.states.dashboard_state import DashboardState
from app.states.image_state import Image, ImageState


class ImageDetailState(rx.State):
    selected_image: Optional[Image] = None
    similar_images: list[Image] = []
    suggested_tags: list[str] = []
    is_loading: bool = True
    zoom_level: float = 1.0

    @rx.event
    async def load_image_details(self):
        """Load image details based on the image ID from the URL."""
        image_id_str = self.router.page.params.get("image_id", "")
        self.is_loading = True
        if not image_id_str or not image_id_str.isdigit():
            logging.error(f"Invalid image_id from router: {image_id_str}")
            self.is_loading = False
            return
        selected_id = -1
        try:
            selected_id = int(image_id_str)
        except (ValueError, TypeError) as e:
            logging.exception(f"Error converting image_id: {e}")
            self.is_loading = False
            return
        image_state = await self.get_state(ImageState)
        if not image_state.images:
            image_state.on_load_sync()
        found = False
        for img in image_state.images:
            if img["id"] == selected_id:
                self.selected_image = img
                found = True
                break
        if not found:
            self.selected_image = None
            self.is_loading = False
            return
        await asyncio.sleep(0.5)
        self.similar_images = random.sample(
            [i for i in image_state.images if i["id"] != selected_id],
            k=min(6, len(image_state.images) - 1),
        )
        self.suggested_tags = random.sample(
            ["modern", "chic", "vibrant", "minimalist", "elegant"], k=3
        )
        self.is_loading = False

    @rx.event
    def add_tag(self, form_data: dict):
        """Add a new tag to the selected image."""
        new_tag = form_data.get("new_tag")
        if (
            self.selected_image
            and new_tag
            and (new_tag not in self.selected_image["tags"])
        ):
            self.selected_image["tags"].append(new_tag)

    @rx.event
    def remove_tag(self, tag: str):
        """Remove a tag from the selected image."""
        if self.selected_image and tag in self.selected_image["tags"]:
            self.selected_image["tags"].remove(tag)

    @rx.event
    def trigger_analysis(self, model_type: str):
        """Trigger a specific AI model analysis for the image."""
        yield rx.toast.info(
            f"Triggering {model_type} analysis for {(self.selected_image['name'] if self.selected_image else 'image')}."
        )

    @rx.event
    def zoom_in(self):
        self.zoom_level = min(self.zoom_level + 0.1, 3.0)

    @rx.event
    def zoom_out(self):
        self.zoom_level = max(self.zoom_level - 0.1, 0.5)

    @rx.event
    async def navigate_to_next(self):
        image_state = await self.get_state(ImageState)
        image_id = self.router.page.params.get("image_id")
        if not image_id or not image_id.isdigit():
            return
        selected_id = int(image_id)
        current_index = -1
        for i, img in enumerate(image_state.images):
            if img["id"] == selected_id:
                current_index = i
                break
        if current_index != -1 and current_index < len(image_state.images) - 1:
            next_id = image_state.images[current_index + 1]["id"]
            return rx.redirect(f"/images/{next_id}")

    @rx.event
    async def navigate_to_prev(self):
        image_state = await self.get_state(ImageState)
        image_id = self.router.page.params.get("image_id")
        if not image_id or not image_id.isdigit():
            return
        selected_id = int(image_id)
        current_index = -1
        for i, img in enumerate(image_state.images):
            if img["id"] == selected_id:
                current_index = i
                break
        if current_index > 0:
            prev_id = image_state.images[current_index - 1]["id"]
            return rx.redirect(f"/images/{prev_id}")