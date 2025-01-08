import pdfplumber

def extract_sections_with_pdfplumber(pdf_path):
    sections = []
    current_section = None
    section_text = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages):
            text = page.extract_text()
            lines = text.split("\n")

            for line in lines:
                # Heuristic to detect section headings: capitalize or numbered patterns
                if line.isupper() or line.strip().endswith(":"):
                    if current_section:
                        # Save the current section and its text
                        sections.append({"section": current_section, "text": "\n".join(section_text)})

                    # Start a new section
                    current_section = line.strip()
                    section_text = []
                else:
                    # Append text to the current section
                    section_text.append(line.strip())

        # Add the last section
        if current_section:
            sections.append({"section": current_section, "text": "\n".join(section_text)})

    return sections

# Example usage
pdf_path = "sample.pdf"  # Replace with your PDF path
sections = extract_sections_with_pdfplumber(pdf_path)

# Print sections and their texts
for section in sections:
    print(f"Section: {section['section']}")
    print(f"Text: {section['text']}")
    print("-" * 50)
