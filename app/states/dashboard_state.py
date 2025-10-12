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


class Stats(TypedDict):
    processed: int
    in_queue: int
    errors: int


class DashboardState(rx.State):
    server_status: Literal["online", "offline", "starting"] = "offline"
    images: list[Image] = []
    is_sidebar_open: bool = True
    is_loading: bool = True
    processing_log: list[str] = ["System Initialized. Ready for operations."]
    color_scheme: Literal["moonlit_clearing", "enchanted_forest"] = "moonlit_clearing"

    @rx.var
    def stats(self) -> Stats:
        processed = sum((1 for img in self.images if img["status"] == "completed"))
        in_queue = sum((1 for img in self.images if img["status"] == "pending"))
        errors = sum((1 for img in self.images if img["status"] == "error"))
        return {"processed": processed, "in_queue": in_queue, "errors": errors}

    @rx.event
    async def on_load(self):
        if self.is_loading:
            self.images = self._generate_mock_data(15)
            await asyncio.sleep(1.5)
            self.is_loading = False

    @rx.event
    def toggle_sidebar(self):
        self.is_sidebar_open = not self.is_sidebar_open

    @rx.event
    def toggle_color_scheme(self):
        if self.color_scheme == "moonlit_clearing":
            self.color_scheme = "enchanted_forest"
        else:
            self.color_scheme = "moonlit_clearing"

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

    def _add_log(self, message: str):
        self.processing_log.insert(
            0, f"[{datetime.now().strftime('%H:%M:%S')}] {message}"
        )
        if len(self.processing_log) > 100:
            self.processing_log = self.processing_log[:100]

    @rx.event(background=True)
    async def toggle_server_status(self):
        current_status = ""
        async with self:
            current_status = self.server_status
        if current_status == "online":
            async with self:
                self.server_status = "offline"
                self._add_log("Server shutdown initiated.")
            await asyncio.sleep(1)
            async with self:
                self._add_log("Server is offline.")
        elif current_status == "offline":
            async with self:
                self.server_status = "starting"
                self._add_log("Server startup sequence initiated.")
            await asyncio.sleep(2)
            async with self:
                self.server_status = "online"
                self._add_log("Server is online and operational.")

    @rx.event(background=True)
    async def process_image_by_id(self, image_id: int):
        async with self:
            if self.server_status != "online":
                yield rx.toast.error("Server is offline. Cannot process images.")
                return
        image_index = -1
        async with self:
            for i, img in enumerate(self.images):
                if img["id"] == image_id:
                    image_index = i
                    break
            if image_index != -1:
                self.images[image_index]["status"] = "processing"
                self._add_log(f"Processing image: {self.images[image_index]['name']}")
        await asyncio.sleep(random.uniform(2, 5))
        async with self:
            if image_index != -1:
                if random.random() > 0.15:
                    self.images[image_index]["status"] = "completed"
                    self.images[image_index]["tags"] = random.sample(
                        ["landscape", "tech", "urban", "vibrant", "dark"],
                        k=random.randint(2, 4),
                    )
                    self.images[image_index]["processed_at"] = datetime.now().strftime(
                        "%Y-%m-%d %H:%M"
                    )
                    self._add_log(
                        f"Successfully enriched: {self.images[image_index]['name']}"
                    )
                else:
                    self.images[image_index]["status"] = "error"
                    self._add_log(
                        f"Error processing: {self.images[image_index]['name']}"
                    )
                    yield rx.toast.error(
                        f"Failed to process {self.images[image_index]['name']}."
                    )

    @rx.event(background=True)
    async def process_all_pending(self):
        async with self:
            if self.server_status != "online":
                yield rx.toast.error("Server is offline. Cannot process images.")
                return
            self._add_log("Starting batch processing for all pending images.")
            pending_ids = [
                img["id"] for img in self.images if img["status"] == "pending"
            ]
        if not pending_ids:
            async with self:
                self._add_log("No pending images to process.")
            yield rx.toast.info("No pending images to process.")
            return
        for image_id in pending_ids:
            yield DashboardState.process_image_by_id(image_id)
            await asyncio.sleep(0.5)