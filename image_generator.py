#### Generate Images
import os
from multiprocessing import Pool

from PIL import Image
from tqdm import tqdm

from generator import TOTAL_IMAGES
from gistfile import *

if not os.path.exists("./images"):
    os.makedirs("./images")

layers_path = "layers"
layers = {
    "01": [
        ("Background", "00_background_"),
        ("Body", "01_body_"),
        ("Left Strand", "02_left-strand_"),
        ("Face", "03_face"),
        ("Right Strand", "04_right-strand_"),
        ("Left Eye", "05_left-eye_"),
        ("Nose", "06_nose_"),
        ("Right Eye", "07_right-eye_"),
        ("Print", "08_print_"),
        ("Lips", "09_lips_"),
        ("Flowers", "10_flowers_"),
    ],
    "02": [
        ("Background", "00_background_"),
        ("Hair", "02_hair_"),
        ("Body", "03_body_"),
        ("Face", "04_face_"),
        ("Nose", "05_nose_"),
        ("Left Eye", "06_left-eye_"),
        ("Right Eye", "07_right-eye_"),
        ("Print", "08_print_"),
        ("Lips", "09_lips_"),
        ("Flowers", "10_flowers_"),
    ],
}


def generate_images(all_images):
    for item in tqdm(all_images):
        generate_image(item)


def generate_image(item):
    last_image = Image.new("RGBA", (2000, 2000))
    for layer, file_name in layers[item["path"]]:
        if item[layer]:
            image = Image.open(
                f"{layers_path}/{item['path']}/{file_name}{item[layer]:02d}.png"
            ).convert("RGBA")
            last_image = Image.alpha_composite(last_image, image)

    rgb_im = last_image.convert("RGB")
    file_name = str(item["tokenId"]) + ".png"
    rgb_im.save("./images/" + file_name)


def generate_images_in_pool(all_images):
    with Pool(processes=4) as p:
        max_ = TOTAL_IMAGES
        with tqdm(total=max_) as pbar:
            for i, _ in enumerate(p.imap_unordered(generate_image, all_images)):
                pbar.update()
