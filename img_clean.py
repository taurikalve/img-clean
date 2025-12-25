import os
import argparse
from pathlib import Path
from PIL import Image
from tqdm import tqdm


def process_images(input_path, output_dir=None, compress=True):
    # Handle globbing or single file
    p = Path(input_path)
    files = (
        list(p.parent.glob(p.name))
        if "*" in input_path
        else ([p] if p.is_file() else list(p.glob("*.png")))
    )

    if not files:
        print(f"No files found for: {input_path}")
        return

    # Create output directory
    if output_dir:
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)
    else:
        # Default to a 'clean' folder relative to the first file
        out_path = files[0].parent / "clean"
        out_path.mkdir(exist_ok=True)

    print(f"Processing {len(files)} images...")
    print(f"Output folder: {out_path.resolve()}")

    for file_path in tqdm(files, unit="img"):
        try:
            with Image.open(file_path) as img:
                # 1. Convert to RGB if needed (strips some alpha weirdness, optional)
                # img = img.convert('RGB')

                # 2. Create a new filename
                new_filename = file_path.name
                save_path = out_path / new_filename

                # 3. Save without metadata
                # Pillow does NOT save PngInfo/metadata by default unless you pass it.
                # optimize=True enables generic PNG compression (smaller size, no quality loss)
                img.save(save_path, "PNG", optimize=compress)

        except Exception as e:
            print(f"Error processing {file_path.name}: {e}")

    print("Done! ✨")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Strip metadata and optimize PNGs for upload."
    )
    parser.add_argument(
        "input", help="Input file or pattern (e.g. *.png or path/to/dir)"
    )
    parser.add_argument("-o", "--output", help="Output directory (default: ./clean)")
    parser.add_argument(
        "--no-compress",
        action="store_true",
        help="Disable PNG optimization (faster save)",
    )

    args = parser.parse_args()

    process_images(args.input, args.output, not args.no_compress)
