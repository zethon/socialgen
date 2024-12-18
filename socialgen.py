import glob
import random
import os
import re
import sys
from PIL import Image, ImageDraw, ImageFont
from QuoteGenerator import get_quotes
import logging
from colorlog import ColoredFormatter

OUTPUT_FOLDER = "output"
FONTS_LOCATION = "fonts/*.*"
MAX_TEXT_LENGTH = 40

def get_random_file_from_glob(pattern):
    files = glob.glob(pattern)
    if not files:
        print("No files matched the given glob pattern.")
        return None
    random_file = random.choice(files)
    return random_file

def get_font_size(chunks, img_width, font_file, draw_obj=None):
    longest_string = max(chunks, key=len)
    font_size = 1
    while True:
        font = ImageFont.truetype(font_file, size=font_size)
        bbox = draw_obj.textbbox((0, 0), longest_string, font=font)
        text_width = bbox[2] - bbox[0]
        if text_width > img_width:
            break
        font_size += 1
    return font_size


def get_text_boxes(text, img_width, img_height, font_file, draw_obj=None):
    chunks = re.split(r'(?<=[,.!?;:\-])\s*', text)
    chunks = [chunk for chunk in chunks if chunk.strip()]
    final_chunks = []
    for chunk in chunks:
        if len(chunk) <= 40:
            final_chunks.append(chunk)
        else:
            words = chunk.split()
            temp = ""
            for word in words:
                if len(temp) + len(word) <= MAX_TEXT_LENGTH:
                    temp += word + " "
                else:
                    final_chunks.append(temp)
                    temp = word + " "
            final_chunks.append(temp)

    final_chunks = [line.strip() for line in final_chunks]
    final_chunks = [chunk.strip('"').strip("'") for chunk in final_chunks]
    line_height = (img_height - 20) // len(final_chunks)

    try:
        font_file = get_random_file_from_glob(FONTS_LOCATION)
        font_size = get_font_size(final_chunks, img_width, font_file)
        font = ImageFont.truetype(font_file, size=font_size)
    except:
        font = ImageFont.load_default()

    # (0, 0), text, font=font
    img_boxes = []
    for i, line in enumerate(final_chunks):
        img_boxes.append((0, i*line_height, line, font))

    return img_boxes

def generate_image(width, height, text, output_path):
    # Create a blank image
    image = Image.new("RGB", (width, height), color="white")
    
    # Initialize drawing context
    draw = ImageDraw.Draw(image)
    
    # # Load a font (default or system font)
    # try:
    #     font_file = get_random_file_from_glob(FONTS_LOCATION)
    #     font = ImageFont.truetype(font_file, size=min(width, height) // 10)
    # except:
    #     # Use default font if "arial.ttf" is unavailable
    #     font = ImageFont.load_default()

    font_file = get_random_file_from_glob(FONTS_LOCATION)
    text_boxes = get_text_boxes(text, width, height, font_file, draw)
    for box in text_boxes:
        draw.text((box[0], box[1]), box[2], fill="black", font=box[3])
    
    # # Get text size
    # # text_width, text_height = draw.textsize(text, font=font)
    # bbox = draw.textbbox((0, 0), text, font=font)
    # text_width = bbox[2] - bbox[0]
    # text_height = bbox[3] - bbox[1]
    
    # # Calculate position to center the text
    # x = (width - text_width) / 2
    # y = (height - text_height) / 2
    
    # # Add text to the image
    # draw.text((x, y), text, fill="black", font=font)
    
    # Save the image
    image.save(output_path)
    print(f"Image saved at {output_path}")

def main():
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
        print(f"Created folder: {OUTPUT_FOLDER}")
        
    output_path = os.path.join(OUTPUT_FOLDER, "output_image.png")

    # msgs = get_quotes()
    msgs = ["'Life is like a box of chocolates. You never know what you're gonna get.'"]
    for i, msg in enumerate(msgs):
        output_path = os.path.join(OUTPUT_FOLDER, f"output_image_{i+1}.png")
        print(f"Quote {i+1}:", msg)
        generate_image(274, 341, msg, output_path)
    
    # msg = "My name is Jeff, and I like to eat cheese. Yesterday my Mom told me to go to the store and buy some milk. I went to the store and bought some milk. I also bought some cheese. I like cheese. I like milk. I like to eat cheese. I like to poop"

    # print("Quote:", msg)
    # generate_image(274, 341, msg, output_path)

# Example Usage
if __name__ == "__main__":
    main()
