import exifread
import argparse
import os

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

def extract_metadata(file_path):
    if not os.path.isfile(file_path):
        print(f"File {file_path} does not exist.")
        return
    
    with open(file_path, "rb") as image_file:
        tags = exifread.process_file(image_file)

        if not tags:
            print("No metadata found.")
            return

        print("\n=== Metadata Extractor===")
        print(f"File: {file_path}\n")

        make = get_tag_value(tags, "Image Make")
        model = get_tag_value(tags, "Image Model")
        data_taken = get_tag_value(tags, "EXIF DateTimeOriginal")
        software = get_tag_value(tags, "Image Software")

        print(f"Camera Make: {make}")
        print(f"Camera Model: {model}")
        print(f"Date Taken: {data_taken}")
        print(f"Software: {software}")

        lat, lon = extract_gps_info(tags)

        if lat is not None and lon is not None:
            print(f"GPS Latitude: {lat}")
            print(f"GPS Longitude: {lon}")
            print(f"Google Maps Link: https://www.google.com/maps/search/?api=1&query={lat},{lon}")
        else:
            print("GPS Data: Not found")



def main():
    parser = argparse.ArgumentParser(
        description="Extract metadata from image"
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