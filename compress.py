from PIL import Image
import os

def compress_image(
    image_path: str,
    output_quality: int = 80,
    max_size_kb: int = 500,
    output_format: str = "webp",
    auto_resize: bool = True
) -> str:
    """
    Compress an image and save it.
    Returns the path of the compressed image.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError("File does not exist.")

    original_size = os.path.getsize(image_path) / 1024
    img = Image.open(image_path)

    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    # Resize if auto_resize is enabled
    if auto_resize:
        width, height = img.size
        scale_factor = min(1, (max_size_kb / original_size) ** 0.5)
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)
        if new_width < width or new_height < height:
            img = img.resize((new_width, new_height), Image.LANCZOS)

    # Save compressed image
    compressed_path = image_path.rsplit(".", 1)[0] + f"_compressed.{output_format}"
    img.save(compressed_path, output_format, quality=output_quality)

    compressed_size = os.path.getsize(compressed_path) / 1024
    print(f"Original size: {original_size:.2f} KB")
    print(f"Compressed size: {compressed_size:.2f} KB")
    print(f"Compressed image saved at: {compressed_path}")

    return compressed_path