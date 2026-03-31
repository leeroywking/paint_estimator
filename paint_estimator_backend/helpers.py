from PIL import Image


# def flatten_image(image_path,num_colors):
#     image = Image.open(image_path) # switch out for actual bit object
#     result = image.convert('P' , palette=Image.ADAPTIVE, colors=num_colors)
#     result.show()
#     result.save("./flattened_image.png","png")
#     return result

def flatten_image(image_path, num_colors):
    image = Image.open(image_path).convert("RGB")
    small = image.resize((image.width // 2, image.height // 2))
    result = small.quantize(colors=num_colors, method=Image.MEDIANCUT)
    result = result.resize(image.size, Image.NEAREST)
    result.save("./flattened_image.png","png")
    return result

def display_flattened_colors_by_percentage(image_path, num_colors):
    image = Image.open(image_path).convert("RGB")
    small = image.resize((image.width // 2, image.height // 2))
    quantized = small.quantize(colors=num_colors, method=Image.MEDIANCUT)
    color_counts = quantized.getcolors()
    total_pixels = sum(count for count, _ in color_counts)

    print(f"Top {num_colors} colors by percentage:")
    for count, palette_index in color_counts:
        percentage = (count / total_pixels) * 100
        rgb = quantized.getpalette()[palette_index * 3: palette_index * 3 + 3]
        print(f"Color: {tuple(rgb)}, Percentage: {percentage:.2f}%")

