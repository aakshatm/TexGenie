import fitz  # PyMuPDF
import os

def extract_images_with_metadata(pdf_path, output_folder):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    image_metadata = []  # List to store metadata

    image_count = 0
    for page_number in range(len(pdf_document)):
        page = pdf_document[page_number]
        images = page.get_images(full=True)  # Get all images on the page

        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)  # Extract image
            image_bytes = base_image["image"]  # Get the image bytes
            image_ext = base_image["ext"]  # Get the image extension

            # Get the bounding box (position) of the image
            for block in page.get_text("dict")["blocks"]:
                if "image" in block:
                    bbox = block["bbox"]  # Bounding box of the image
                    break
            else:
                bbox = None

            # Save the image
            image_count += 1
            image_filename = f"image_{page_number + 1}_{img_index + 1}.{image_ext}"
            image_path = os.path.join(output_folder, image_filename)

            with open(image_path, "wb") as img_file:
                img_file.write(image_bytes)

            # Add metadata to the list
            metadata = {
                "page": page_number + 1,
                "xref": xref,
                "filename": image_filename,
                "bbox": bbox,
                "image_format": image_ext,
            }
            image_metadata.append(metadata)

    print(f"Extraction complete. {image_count} images were saved to {output_folder}.")
    return image_metadata

# Example usage
pdf_path = "sample.pdf"  # Replace with the path to your PDF file
output_folder = "extracted_images"
metadata = extract_images_with_metadata(pdf_path, output_folder)

# Print metadata
for item in metadata:
    print(item)
