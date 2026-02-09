import os
from PyPDF2 import PdfMerger

# Path to your folder containing PDFs
lvl_text = "lvl7"
pdf_folder = f"character_pdfs\{lvl_text}"
output_file = os.path.join(pdf_folder, f"merged_24characters_{lvl_text}_output.pdf")

# Get all PDF files in the folder (sorted alphabetically)
pdf_files = sorted([f for f in os.listdir(pdf_folder) if f.lower().endswith(".pdf")])

# Initialize the merger
merger = PdfMerger()

# Merge them all
for pdf in pdf_files:
    full_path = os.path.join(pdf_folder, pdf)
    merger.append(full_path)
    print(f"Merged: {pdf}")

# Write output
merger.write(output_file)
merger.close()

print(f"\nMerged PDF saved as: {output_file}")
