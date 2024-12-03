import os
from PIL import Image

# Directory containing images
IMAGE_DIR = '/home/sofiane/CascadeProjects/celebritys_travel/static/images'

# Target directory for compressed images
COMPRESSED_DIR = '/home/sofiane/CascadeProjects/celebritys_travel/static/images/compressed'

# Ensure the compressed directory exists
os.makedirs(COMPRESSED_DIR, exist_ok=True)

# Iterate over all files in the image directory
for filename in os.listdir(IMAGE_DIR):
    if filename.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'bmp')):
        filepath = os.path.join(IMAGE_DIR, filename)
        with Image.open(filepath) as img:
            # Compress and save the image
            img.save(os.path.join(COMPRESSED_DIR, filename), optimize=True, quality=85)

print('Image compression complete.')
