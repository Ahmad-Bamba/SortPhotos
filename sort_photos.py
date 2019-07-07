#!/usr/bin/python3

from PIL import Image
from pathlib import Path
import os
import glob
import sys
import ntpath

def get_year(image_path):
    raw = Image.open(image_path)._getexif()
    return raw[36867][0:4] if (raw is not None) else "0000"

def main():
    cwd = os.getcwd()
    print(f"Working from {cwd}...\n\n")

    # Get some kind of representation of every .png, .jpg, and .jpeg file in the directory
    images = glob.glob(str(Path(cwd + "/**/*.jpg")), recursive=True) + glob.glob(str(Path(cwd + "/**/*.jpeg")), recursive=True) \
        + glob.glob(str(Path(cwd + "/**/*.png")), recursive=True) + glob.glob(str(Path(cwd + "/**/*.JPG")), recursive=True) \
        + glob.glob(str(Path(cwd + "/**/*.JPEG")), recursive=True) + glob.glob(str(Path(cwd + "/**/*.PNG")), recursive=True)
    print(f"Found {len(images)} images!")

    for image in images:
        # extract year from image
        year = get_year(image)
        if year == "0000":
            year = "Other"
        if (not os.path.isdir(cwd + "/" + year)):
            os.mkdir(year)

        os.rename(image, str(Path(cwd) / year / ntpath.basename(image)))
        print(".")
    
    # Print exit message
    print("\n\n...Done!")


if __name__ == '__main__':
    main()
    sys.exit()
