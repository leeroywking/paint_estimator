# import flatten_image from helpers
from helpers import flatten_image, display_flattened_colors_by_percentage
from chat_gptcode import flatten_with_min_distance


if __name__ == "__main__":
    # flatten_image("./image.jpg", 20)
    result, palette = flatten_with_min_distance(
        "image.png",
        num_colors=20,
        candidate_count=150,
        min_distance=5
    )

    print(palette)
    result.show()
    result.save("flattened_image.png")
    display_flattened_colors_by_percentage("./flattened_image.png", 20 )