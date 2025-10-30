I have a FastAPI implementation for my backend that uses various models to perform object detection, image classification, and captioning. I also generate image embeddings that are used for kmeans clustering analysis. Next on my implementation to-do list is to implement pose similarity analysis, human action classificaiton, and sequence detection.

My image database is primarily composed of models in various outfits.

From my frontend I need the following types of pages:
-a Dashboard to monitor background processes and quickly determine progress and other information
-An images tab that gives the user a grid view and lets them perform various functions, as well as select an image to go to a single-image page where the user can trigger analyses, review tags generated, and view suggested similar images or missing tags
-Galleries page that lets the user create galleries of related images, either conceptually (ex. blue dresses), from the same photoshoot, or from the same event (ex. MTV VMAs 2024)
-Tags page to allow the user to perform various tag management tasks
-Tools page to allow the user to start or stop background processing, manage databases, etc.
-Settings page