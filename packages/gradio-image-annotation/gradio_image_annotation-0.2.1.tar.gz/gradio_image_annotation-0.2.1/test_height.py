import gradio as gr
from gradio_image_annotation import image_annotator
import time
import numpy as np
import random

example_annotation = {
    "image": "https://gradio-builds.s3.amazonaws.com/demo-files/base.png",
    "boxes": [
        {
            "xmin": 636,
            "ymin": 575,
            "xmax": 801,
            "ymax": 697,
            "label": "Vehicle",
            "color": (255, 0, 0)
        },
        {
            "xmin": 360,
            "ymin": 615,
            "xmax": 386,
            "ymax": 702,
            "label": "Person",
            "color": (0, 255, 0)
        }
    ]
}

example_crop = {
    "image": "https://raw.githubusercontent.com/gradio-app/gradio/main/guides/assets/logo.png",
    "boxes": [
        {
            "xmin": 30,
            "ymin": 70,
            "xmax": 530,
            "ymax": 500,
            "color": (100, 200, 255)
        }
    ]
}


def run(annotations):
    while True:
        w = 1920
        # h = random.randint(100, 700)
        h = 1080
        img = np.random.random((h, w, 3))
        yield  {
            "image": img
        }
        time.sleep(1)

def run2(annotations):
    while True:
        w = 1920
        # h = random.randint(100, 700)
        h = 1080
        img = np.random.random((h, w, 3))
        yield  img
        time.sleep(1)

with gr.Blocks() as demo:
    with gr.Row():
        annotator = image_annotator(
            example_crop,
            image_type="numpy",
        )
        image = gr.Image()
    button = gr.Button()
    button.click(run, annotator, annotator)
    button2 = gr.Button()
    button2.click(run2, image, image)


if __name__ == "__main__":
    demo.launch()
