import pdfplumber
import csv
import os

def extract_tables_with_pdfplumber(pdf_path, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages):
            tables = page.extract_tables()

            for table_index, table in enumerate(tables):
                output_csv = os.path.join(output_folder, f"table_page_{page_number + 1}_{table_index + 1}.csv")
                # Write table to CSV
                with open(output_csv, mode="w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerows(table)

                print(f"Table from Page {page_number + 1}, Table {table_index + 1} saved to {output_csv}.")

# Example usage
pdf_path = "sample.pdf"  # Replace with your PDF path
output_folder = "extracted_tables"
extract_tables_with_pdfplumber(pdf_path, output_folder)
