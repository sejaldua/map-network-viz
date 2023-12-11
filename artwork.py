from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

# Define the paths to your 9 images
image_paths = [
    "./city_maps/Rome.png",
    "./city_maps/Bogota.png",
    "./city_maps/Tokyo.png",
    "./city_maps/Moscow.png",
    "./city_maps/Portland.png",
    "./city_maps/New_York.png",
    "./city_maps/Stockholm.png",
    "./city_maps/Budapest.png",
    "./city_maps/Vancouver.png",
]

# Check if there are exactly 9 images
if len(image_paths) != 9:
    raise ValueError(f"Expected 9 images, but found {len(image_paths)}")

# Load and resize images to be squares with 1:1 aspect ratio
images = []
for path in image_paths:
    try:
        image = Image.open(path)
        # Resize the image while maintaining aspect ratio and square shape
        width, height = image.size
        if width != height:
            new_size = min(width, height)
            image = image.crop((0, 0, new_size, new_size))
        # Convert to RGB format if needed
        if image.mode != "RGB":
            image = image.convert("RGB")
        images.append(np.array(image))
    except Exception as e:
        print(f"Error loading image: {path}")
        print(e)

# Create a 3x3 grid of subplots
fig, axes = plt.subplots(3, 3, figsize=(12, 12))

# Plot each image in its own subplot
for i in range(3):
    for j in range(3):
        index = i * 3 + j
        if index < len(images):
            axes[i, j].imshow(images[index])
            axes[i, j].set_xticks([])
            axes[i, j].set_yticks([])
            axes[i, j].set_ylim([0, images[index].shape[0]])
            axes[i, j].set_xlim([0, images[index].shape[1]])
        else:
            axes[i, j].axis("off")

fig.tight_layout()
fig.savefig('./art.png')