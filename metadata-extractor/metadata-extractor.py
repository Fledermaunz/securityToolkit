import exifread
import argparse
import os
import logging

def setup_logging(verbose=False):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level, 
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

def get_tag_value(tags, tag_name):
    return str(tags.get(tag_name, "Not found"))

def convert_to_degrees(value):
    d = float(value.values[0].num) / float(value.values[0].den)
    m = float(value.values[1].num) / float(value.values[1].den)
    s = float(value.values[2].num) / float(value.values[2].den)

    return d + (m / 60.0) + (s / 3600.0)

def extract_gps_info(tags):
    gps_latitude = tags.get("GPS GPSLatitude")
    gps_latitude_ref = tags.get("GPS GPSLatitudeRef")
    gps_longitude = tags.get("GPS GPSLongitude")
    gps_longitude_ref = tags.get("GPS GPSLongitudeRef")

    if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
        lat = convert_to_degrees(gps_latitude)
        lon = convert_to_degrees(gps_longitude)

        if str(gps_latitude_ref) != "N":
            lat = -lat
        if str(gps_longitude_ref) != "E":   
            lon = -lon

        return lat, lon

    return None, None

def extract_metadata(file_path, logger):
    logger.debug(f"Checking file path: {file_path}")

    if not os.path.isfile(file_path):
        logger.error(f"File {file_path} does not exist.")
        return None
    
    logger.info("Opening image file")
    with open(file_path, "rb") as image_file:
        logger.info("Reading EXIF metadata")
        tags = exifread.process_file(image_file)

    if not tags:
        logger.warning("No metadata found in the image.")
        return None

    make = get_tag_value(tags, "Image Make")
    model = get_tag_value(tags, "Image Model")
    data_taken = get_tag_value(tags, "EXIF DateTimeOriginal")
    software = get_tag_value(tags, "Image Software")
    lat, lon = extract_gps_info(tags)

    metadata = {
        "file": file_path,
        "camera_make": make,
        "camera_model": model,
        "date_taken": data_taken,
        "software": software,
        "gps_latitude": lat,
        "gps_longitude": lon    
    }

    logger.debug(f"Extracted metadata: {metadata}")
    return metadata
    
def print_metadata(metadata):
    print("\n=== Metadata Extractor===")
    print(f"File: {metadata['file']}\n")
    print(f"Camera Make: {metadata['camera_make']}")
    print(f"Camera Model: {metadata['camera_model']}")
    print(f"Date Taken: {metadata['date_taken']}")
    print(f"Software: {metadata['software']}")

    if metadata['gps_latitude'] is not None and metadata['gps_longitude'] is not None:
        print(f"GPS Latitude: {metadata['gps_latitude']}")
        print(f"GPS Longitude: {metadata['gps_longitude']}")
        print(
            f"Google Maps Link: https://www.google.com/maps?q="
            f"{metadata['gps_latitude']},{metadata['gps_longitude']}"
        )
    else:
        print("GPS Data: Not found")

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Extract useful EXIF metadata from an image file."
    )

    parser.add_argument(
        "-f",
        "--file",
        required=True,
        help="Path to the image file"
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose logging for debugging"
    )

    return parser.parse_args()

def main():
    args = parse_arguments()
    logger = setup_logging(args.verbose)

    metadata = extract_metadata(args.file, logger)

    if metadata is None:
        return
    
    print_metadata(metadata)


if __name__ == "__main__":
    main()