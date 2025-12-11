from PIL import Image
import os, sys

IMAGE_DIR_PATH = ''

if len(sys.argv) != 2:
  print("Usage: ")
  print(sys.argv[0] + " /IMAGE/DIRECTORY/DIR")
  exit(0)
else:
  len(sys.argv) == 2:
  IMAGE_DIR_PATH = sys.argv[1]


def merge_pngs_to_pdf(png_files, pdf_file):
  if not png_files:
    print("No PNG files provided.")
    return

  images = []
  for file_path in png_files:
    im = Image.open(file_path)
    images.append(im)
    # Save the first image, appending the rest
  images[0].save(pdf_file, "PDF", resolution=300.0, \
                 save_all=True, append_images=images[1:])
  print(f"Saved PDF to: {pdf_file}")

image_files = sorted(os.listdir(IMAGE_DIR_PATH))
image_files = list(filter(lambda x: ".png" in x, image_files))
image_files = [(lambda x: os.path.join(IMAGE_DIR_PATH, x))(a) for a in image_files]

output_pdf_name = os.path.join(IMAGE_DIR_PATH, 'merged.pdf')

merge_pngs_to_pdf(image_files, output_pdf_name)