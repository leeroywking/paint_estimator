from PIL import Image
import math


def color_distance(c1, c2):
    return math.sqrt(
        (c1[0] - c2[0]) ** 2 +
        (c1[1] - c2[1]) ** 2 +
        (c1[2] - c2[2]) ** 2
    )


def get_candidate_colors(image, candidate_count=64):
    """
    Quantize to a larger palette first, then extract RGB colors with counts.
    """
    quantized = image.quantize(colors=candidate_count, method=Image.MEDIANCUT)
    palette = quantized.getpalette()[:candidate_count * 3]
    color_counts = quantized.getcolors()

    candidates = []
    for count, palette_index in color_counts:
        rgb = tuple(palette[palette_index * 3: palette_index * 3 + 3])
        candidates.append((count, rgb))

    # most common first
    candidates.sort(reverse=True, key=lambda x: x[0])
    return candidates


def pick_distinct_colors(candidates, num_colors, min_distance=60):
    """
    Greedy selection:
    - prefer common colors
    - reject colors too close to already selected ones
    """
    selected = []

    for count, color in candidates:
        if all(color_distance(color, chosen) >= min_distance for chosen in selected):
            selected.append(color)
            if len(selected) == num_colors:
                return selected

    # If threshold was too strict, fill remaining slots with best leftovers
    for count, color in candidates:
        if color not in selected:
            selected.append(color)
            if len(selected) == num_colors:
                break

    return selected


def nearest_color(pixel, palette):
    return min(palette, key=lambda c: color_distance(pixel, c))


def remap_image_to_palette(image, palette):
    """
    Remap every pixel in the image to the nearest selected palette color.
    """
    image = image.convert("RGB")
    pixels = list(image.getdata())
    remapped = [nearest_color(pixel, palette) for pixel in pixels]

    output = Image.new("RGB", image.size)
    output.putdata(remapped)
    return output


def flatten_with_min_distance(image_path, num_colors, candidate_count=64, min_distance=60):
    image = Image.open(image_path).convert("RGB")

    candidates = get_candidate_colors(image, candidate_count=candidate_count)
    palette = pick_distinct_colors(candidates, num_colors=num_colors, min_distance=min_distance)
    result = remap_image_to_palette(image, palette)

    return result, palette