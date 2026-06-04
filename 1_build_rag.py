import os
import json
from pypdf import PdfReader

def extract_raw_text_from_pdf(pdf_path: str) -> str:
    """Extracts all text from a PDF document safely page-by-page."""
    try:
        reader = PdfReader(pdf_path)
        full_text = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                full_text.append(f"--- PAGE {i+1} ---\n{text}")
        return "\n\n".join(full_text)
    except Exception as e:
        return f"[ERROR] Unreadable PDF file: {e}"

def extract_raw_text_from_md(md_path: str) -> str:
    """Reads a text-based Markdown file directly using standard encoding."""
    try:
        with open(md_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        return f"[ERROR] Unreadable Markdown file: {e}"

def run_ingestion(parent_dir: str, rag_json_path: str):
    database = {}
    if not os.path.exists(parent_dir):
        print(f"[Error] Target directory '{parent_dir}' does not exist.")
        return

    print(f"Indexing shipment files (.pdf & .md) into local RAG store from: '{parent_dir}'")
    
    for root, _, files in os.walk(parent_dir):
        for file in files:
            file_lower = file.lower()
            
            # Match both PDF and Markdown files
            if file_lower.endswith('.pdf') or file_lower.endswith('.md'):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, parent_dir)
                
                # Determine file type and execute matching extraction pipeline
                if file_lower.endswith('.pdf'):
                    print(f" -> [PDF] Extracting: {rel_path}")
                    extracted_text = extract_raw_text_from_pdf(full_path)
                    
                    # Run safety check for unrendered interactive XFA forms
                    if "Please wait... If this message is not eventually replaced" in extracted_text:
                        status = "XFA_RENDER_ERROR"
                    elif not extracted_text.strip():
                        status = "EMPTY_OR_SCANNED_PDF"
                    else:
                        status = "SUCCESS"
                        
                elif file_lower.endswith('.md'):
                    print(f" -> [MD]  Reading: {rel_path}")
                    extracted_text = extract_raw_text_from_md(full_path)
                    
                    if not extracted_text.strip():
                        status = "EMPTY_MARKDOWN"
                    else:
                        status = "SUCCESS"

                # Commit entry to the unified RAG database object
                database[rel_path] = {
                    "file_name": file,
                    "relative_path": rel_path,
                    "file_type": "PDF" if file_lower.endswith('.pdf') else "MARKDOWN",
                    "status": status,
                    "raw_text": extracted_text
                }

    # Write out the structural text database
    with open(rag_json_path, 'w', encoding='utf-8') as f:
        json.dump(database, f, indent=4, ensure_ascii=False)
        
    print(f"\nRAG Database initialized with {len(database)} total indexed files.")

if __name__ == "__main__":
    TEST_DIRECTORY = r"C:\Users\Jason\Projects\zCompleted-Shipment-Test-BA3087"
    run_ingestion(TEST_DIRECTORY, "rag_database.json")