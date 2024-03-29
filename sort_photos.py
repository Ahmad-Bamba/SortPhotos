#!/usr/bin/python3

from PIL import Image
from pathlib import Path
import os
import glob
import sys
import ntpath

def get_year(image_path):
    try:
        raw = Image.open(image_path)._getexif()
        return raw[36867][0:4] if (raw is not None) else "0000"
    except KeyError:
        print(f"Somehow, the key didnt work for image at {image_path}")
        return "0000"
    except OSError:
        print(f"The image at {image_path} could not be identified!")
        return "IDEN"
    except SyntaxError:
        print(f"The image at {image_path} has an invalid TIFF header! Ignoring...")
        return "IDEN"
    except AttributeError:
        print(f"The image at {image_path} has no EXIF data!")
        return "0000"
    except:
        print("Something else went wrong :(")
        return "IDEN"


def main():
    print("This may permenently alter the file organisation of this folder. Continue? Y/n:", end='')
    response = input('')
    if not (len(response) == 0 or response.lower()[0] == 'y'):
        sys.exit()
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
        if year == "IDEN":
            continue

        if (not os.path.isdir(cwd + "/" + year)):
            os.mkdir(year)

        # rename file just in case 2 files exist in the tree with the same name and year
        newpath = Path(cwd) / year / ntpath.basename(image)
        if os.path.exists(str(newpath)):
            append = 0
            newnewpath_str = str(newpath)
            while True:
                extension_split = str(newpath).split('.', 1)
                newnewpath_str = extension_split[0] + "_" + str(append) + "." + extension_split[1]
                if os.path.exists(newnewpath_str):
                    append += 1
                    continue
                else:
                    break

            newpath = Path(newnewpath_str)

        os.rename(image, str(newpath))
        print(".")
    
    # Print exit message
    print("\n\n...Done!")


if __name__ == '__main__':
    main()
    sys.exit()
