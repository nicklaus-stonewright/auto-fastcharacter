import os
from PyPDF2 import PdfMerger

def merge_pdfs(pdf_list, output_path):
    merger = PdfMerger()
    for pdf in pdf_list:
        merger.append(pdf)
    merger.write(output_path)
    merger.close()
    print(f"Merged PDF saved as: {output_path}")

# Example usage
if __name__ == "__main__":
    # List your PDFs in the order you want them merged
    pdf_files = [
        # "merged_characters_lvl3_output.pdf",
        # "merged_characters_lvl4_output.pdf",
        "C:/LocalApplications/auto-fastcharacter/character_pdfs/_archive/pre-gens 5e 2024/merged_characters_lvl5_output.pdf",
        "C:/LocalApplications/auto-fastcharacter/character_pdfs/_archive/pre-gens 5e 2024/merged_characters_lvl7_output.pdf",
        "C:/LocalApplications/auto-fastcharacter/character_pdfs/_archive/pre-gens 5e 2024/merged_characters_lvl9_output.pdf",
        "C:/LocalApplications/auto-fastcharacter/character_pdfs/_archive/spells/dnd-5e-2024-druid.pdf",
        "C:/LocalApplications/auto-fastcharacter/character_pdfs/_archive/spells/dnd-5e-2024-paladin.pdf",
        "C:/LocalApplications/auto-fastcharacter/character_pdfs/_archive/spells/dnd-5e-2024-sorcerer.pdf",
        "C:/LocalApplications/auto-fastcharacter/character_pdfs/_archive/spells/dnd-5e-2024-warlock.pdf",
        "C:/LocalApplications/auto-fastcharacter/character_pdfs/_archive/spells/dnd-5e-2024-cleric.pdf",
        "C:/LocalApplications/auto-fastcharacter/character_pdfs/_archive/blank_padding_pdf.pdf",
        "C:/LocalApplications/auto-fastcharacter/character_pdfs/_archive/spells/dnd-5e-2024-ranger.pdf",
        "C:/LocalApplications/auto-fastcharacter/character_pdfs/_archive/blank_padding_pdf.pdf",
        "C:/LocalApplications/auto-fastcharacter/character_pdfs/_archive/spells/dnd-5e-2024-bard.pdf",
        "C:/LocalApplications/auto-fastcharacter/character_pdfs/_archive/blank_padding_pdf.pdf",
        "C:/LocalApplications/auto-fastcharacter/character_pdfs/_archive/spells/dnd-5e-2024-wizard.pdf",
        "C:/LocalApplications/auto-fastcharacter/character_pdfs/_archive/blank_padding_pdf.pdf",
    ]

    # Output file name
    output_file = 'C:/LocalApplications/auto-fastcharacter/character_pdfs/merged_output.pdf'

    # Merge PDFs
    merge_pdfs(pdf_files, output_file)
