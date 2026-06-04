import os
import json
from pypdf import PdfReader

def extract_raw_text(pdf_path: str) -> str:
    """Extracts text from all pages of a PDF document securely."""
    try:
        reader = PdfReader(pdf_path)
        full_text = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                full_text.append(f"--- PAGE {i+1} ---\n{text}")
        return "\n\n".join(full_text)
    except Exception as e:
        return f"[ERROR] Unreadable file: {e}"

def run_ingestion(parent_dir: str, rag_json_path: str):
    database = {}
    if not os.path.exists(parent_dir):
        print(f"[Error] Target directory '{parent_dir}' does not exist.")
        return

    print(f"Indexing test shipment folder into local RAG store: '{parent_dir}'")
    for root, _, files in os.walk(parent_dir):
        for file in files:
            if file.lower().endswith('.pdf'):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, parent_dir)
                
                print(f" -> Extracting: {rel_path}")
                extracted_text = extract_raw_text(full_path)
                
                if "Please wait... If this message is not eventually replaced" in extracted_text:
                    status = "XFA_RENDER_ERROR"
                elif not extracted_text.strip():
                    status = "EMPTY_OR_SCANNED"
                else:
                    status = "SUCCESS"

                database[rel_path] = {
                    "file_name": file,
                    "relative_path": rel_path,
                    "status": status,
                    "raw_text": extracted_text
                }

    with open(rag_json_path, 'w', encoding='utf-8') as f:
        json.dump(database, f, indent=4, ensure_ascii=False)
    print(f"\nRAG Database initialized with {len(database)} indexed files.")

if __name__ == "__main__":
    TEST_DIRECTORY = r"C:\Users\Jason\Projects\zCompleted-Shipment-Test-BA3087"
    run_ingestion(TEST_DIRECTORY, "rag_database.json")