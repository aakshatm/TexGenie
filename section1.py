import fitz  # PyMuPDF

def extract_sections_with_text(pdf_path):
    pdf_document = fitz.open(pdf_path)
    sections = []

    for page_number in range(len(pdf_document)):
        page = pdf_document[page_number]
        blocks = page.get_text("dict")["blocks"]  # Extract text as a dictionary of blocks
        
        current_section = None
        section_text = []

        for block in blocks:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    font_size = span["size"]
                    text = span["text"]

                    # Heuristic to detect headings: larger font size or bold text
                    if font_size > 12 or span.get("flags", 0) & 2:
                        if current_section:
                            # Save the current section and its text
                            sections.append({"section": current_section, "text": "\n".join(section_text)})
                        
                        # Start a new section
                        current_section = text.strip()
                        section_text = []
                    else:
                        # Append text to the current section
                        section_text.append(text.strip())
        
        # Add the last section on the page
        if current_section:
            sections.append({"section": current_section, "text": "\n".join(section_text)})

    return sections

# Example usage
pdf_path = "AOD.pdf"  # Replace with your PDF path
sections = extract_sections_with_text(pdf_path)

# Print sections and their texts
for section in sections:
    print(f"Section: {section['section']}")
    print(f"Text: {section['text']}")
    print("-" * 50)
