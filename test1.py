import fitz  # PyMuPDF
import os

def extract_images_from_pdf(pdf_path, output_folder):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Open the PDF file
    pdf_document = fitz.open('sample.pdf')

    image_count = 0
    for page_number in range(len(pdf_document)):
        page = pdf_document[page_number]
        images = page.get_images(full=True)  # Get all images on the page
        print(images)
        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)  # Extract image
            image_bytes = base_image["image"]  # Get the image bytes
            image_ext = base_image["ext"]  # Get the image extension

            # Save the image
            image_count += 1
            image_filename = f"image_{page_number + 1}_{img_index + 1}.{image_ext}"
            image_path = os.path.join(output_folder, image_filename)

            with open(image_path, "wb") as img_file:
                img_file.write(image_bytes)

    print(f"Extraction complete. {image_count} images were saved to {output_folder}.")

# Example usage
pdf_path = "sample.pdf"  # Replace with the path to your PDF file
output_folder = "extracted_images"
extract_images_from_pdf(pdf_path, output_folder)
