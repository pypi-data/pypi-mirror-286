import os
import cv2
import torch
import numpy as np
from pathlib import Path
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn, TimeRemainingColumn
from rich.console import Console
import concurrent.futures
import tkinter as tk
from tkinter import filedialog
import typer
from typing import List
from ultralytics import YOLO

app = typer.Typer()
console = Console()

def model_callback(value: str):
    if value not in ["yolov8x.pt", "yolov8m.pt", "yolov8s.pt"]:
        raise typer.BadParameter("Invalid model choice")
    return value

@app.command()
def main(
    margin_percentage: int = typer.Option(3, help="Margin percentage for bounding box (default: 3, recommended range: 0-10)"),
    model_size: int = typer.Option(640, help="Model size (default: 640, recommended: 320, 640, or 1280)"),
    model: str = typer.Option(
        "yolov8x.pt", 
        callback=model_callback, 
        help="YOLOv8 model to use (options: yolov8x.pt, yolov8m.pt, yolov8s.pt)"
    ),
    recursive: bool = typer.Option(False, help="Search for images recursively"),
    crop_all: bool = typer.Option(False, help="Crop all detected persons instead of just the largest")
):
    # Load the YOLOv8 model
    yolo_model = YOLO(model)
    yolo_model.verbose = False  # Disable verbose output from YOLO

    # Use tkinter to prompt the user to pick the input directory
    tk.Tk().withdraw()
    input_dir_input = filedialog.askdirectory(title="Select Input Directory")
    if not input_dir_input:
        console.print("No directory selected, exiting...")
        raise typer.Exit()

    # Output directory is input + _cropped
    input_dir = Path(input_dir_input)
    output_dir = input_dir / "cropped"
    # Create the output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    # Recursive or non-recursive search for images
    if recursive:
        images_paths = list(input_dir.rglob("*.jpg")) + list(input_dir.rglob("*.jpeg")) + list(input_dir.rglob("*.png"))
    else:
        images_paths = list(input_dir.glob("*.jpg")) + list(input_dir.glob("*.jpeg")) + list(input_dir.glob("*.png"))

    console.print(f"Found {len(images_paths)} images to process.")

    def process_image(img_path):
        # Load the image
        image = cv2.imread(str(img_path))
        if image is None:
            console.print(f"Failed to load image: {img_path}")
            return False
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Detect the person in the image
        results = yolo_model(image_rgb, imgsz=model_size)
        
        # Check if results is a list and take the first item if so
        if isinstance(results, list):
            results = results[0]
        
        # Check if 'boxes' attribute exists
        if not hasattr(results, 'boxes'):
            console.print(f"No detection results for {img_path}")
            return False

        person_boxes = [box for box in results.boxes if box.cls == 0]  # Class 0 is typically person

        if person_boxes:
            if crop_all:
                boxes_to_process = person_boxes
            else:
                # Get the box with the largest area
                largest_box = max(person_boxes, key=lambda box: (box.xyxy[0][2] - box.xyxy[0][0]) * (box.xyxy[0][3] - box.xyxy[0][1]))
                boxes_to_process = [largest_box]

            for i, box in enumerate(boxes_to_process):
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                # Calculate the margin
                width = x2 - x1
                height = y2 - y1
                margin_x = int(width * margin_percentage / 100)
                margin_y = int(height * margin_percentage / 100)

                # Add the margin to the bounding box
                x1 = max(0, x1 - margin_x)
                y1 = max(0, y1 - margin_y)
                x2 = min(image.shape[1], x2 + margin_x)
                y2 = min(image.shape[0], y2 + margin_y)
                cropped_image = image[y1:y2, x1:x2]

                # Save the cropped image
                relative_path = img_path.relative_to(input_dir)
                suffix = f"_person_{i}" if crop_all else ""
                output_path = output_dir / relative_path.parent / f"{img_path.stem}_cropped{suffix}{img_path.suffix}"
                output_path.parent.mkdir(parents=True, exist_ok=True)
                cv2.imwrite(str(output_path), cropped_image)
            return True
        else:
            console.print(f"No person detected in {img_path}")
            return False

    processed_count = 0
    failed_count = 0
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("[cyan]Processing images...", total=len(images_paths))

        # Parallelize the processing of images using a ThreadPoolExecutor
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
            futures = [executor.submit(process_image, img_path) for img_path in images_paths]

            for future in concurrent.futures.as_completed(futures):
                try:
                    if future.result():
                        processed_count += 1
                    else:
                        failed_count += 1
                except Exception as e:
                    console.print(f"Error processing image: {e}")
                    failed_count += 1
                finally:
                    progress.update(task, advance=1)

    console.print(f"Processing finished! Successfully processed {processed_count} images. Failed to process {failed_count} images.")

    # Ask user if they want to remove small images
    remove_small = typer.confirm("Do you want to remove small images?")
    if remove_small:
        size_threshold = typer.prompt("Enter size threshold in kB", type=int)
        size_threshold_bytes = size_threshold * 1024  # Convert kB to bytes

        removed_count = 0
        for img_path in output_dir.glob("*"):
            if img_path.stat().st_size < size_threshold_bytes:
                os.remove(str(img_path))
                removed_count += 1

        console.print(f"Removed {removed_count} images smaller than {size_threshold} kB")

    console.print("Script finished successfully!")

if __name__ == "__main__":
    app()