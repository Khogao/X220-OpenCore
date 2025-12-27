import os
from pypdf import PdfReader

def extract_pdf_to_md(pdf_path, md_path):
    try:
        reader = PdfReader(pdf_path)
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(f"# Extracted Content from {os.path.basename(pdf_path)}\n\n")
            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                if text:
                    f.write(f"## Page {i+1}\n\n")
                    f.write(text)
                    f.write("\n\n---\n\n")
        print(f"Successfully extracted to {md_path}")
    except Exception as e:
        print(f"Error extracting PDF: {e}")

if __name__ == "__main__":
    pdf_file = r"C:\Users\Phi\OneDrive\Documents\GitHub\X220-OpenCore\Updates\OpenCore_Extracted\Docs\Configuration.pdf"
    md_file = r"C:\Users\Phi\OneDrive\Documents\GitHub\X220-OpenCore\Updates\OpenCore_Configuration.md"
    extract_pdf_to_md(pdf_file, md_file)
