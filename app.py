from flask import Flask, render_template, request, send_file
from PIL import Image
from io import BytesIO

app = Flask(__name__)

def compress_image_in_memory(img: Image.Image, output_quality=80, output_format="webp", max_size_kb=500) -> BytesIO:
    """
    Compress a PIL image in memory and return a BytesIO object.
    """
    # Convert mode if needed
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    # Resize to reduce file size
    width, height = img.size
    original_bytes = BytesIO()
    img.save(original_bytes, format=output_format, quality=output_quality)
    original_size = len(original_bytes.getvalue()) / 1024

    scale_factor = min(1, (max_size_kb / original_size) ** 0.5)
    if scale_factor < 1:
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)
        img = img.resize((new_width, new_height), Image.LANCZOS)

    # Save to BytesIO
    output_bytes = BytesIO()
    img.save(output_bytes, format=output_format, quality=output_quality)
    output_bytes.seek(0)
    return output_bytes

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("image")
        if not file:
            return "No file uploaded", 400

        img = Image.open(file)
        quality = int(request.form.get("quality", 80))
        max_size = int(request.form.get("max_size", 500))
        output_format = request.form.get("format", "webp")

        compressed_bytes = compress_image_in_memory(
            img,
            output_quality=quality,
            output_format=output_format,
            max_size_kb=max_size
        )

        # Return compressed image for download
        return send_file(
            compressed_bytes,
            as_attachment=True,
            download_name=f"compressed.{output_format}",
            mimetype=f"image/{output_format}"
        )

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")