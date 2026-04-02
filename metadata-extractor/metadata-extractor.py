import exifread
import argparse
import os

def extract_metadata(file_path):
    if not os.path.isfile(file_path):
        print(f"File {file_path} does not exist.")
        return
    
    with open(file_path, "rb") as image_file:
        tags = exifread.process_file(image_file)

        if not tags:
            print("No metadata found.")
            return

        found = False

        for tag in tags.keys():
            if tag not in ("JPEGThumbnail", "TIFFThumbnail"):
                print(f"{tag}: {tags[tag]}")

def main():
    parser = argparse.ArgumentParser(
        description="Extract metadata from images"
    )

    parser.add_argument(
        "-f",
        "--file",
        required=True,
        help="Path to image file"
    )

    args = parser.parse_args()

    extract_metadata(args.file)

if __name__ == "__main__":
    main()