import reflex as rx
from typing import TypedDict, Literal
import asyncio
import random
from datetime import datetime

ImageStatus = Literal["pending", "processing", "completed", "error"]


class Image(TypedDict):
    id: int
    name: str
    url: str
    status: ImageStatus
    processed_at: str
    size_kb: int
    tags: list[str]


class ImageState(rx.State):
    images: list[Image] = []
    is_loading: bool = True
    sort_by: str = "date_desc"
    status_filter: str = "all"
    search_query: str = ""
    selected_image_ids: set[int] = set()

    @rx.event
    async def on_load(self):
        if self.is_loading:
            self.images = self._generate_mock_data(25)
            await asyncio.sleep(1.5)
            self.is_loading = False

    @rx.event
    def toggle_image_selection(self, image_id: int):
        if image_id in self.selected_image_ids:
            self.selected_image_ids.remove(image_id)
        else:
            self.selected_image_ids.add(image_id)

    @rx.var
    def filtered_images(self) -> list[Image]:
        images = self.images
        if self.status_filter != "all":
            images = [img for img in images if img["status"] == self.status_filter]
        if self.search_query:
            images = [
                img
                for img in images
                if self.search_query.lower() in img["name"].lower()
            ]
        sort_map = {
            "date_desc": ("processed_at", True),
            "date_asc": ("processed_at", False),
            "name_asc": ("name", False),
            "name_desc": ("name", True),
        }
        if self.sort_by in sort_map:
            key, reverse = sort_map[self.sort_by]
            images = sorted(images, key=lambda img: img[key], reverse=reverse)
        return images

    @rx.var
    def has_selection(self) -> bool:
        return len(self.selected_image_ids) > 0

    @rx.var
    def selection_count(self) -> int:
        return len(self.selected_image_ids)

    @rx.event
    def on_load_sync(self):
        if not self.images:
            self.images = self._generate_mock_data(25)

    def _generate_mock_data(self, count: int) -> list[Image]:
        mock_images = []
        for i in range(count):
            status = random.choice(["pending", "completed", "error", "processing"])
            mock_images.append(
                {
                    "id": i,
                    "name": f"image_{100 + i}_{random.randint(1000, 9999)}.jpg",
                    "url": f"https://api.dicebear.com/9.x/initials/svg?seed=Image{i}",
                    "status": status,
                    "processed_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "size_kb": random.randint(50, 2048),
                    "tags": random.sample(
                        ["nature", "city", "animal", "portrait", "abstract", "food"],
                        k=random.randint(1, 3),
                    )
                    if status == "completed"
                    else [],
                }
            )
        return mock_images