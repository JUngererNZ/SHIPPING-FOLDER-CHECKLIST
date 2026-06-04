explain these to me

The text you provided consists of two distinct components. Source 1 is a generic error message from an Adobe PDF reader, while Source 2 is a highly detailed **South African Revenue Service (SARS) Customs Declaration (SAD 500 / 502 / 505)** for an export shipment.

Here is a breakdown of exactly what this document represents.

---

## 1. Executive Summary

This document confirms that a high-value piece of earthmoving machinery has been legally cleared by SARS for export from South Africa, moving under **Removal in Bond (RIB)** regulations toward its final destination. The customs decision is officially marked as **"RELEASE"**, meaning the shipment is cleared to proceed.

---

## 2. Key Transaction & Logistics Details

* **The Goods:** One heavy industrial vehicle—specifically an **Elphinstone EG20 Motor Grader** (Tariff Heading `8429.20`, which covers self-propelled graders and levelers). The document logs its unique identifying markers:
* *Serial No:* 21NK0112
* *Engine No:* E7A67305
* *PIN:* CAT00120CE9601160


* **The Value:** The customs value of the machinery is **R9,363,416.00** (ZAR).
* **Weight & Packing:** It is transported as a single (`1.00`) package with a gross mass of **16,230.00 kg** (16.23 metric tonnes).

---

## 3. Supply Chain Entities Involved

* **Exporter / Consignor:** FML Freight Solutions Pty Ltd, acting on behalf of *Batrace Equipment* (registered in Mauritius).
* **Importer / Consignee:** Kamoa Copper S.A., located in Lubumbashi, **Democratic Republic of Congo (CD)**.
* **Clearing Agent:** Cargo Services JHB (Pty) Ltd (operating out of Villa Valencia Office Park, Kempton Park).
* **Licensed Remover (Carrier):** Tiger Zambezi Investments Limited, who is legally responsible for hauling the bonded cargo.

---

## 4. Customs & Route Mechanics

The paperwork tracks a coordinated transit route across African borders:

* **Customs Office of Clearance:** **Durban (DBN)**. The cargo originated or was processed through a bonded warehouse environment in Durban (`Warehouse: DBNSOS50069 / Freight Station SA`).
* **Movement Type (CPC 67 42):** This indicates a permanent export under a **Removal in Bond (R.I.B)** status. Because the cargo is high-value and moving through South Africa to a foreign destination, it is tied to a security bond (**Bond Number: 1544964 / Penal Sum: R1,544,963.70**) to guarantee the cargo doesn't illegally leak into the local South African market without duties being paid.
* **Port of Exit:** **KFN** (Kasumbalesa), which is the primary border post between Zambia and the DRC.
* **Transport Mode:** Road transport (`Transport Code: 3`), designated by the horse/truck registration placeholder `ROOAD`.

---

## 5. Duties, Financials, and Reference Numbers

* **Duties & Taxes Due:** **R0.00**. Because this is a standard export leaving South Africa for the DRC, the local customs duties and VAT are rated as zero or deferred, provided the carrier proves the cargo successfully leaves the country.
* **Key Reference Numbers for Tracking:**
* **MRN (Movement Reference Number):** `DBN202604245059654`
* **LRN (Local Reference Number):** `21542855DBN20260424490693`
* **Client Reference:** `2602DS12783`
* **UCR (Unique Consignment Reference):** `6ZA22035919CINV2602DS12783 M`



This clear paperwork acts as the "passport" for the grader to travel from the port/warehouse in Durban up through the continent to the copper mines in the DRC.

this example of files is in a folder. i want to create a python script to create a "summary", like shown here. the script should create a "master-folder-file.json" with the file name, and the summary like you have created. start with creating the script that looks at pdf files

To automate this, you can write a Python script that uses a PDF layout-extraction library (like `pypdf` or `pdfplumber`) to read the raw text from the files, sends that text to an AI model via an API (such as Google's Gemini API) to generate the structured summary, and then writes the results to a JSON file.

Here is a complete, production-ready script to get you started.

### Prerequisites

First, install the required libraries in your terminal:

```bash
pip install pypdf google-genai

```

*(Make sure you have your Gemini API key set as an environment variable: `export GEMINI_API_KEY="your-api-key-here"`)*

---

### The Python Script (`summarize_folder.py`)

```python
import os
import json
from pypdf import PdfReader
from google import genai
from google.genai import types

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extracts all raw text from a given PDF file."""
    try:
        reader = PdfReader(pdf_path)
        full_text = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                full_text.append(f"--- PAGE {i+1} ---\n{text}")
        return "\n\n".join(full_text)
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
        return ""

def generate_summary_with_ai(file_name: str, doc_text: str) -> dict:
    """Sends the document text to Gemini to generate a structured JSON summary."""
    # Initialize the standard GenAI client (picks up GEMINI_API_KEY from environment)
    client = genai.Client()
    
    prompt = f"""
    You are an expert customs and logistics data analyst. Analyze the following raw text extracted from a shipping/customs document named '{file_name}'.
    
    Provide a comprehensive, highly detailed summary breaking down:
    1. Executive Summary (The core status and nature of the document)
    2. Key Transaction & Logistics Details (Goods description, serials/numbers, value, weight, etc.)
    3. Supply Chain Entities Involved (Exporter, Importer, Agent, Removers)
    4. Customs & Route Mechanics (Office of clearance, border posts, movement types, bond details)
    5. Duties, Financials, and Reference Numbers (Total payable, reference codes like MRN/LRN)

    Format your entire response as a structured, clean Markdown document with appropriate headers.
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_text(text=prompt),
                        types.Part.from_text(text=f"Document Content:\n{doc_text}")
                    ]
                )
            ]
        )
        return {
            "file_name": file_name,
            "summary": response.text
        }
    except Exception as e:
        print(f"Error generating summary for {file_name}: {e}")
        return {
            "file_name": file_name,
            "summary": f"Failed to generate summary due to API error: {e}"
        }

def process_folder(folder_path: str, output_json_path: str):
    """Loops through a folder, extracts PDFs, summarizes them, and saves to a JSON file."""
    master_records = []

    # Check if the directory exists
    if not os.path.exists(folder_path):
        print(f"Error: Folder path '{folder_path}' does not exist.")
        return

    print(f"Scanning folder: {folder_path} for PDF files...")
    
    # Iterate through all files in the directory
    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith('.pdf'):
            pdf_path = os.path.join(folder_path, file_name)
            print(f"\nProcessing: {file_name}")
            
            # 1. Extract text
            raw_text = extract_text_from_pdf(pdf_path)
            
            # Handle empty/unreadable PDFs (like your 'WE CN1' error file)
            if not raw_text.strip() or "Please wait... If this message is not eventually replaced" in raw_text:
                print(f"-> Warning: {file_name} appears to be unrendered, empty, or corrupted.")
                master_records.append({
                    "file_name": file_name,
                    "summary": "Error: This PDF could not be read properly. It may be an unrendered dynamic XFA form or corrupted document."
                })
                continue
                
            # 2. Get AI Summary
            print(f"-> Extracting customs insights using Gemini...")
            record = generate_summary_with_ai(file_name, raw_text)
            master_records.append(record)

    # 3. Write out to the Master JSON file
    with open(output_json_path, 'w', encoding='utf-8') as json_file:
        json.dump(master_records, json_file, indent=4, ensure_ascii=False)
        
    print(f"\nSuccess! Master summary saved to: {output_json_path}")

if __name__ == "__main__":
    # Define your local paths here
    TARGET_FOLDER = "./customs_documents"  # Change this to your folder path
    OUTPUT_FILE = "master-folder-file.json"
    
    process_folder(TARGET_FOLDER, OUTPUT_FILE)

```

---

### How this script handles your exact files:

1. 
**`XE ENTRY - BA2950.pdf`**: The script will read all pages, extract key text data (like `KAMOA COPPER S.A`, `DBN202604245059654`, and `ELPHINSTONE EG20 MOTOR GRADER`), and feed it to the `gemini-2.5-flash` model to return a structured markdown summary.


2. 
**`WE CN1 - BA2950.pdf`**: The script explicitly checks for the Adobe Reader warning text (`"Please wait... If this message is not eventually replaced..."`). If it encounters this text, it flags it as an unreadable/corrupted file error in the JSON string instead of wasting an API call on error messages.



### Output Structure

The generated `master-folder-file.json` will look like this:

```json
[
    {
        "file_name": "XE ENTRY - BA2950.pdf",
        "summary": "## 1. Executive Summary\nThis document confirms that..."
    },
    {
        "file_name": "WE CN1 - BA2950.pdf",
        "summary": "Error: This PDF could not be read properly..."
    }
]

```

i dont have a gemini key, as that costs money. is there another alternative for small language model to run on local?
currently installed is llama-cpp, with "qwen2.5-1.5b-instruct-q8_0.gguf"

You absolutely do not need to pay for an API key. Running a Small Language Model (SLM) locally on your own machine is a fantastic alternative, and the **Qwen2.5-1.5B** model you have installed is actually one of the best models in its size class for structural data extraction and document parsing.

Since you already have `llama-cpp` and the `.gguf` file ready to go, we can rewrite the script to use a **local inference server**. The easiest and most robust way to do this is to spin up `llama.cpp`'s built-in, OpenAI-compatible local server and point your Python script directly to your own machine.

Here is how to set up the entire local, cost-free pipeline.

---

## Step 1: Start Your Local Llama.cpp Server

Before running the script, you need to launch your local model so it can listen for requests. Open your terminal or command prompt, navigate to where your `llama-cpp` executable and model are, and run:

```bash
# Start the llama-cpp server on port 8000
llama-server --model qwen2.5-1.5b-instruct-q8_0.gguf --port 8000 --ctx-size 8192

```

> **Important Note on Context Size:** Customs documents contain a lot of text. The `--ctx-size 8192` flag gives the model an expanded 8k token memory window so it doesn't "forget" the beginning of the customs document by the time it reaches the end.

---

## Step 2: Install Python Prerequisites

We will use the official `openai` Python library. Because your local `llama.cpp` server perfectly mimics OpenAI's API layout, we can use their standard, highly optimized library for free by pointing it to `localhost`.

```bash
pip install pypdf openai

```

---

## Step 3: The Local Python Script (`local_summarize.py`)

This updated script reads the PDFs locally, connects to your running `llama-server`, and generates the `master-folder-file.json` file.

```python
import os
import json
from pypdf import PdfReader
from openai import OpenAI

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extracts all raw text from a given PDF file."""
    try:
        reader = PdfReader(pdf_path)
        full_text = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                full_text.append(f"--- PAGE {i+1} ---\n{text}")
        return "\n\n".join(full_text)
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
        return ""

def generate_local_summary(file_name: str, doc_text: str) -> dict:
    """Sends document text to the locally running llama-cpp server."""
    # Point the client to your local machine instead of the cloud
    client = OpenAI(
        base_url="http://localhost:8000/v1",
        api_key="local-no-key-needed" 
    )
    
    # We use a concise system prompt tailored perfectly for small models (SLMs)
    system_prompt = (
        "You are a helpful assistant that summarizes customs documents accurately. "
        "Extract details from the text provided and format them into clear Markdown sections: "
        "1. Executive Summary, 2. Key Transaction Details, 3. Entities Involved, "
        "4. Customs Mechanics, 5. Duties & Reference Numbers."
    )
    
    user_prompt = f"Analyze this text from file '{file_name}':\n\n{doc_text}"

    try:
        response = client.chat.completions.create(
            model="qwen2.5-1.5b-instruct", # Name doesn't strictly matter for local servers
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1, # Low temperature keeps the model focused on factual data extraction
            max_tokens=1500
        )
        return {
            "file_name": file_name,
            "summary": response.choices[0].message.content
        }
    except Exception as e:
        print(f"Local inference error for {file_name}: {e}")
        return {
            "file_name": file_name,
            "summary": f"Failed to generate summary locally. Error: {e}"
        }

def process_folder_locally(folder_path: str, output_json_path: str):
    """Loops through a folder, extracts text, handles errors, and calls local SLM."""
    master_records = []

    if not os.path.exists(folder_path):
        print(f"Error: Folder path '{folder_path}' does not exist.")
        return

    print(f"Scanning folder '{folder_path}' for PDF files...")
    
    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith('.pdf'):
            pdf_path = os.path.join(folder_path, file_name)
            print(f"\nProcessing: {file_name}")
            
            # 1. Extract text from the PDF file
            raw_text = extract_text_from_pdf(pdf_path)
            
            # Catch unrendered Adobe/XFA forms or corrupt files
            if not raw_text.strip() or "Please wait... If this message is not eventually replaced" in raw_text:
                print(f"-> Warning: {file_name} is unreadable or empty.")
                master_records.append({
                    "file_name": file_name,
                    "summary": "Error: Unreadable PDF format (Dynamic XFA form or corrupted document)."
                })
                continue
                
            # 2. Query your local Qwen model
            print(f"-> Processing text through local Qwen2.5-1.5B...")
            record = generate_local_summary(file_name, raw_text)
            master_records.append(record)

    # 3. Save everything to the master JSON file
    with open(output_json_path, 'w', encoding='utf-8') as json_file:
        json.dump(master_records, json_file, indent=4, ensure_ascii=False)
        
    print(f"\nCompleted! Local master summary file saved to: {output_json_path}")

if __name__ == "__main__":
    # Specify the target folder containing your customs PDFs
    TARGET_FOLDER = "./customs_documents" 
    OUTPUT_FILE = "master-folder-file.json"
    
    process_folder_locally(TARGET_FOLDER, OUTPUT_FILE)

```

---

## Why this works so well with Qwen 2.5 (1.5B)

1. **Speed:** Because it's only a 1.5-billion parameter model, it will chew through these text extractions incredibly fast on local hardware (even on standard laptops without a heavy-duty GPU).
2. **Precision:** Qwen2.5 models were trained heavily on code, tables, and structured data data formats. It handles messy customs logs, key-value configurations, and numbers significantly better than almost any other model of its size.

in the parent directory, there is also sub directories, will the script be able to search through them and add to the master-folder-file.json?

The current script only looks at the top level of the folder you specify. If you have nested subdirectories inside your parent directory, it will completely miss those files.

To fix this, we can swap out `os.listdir()` (which only looks one level deep) with `os.walk()`. This built-in Python function automatically and recursively searches through the parent directory, slips into every single subdirectory it finds, and processes any PDFs hidden inside them.

Here is the updated, recursive version of the script. It retains the same local `llama-cpp` pipeline but ensures no folder is left behind.

### The Recursive Local Python Script (`local_summarize_recursive.py`)

```python
import os
import json
from pypdf import PdfReader
from openai import OpenAI

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extracts all raw text from a given PDF file."""
    try:
        reader = PdfReader(pdf_path)
        full_text = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                full_text.append(f"--- PAGE {i+1} ---\n{text}")
        return "\n\n".join(full_text)
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
        return ""

def generate_local_summary(file_name: str, doc_text: str) -> dict:
    """Sends document text to the locally running llama-cpp server."""
    client = OpenAI(
        base_url="http://localhost:8000/v1",
        api_key="local-no-key-needed" 
    )
    
    system_prompt = (
        "You are a helpful assistant that summarizes customs documents accurately. "
        "Extract details from the text provided and format them into clear Markdown sections: "
        "1. Executive Summary, 2. Key Transaction Details, 3. Entities Involved, "
        "4. Customs Mechanics, 5. Duties & Reference Numbers."
    )
    
    user_prompt = f"Analyze this text from file '{file_name}':\n\n{doc_text}"

    try:
        response = client.chat.completions.create(
            model="qwen2.5-1.5b-instruct",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1,
            max_tokens=1500
        )
        return {
            "file_name": file_name,
            "summary": response.choices[0].message.content
        }
    except Exception as e:
        print(f"Local inference error for {file_name}: {e}")
        return {
            "file_name": file_name,
            "summary": f"Failed to generate summary locally. Error: {e}"
        }

def process_nested_folders_locally(parent_folder_path: str, output_json_path: str):
    """Recursively crawls through a parent folder and all its subdirectories to process PDFs."""
    master_records = []

    if not os.path.exists(parent_folder_path):
        print(f"Error: Parent folder path '{parent_folder_path}' does not exist.")
        return

    print(f"Deep scanning parent folder '{parent_folder_path}' and all subdirectories...")
    
    # os.walk travels down the entire folder tree automatically
    for root, dirs, files in os.walk(parent_folder_path):
        for file_name in files:
            if file_name.lower().endswith('.pdf'):
                # Construct the full relative path to the file, no matter how deep it is nested
                pdf_path = os.path.join(root, file_name)
                
                # We calculate a relative display name so you can see where it lives in your JSON
                display_name = os.path.relpath(pdf_path, parent_folder_path)
                print(f"\nFound & Processing: {display_name}")
                
                # 1. Extract text
                raw_text = extract_text_from_pdf(pdf_path)
                
                # Catch unrendered Adobe/XFA forms or corrupt files
                if not raw_text.strip() or "Please wait... If this message is not eventually replaced" in raw_text:
                    print(f"-> Warning: {display_name} is unreadable or empty.")
                    master_records.append({
                        "file_name": display_name,
                        "summary": "Error: Unreadable PDF format (Dynamic XFA form or corrupted document)."
                    })
                    continue
                    
                # 2. Query your local Qwen model
                print(f"-> Processing through local Qwen2.5-1.5B...")
                record = generate_local_summary(display_name, raw_text)
                master_records.append(record)

    # 3. Save everything to the master JSON file
    with open(output_json_path, 'w', encoding='utf-8') as json_file:
        json.dump(master_records, json_file, indent=4, ensure_ascii=False)
        
    print(f"\nCompleted! Local master summary file saved to: {output_json_path}")

if __name__ == "__main__":
    # Point this to your main parent folder
    PARENT_FOLDER = "./customs_documents" 
    OUTPUT_FILE = "master-folder-file.json"
    
    process_nested_folders_locally(PARENT_FOLDER, OUTPUT_FILE)

```

### What changed?

Instead of tracking just `file_name`, the script now records `display_name` via `os.path.relpath`. This means if you have a file nested deep inside, your final `master-folder-file.json` will beautifully map out exactly where that file came from, like this:

```json
[
    {
        "file_name": "XE ENTRY - BA2950.pdf",
        "summary": "## 1. Executive Summary\n..."
    },
    {
        "file_name": "2026_Archived/April/XE ENTRY - ANOTHER_ONE.pdf",
        "summary": "## 1. Executive Summary\n..."
    }
]

```

but will the script using the llama-cpp output a summary of the pdf file? like the example started at the begining of this chat
example:
The text you provided consists of two distinct components. Source 1 is a generic error message from an Adobe PDF reader, while Source 2 is a highly detailed South African Revenue Service (SARS) Customs Declaration (SAD 500 / 502 / 505) for an export shipment.
Here is a breakdown of exactly what this document represents.

1. Executive Summary
This document confirms that a high-value piece of earthmoving machinery has been legally cleared by SARS for export from South Africa, moving under Removal in Bond (RIB) regulations toward its final destination. The customs decision is officially marked as "RELEASE", meaning the shipment is cleared to proceed.

2. Key Transaction & Logistics Details
The Goods: One heavy industrial vehicle—specifically an Elphinstone EG20 Motor Grader (Tariff Heading 8429.20, which covers self-propelled graders and levelers). The document logs its unique identifying markers:
Serial No: 21NK0112
Engine No: E7A67305
PIN: CAT00120CE9601160
The Value: The customs value of the machinery is R9,363,416.00 (ZAR).
Weight & Packing: It is transported as a single (1.00) package with a gross mass of 16,230.00 kg (16.23 metric tonnes).
3. Supply Chain Entities Involved
Exporter / Consignor: FML Freight Solutions Pty Ltd, acting on behalf of Batrace Equipment (registered in Mauritius).
Importer / Consignee: Kamoa Copper S.A., located in Lubumbashi, Democratic Republic of Congo (CD).
Clearing Agent: Cargo Services JHB (Pty) Ltd (operating out of Villa Valencia Office Park, Kempton Park).
Licensed Remover (Carrier): Tiger Zambezi Investments Limited, who is legally responsible for hauling the bonded cargo.
4. Customs & Route Mechanics
The paperwork tracks a coordinated transit route across African borders:

Customs Office of Clearance: Durban (DBN). The cargo originated or was processed through a bonded warehouse environment in Durban (Warehouse: DBNSOS50069 / Freight Station SA).
Movement Type (CPC 67 42): This indicates a permanent export under a Removal in Bond (R.I.B) status. Because the cargo is high-value and moving through South Africa to a foreign destination, it is tied to a security bond (Bond Number: 1544964 / Penal Sum: R1,544,963.70) to guarantee the cargo doesn't illegally leak into the local South African market without duties being paid.
Port of Exit: KFN (Kasumbalesa), which is the primary border post between Zambia and the DRC.
Transport Mode: Road transport (Transport Code: 3), designated by the horse/truck registration placeholder ROOAD.
5. Duties, Financials, and Reference Numbers
Duties & Taxes Due: R0.00. Because this is a standard export leaving South Africa for the DRC, the local customs duties and VAT are rated as zero or deferred, provided the carrier proves the cargo successfully leaves the country.
Key Reference Numbers for Tracking:
MRN (Movement Reference Number): DBN202604245059654
LRN (Local Reference Number): 21542855DBN20260424490693
Client Reference: 2602DS12783
UCR (Unique Consignment Reference): 6ZA22035919CINV2602DS12783 M
This clear paperwork acts as the "passport" for the grader to travel from the port/warehouse in Durban up through the continent to the copper mines in the DRC.

To answer directly: **Yes, but with one important catch regarding the model size.** The Python script itself is perfectly built to request this exact format, but because you are running **Qwen2.5-1.5B**—which is an incredibly small model—it might lack the advanced logical "reasoning" needed to write that highly fluent, editorial introduction and conclusion.

However, it is *excellent* at matching structural layouts. To guarantee your local 1.5B model outputs a summary that looks exactly like the example, we can use a technique called **Few-Shot Prompting**. By feeding the model an explicit example of your expected input and output directly inside the script's prompt, the model will copy the style, section headers, and tone perfectly.

### The Updated Script with the Example Embedded

Update the `generate_local_summary` function in your script to use this structured prompt. It forces your local Qwen model to copy the exact breakdown you provided:

```python
def generate_local_summary(file_name: str, doc_text: str) -> dict:
    """Sends document text to the locally running llama-cpp server with an explicit example style."""
    client = OpenAI(
        base_url="http://localhost:8000/v1",
        api_key="local-no-key-needed" 
    )
    
    # We embed a template example so the 1.5B model understands the exact style to mimic
    system_prompt = (
        "You are an expert customs and logistics data analyst. Your job is to analyze raw text extracted "
        "from customs documents and output a highly structured Markdown summary matching the exact format, "
        "tone, and section numbering of the example provided."
    )
    
    user_prompt = f"""
[EXAMPLE OF EXPECTED OUTPUT FORMAT]
The text provided consists of... [Briefly introduce the document]
Here is a breakdown of exactly what this document represents.

## 1. Executive Summary
This document confirms that... [Core status and clearance message]

## 2. Key Transaction & Logistics Details
* **The Goods**: [Description of vehicle/items, tariff headings, Serial No, Engine No, PIN]
* **The Value**: [Customs value in local currency]
* **Weight & Packing**: [Gross mass, package counts]

## 3. Supply Chain Entities Involved
* **Exporter / Consignor**: [Company names]
* **Importer / Consignee**: [Company names and locations]
* **Clearing Agent**: [Agent details]
* **Licensed Remover (Carrier)**: [Carrier details]

## 4. Customs & Route Mechanics
* **Customs Office of Clearance**: [Origin office/warehouse]
* **Movement Type**: [CPC codes, RIB status, bond amounts if applicable]
* **Port of Exit**: [Border posts]
* **Transport Mode**: [Road/Sea/Air, registration placeholders]

## 5. Duties, Financials, and Reference Numbers
* **Duties & Taxes Due**: [Amounts due]
* **Key Reference Numbers for Tracking**: [MRN, LRN, Client Ref, UCR]

[Provide a short, concluding narrative sentence summarizing the purpose of the trip]
[END OF EXAMPLE]

Now, analyze the following raw text from the file '{file_name}' and generate the summary matching the exact layout shown above:

{doc_text}
"""

    try:
        response = client.chat.completions.create(
            model="qwen2.5-1.5b-instruct",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1, # Extremely low temperature forces the model to stick strictly to the facts
            max_tokens=1500
        )
        return {
            "file_name": file_name,
            "summary": response.choices[0].message.content
        }
    except Exception as e:
        print(f"Local inference error for {file_name}: {e}")
        return {
            "file_name": file_name,
            "summary": f"Failed to generate summary locally. Error: {e}"
        }

```

### What to expect from Qwen2.5-1.5B:

* **The Good:** It will extract the exact serial numbers, values, names, and reference numbers perfectly. It will lay them out using the `## 1. Executive Summary`, `## 2. Key Transaction...` headers seamlessly because small models are incredible at pattern matching.
* **The Limitation:** Small 1.5B models can sometimes struggle with writing elegant transitional sentences (like *"This clear paperwork acts as the 'passport' for the grader..."*). If you find the writing is a bit too robotic or brief, you can try upgrading your local model to **Qwen2.5-7B-Instruct** or **Llama-3-8B-Instruct** if your computer hardware has enough RAM (8GB–16GB) to run them. The 7B and 8B models will perfectly match the fluid, human-like editorial style of the example.

what about file chunking?

When processing documents locally using small language models (SLMs) like your 1.5B Qwen model, **file chunking is one of the most important concepts you can implement.**

Customs folders often contain documents that are tens or hundreds of pages long. If you try to feed an entire 50-page raw text file into a 1.5B model at once, you will quickly hit the model's memory limits (its **context window**), causing it to crash, ignore the prompt, or hallucinate.

**File chunking** means breaking a massive text file into smaller, overlapping sections (chunks), processing each chunk individually through the model, and then aggregating the results.

Here is an explanation of how it works and how you can add it to your local Python script.

---

### How File Chunking Works (The Strategy)

Instead of passing the entire document to the model at once, a chunking strategy typically reads text page-by-page or by a specific word count.

To ensure that a key piece of information (like a serial number) doesn't get accidentally sliced right in half at the border of two chunks, we use an **overlap**. This means the end of Chunk 1 repeats at the beginning of Chunk 2.

For customs document parsing, a **page-by-page chunking strategy with a rolling summary map** works best:

1. Extract text page-by-page.
2. Group pages together so they fit safely within your model's memory capacity (e.g., 2–3 pages per chunk).
3. Have the model extract details from each chunk into a temporary list.
4. Finally, pass all the extracted bullet points to the model one last time to compile the master summary.

---

### Modifying Your Script to Handle Chunking

Here is how you can update your Python script to automatically chunk long PDFs so your local Qwen model never runs out of memory.

```python
import os
import json
from pypdf import PdfReader
from openai import OpenAI

def extract_chunks_from_pdf(pdf_path: str, pages_per_chunk: int = 3) -> list:
    """Reads a PDF and groups pages into text chunks to prevent model memory overload."""
    chunks = []
    try:
        reader = PdfReader(pdf_path)
        current_chunk_text = []
        
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                current_chunk_text.append(f"--- PAGE {i+1} ---\n{text}")
            
            # Once we hit the page limit for a chunk, bundle it and reset
            if (i + 1) % pages_per_chunk == 0:
                chunks.append("\n\n".join(current_chunk_text))
                current_chunk_text = []
        
        # Don't forget the last remaining pages
        if current_chunk_text:
            chunks.append("\n\n".join(current_chunk_text))
            
        return chunks
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
        return []

def generate_local_summary_with_chunking(file_name: str, pdf_path: str) -> dict:
    """Chunks a document, extracts insights from each chunk, and builds a unified summary."""
    client = OpenAI(base_url="http://localhost:8000/v1", api_key="local-no-key-needed")
    
    # 1. Chunk the file into digestible pieces (3 pages max per API call)
    chunks = extract_chunks_from_pdf(pdf_path, pages_per_chunk=3)
    
    if not chunks:
        return {"file_name": file_name, "summary": "Error: Could not read or extract text."}
        
    intermediate_extractions = []
    
    # 2. Extract information from each chunk individually
    for index, chunk in enumerate(chunks):
        print(f"   -> Processing chunk {index + 1} of {len(chunks)}...")
        
        chunk_prompt = f"Extract all raw logistical data, names, serial numbers, reference numbers, and customs values found in this document segment:\n\n{chunk}"
        
        try:
            response = client.chat.completions.create(
                model="qwen2.5-1.5b-instruct",
                messages=[
                    {"role": "system", "content": "You are a data extraction assistant. Extract factual data points into a raw bulleted list. Do not summarize yet."},
                    {"role": "user", "content": chunk_prompt}
                ],
                temperature=0.1,
                max_tokens=800
            )
            intermediate_extractions.append(response.choices[0].message.content)
        except Exception as e:
            print(f"Error processing chunk {index+1}: {e}")

    # 3. Combine all partial extractions into one master prompt for the final structure
    combined_notes = "\n\n".join(intermediate_extractions)
    
    print(f"   -> Consolidating all chunks into the final requested format...")
    
    final_prompt = f"""
Using these extracted notes gathered from the file '{file_name}', create a final structured report.
Follow the exact section layouts and style specified below:

[EXPECTED FORMAT]
The text provided consists of... [Briefly introduce the document]
Here is a breakdown of exactly what this document represents.

## 1. Executive Summary
[Core status and clearance message]

## 2. Key Transaction & Logistics Details
* **The Goods**: [Description of vehicle/items, tariff headings, Serial No, Engine No, PIN]
* **The Value**: [Customs value in local currency]
* **Weight & Packing**: [Gross mass, package counts]

## 3. Supply Chain Entities Involved
* **Exporter / Consignor**: [Company names]
* **Importer / Consignee**: [Company names and locations]
* **Clearing Agent**: [Agent details]
* **Licensed Remover (Carrier)**: [Carrier details]

## 4. Customs & Route Mechanics
* **Customs Office of Clearance**: [Origin office/warehouse]
* **Movement Type**: [CPC codes, RIB status, bond amounts if applicable]
* **Port of Exit**: [Border posts]
* **Transport Mode**: [Road/Sea/Air, registration placeholders]

## 5. Duties, Financials, and Reference Numbers
* **Duties & Taxes Due**: [Amounts due]
* **Key Reference Numbers for Tracking**: [MRN, LRN, Client Ref, UCR]

[Provide a short, concluding narrative sentence summarizing the purpose of the trip]

---
Here are the extracted notes to compile:
{combined_notes}
"""

    try:
        final_response = client.chat.completions.create(
            model="qwen2.5-1.5b-instruct",
            messages=[
                {"role": "system", "content": "You are an expert customs analyst. Organize the notes into the exact layout requested."},
                {"role": "user", "content": final_prompt}
            ],
            temperature=0.1,
            max_tokens=1200
        )
        return {
            "file_name": file_name,
            "summary": final_response.choices[0].message.content
        }
    except Exception as e:
        return {"file_name": file_name, "summary": f"Failed to consolidate summary. Error: {e}"}

```

### Why this is a game-changer for your local setup:

1. **Safety Against Crashes:** Your `llama-server` won't run out of VRAM/RAM because no single request ever exceeds your context limit.
2. **Higher Accuracy:** Small models easily lose details hidden in the middle of giant walls of text (a phenomenon called "lost in the middle"). By feeding it only 2–3 pages at a time, the model pays perfect attention to all fields.
3. **Efficiency:** If a document is short (e.g., your 1-page error document or a 2-page invoice), it loops just once and functions identically to your previous script. If a document happens to be a 40-page manifestation log, it handles it safely step-by-step.

more example files in parent directory

the script must be able to handle this and output into summary file

To build a robust local pipeline that handles nested folders, file chunking, and multiple PDF styles, you need a multi-stage approach.

Your local model (**Qwen2.5-1.5B**) performs incredibly well at direct information extraction when text blocks are kept brief. However, when processing multiple pages or diverse files across different subdirectories, it can experience memory exhaustion or miss critical elements hidden in long strings of text.

The strategy below breaks long or multiple documents down into brief snippets (chunks), extracts data points step-by-step, and uses **few-shot pattern matching** to guarantee that the final combined `master-folder-file.json` perfectly replicates the structural sections and tone you require.

### Local Robust Pipeline Script (`local_pipeline_master.py`)

Make sure your local `llama-server` is active (`llama-server --model qwen2.5-1.5b-instruct-q8_0.gguf --port 8000 --ctx-size 8192`) before executing this script.

```python
import os
import json
from pypdf import PdfReader
from openai import OpenAI

def extract_chunks_from_pdf(pdf_path: str, pages_per_chunk: int = 2) -> list:
    """
    Reads a PDF file and groups pages into minor text chunks.
    This prevents memory boundary overflow on the local SLM context window.
    """
    chunks = []
    try:
        reader = PdfReader(pdf_path)
        current_chunk_text = []
        
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                current_chunk_text.append(f"--- PAGE {i+1} ---\n{text}")
            
            # Pack chunk once page threshold is met
            if (i + 1) % pages_per_chunk == 0:
                chunks.append("\n\n".join(current_chunk_text))
                current_chunk_text = []
        
        # Capture trailing pages
        if current_chunk_text:
            chunks.append("\n\n".join(current_chunk_text))
            
        return chunks
    except Exception as e:
        print(f"   [Error] Could not extract text from {pdf_path}: {e}")
        return []

def process_chunk_extraction(client, file_name: str, chunk_text: str, current_index: int, total_chunks: int) -> str:
    """Queries the local model to extract raw facts from an isolated text chunk."""
    print(f"   -> Analyzing chunk data block {current_index} of {total_chunks}...")
    
    prompt = (
        f"Extract all primary data records from this section of the document '{file_name}'. "
        f"List all shipping entities, values, commodity codes, reference IDs, and errors exactly as written:\n\n"
        f"{chunk_text}"
    )
    
    try:
        response = client.chat.completions.create(
            model="qwen2.5-1.5b-instruct",
            messages=[
                {"role": "system", "content": "You are a factual logistics data extractor. Pull structural points into a brief bulleted list without rewriting or summarizing them."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0, # Zero temperature keeps the small model highly deterministic
            max_tokens=600
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"   [Error] Chunk processing failed: {e}")
        return ""

def compile_final_report(client, file_name: str, consolidated_notes: str) -> str:
    """
    Takes all separate data extractions and builds a finalized, clean report
    relicating the requested presentation format using explicit few-shot instruction.
    """
    print(f"   -> Synthesizing final analytical report for {file_name}...")
    
    final_prompt = f"""
Using the consolidated data notes extracted below for the file '{file_name}', create a highly professional, cohesive summary. 
You must rigidly replicate the exact style, format, and section numbering shown in the structural template.

[STRUCTURAL TEMPLATE STYLE]
The text you provided consists of... [Brief narrative introducing what the source documents/errors are]
Here is a breakdown of exactly what this document represents.

## 1. Executive Summary
[Clear descriptive paragraph on clearance status, custom decision like RELEASE, and movement scope]

## 2. Key Transaction & Logistics Details
* **The Goods**: [Provide detailed machinery descriptions, model names, Serial Numbers, Engine IDs, and PIN codes]
* **The Value**: [State full custom value or invoice totals with clear currency indicators]
* **Weight & Packing**: [Gross metrics, package counts, packaging types]

## 3. Supply Chain Entities Involved
* **Exporter / Consignor**: [Full enterprise identity and registration addresses]
* **Importer / Consignee**: [Destination business name and border drop location]
* **Clearing Agent**: [Logistics brokerage firm details and business office address]
* **Licensed Remover (Carrier)**: [Assigned cargo hauler identity]

## 4. Customs & Route Mechanics
* **Customs Office of Clearance**: [Origin custom houses, processing depots, or warehouse numbers]
* **Movement Type**: [Customs procedure codes, purpose declarations like R.I.B/XE, security bond details, penal sum totals]
* **Port of Exit**: [Border checkpoint tags or gateway locations]
* **Transport Mode**: [Transit medium e.g., Road/Sea/Air and transport vehicle identifiers]

## 5. Duties, Financials, and Reference Numbers
* **Duties & Taxes Due**: [Explicit statement of duties, VAT, or deferred obligations]
* **Key Reference Numbers for Tracking**: [Full list of MRN, LRN, Client References, and UCR tokens]

[Provide a conclusive, clean summary narrative sentence defining the operational purpose of the paperwork]
[END OF TEMPLATE]

---
CONSOLIDATED NOTES FOR SYNTHESIS:
{consolidated_notes}
"""

    try:
        response = client.chat.completions.create(
            model="qwen2.5-1.5b-instruct",
            messages=[
                {"role": "system", "content": "You are an expert customs declaration analyst. Reorganize raw logistical logs into high-level executive briefs matching the formatting template perfectly."},
                {"role": "user", "content": final_prompt}
            ],
            temperature=0.2,
            max_tokens=1200
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Compilation process encountered an exception error: {e}"

def run_local_directory_pipeline(parent_dir: str, target_json: str):
    """Recursively parses all directories starting from the parent directory and outputs structured metrics."""
    client = OpenAI(base_url="http://localhost:8000/v1", api_key="local-pipeline")
    master_records = []

    if not os.path.exists(parent_dir):
        print(f"[Fatal] Target parent directory path '{parent_dir}' does not exist.")
        return

    print(f"Commencing deep scan of parent root directory: '{parent_dir}'")
    
    # os.walk forces continuous deep traversal into nested folder branches
    for root, subdirs, files in os.walk(parent_dir):
        for file in files:
            if file.lower().endswith('.pdf'):
                full_pdf_path = os.path.join(root, file)
                relative_display_name = os.path.relpath(full_pdf_path, parent_dir)
                
                print(f"\n[Processing File] Location: {relative_display_name}")
                
                # Step 1: Chunk the PDF text to stay within safe model limits
                data_chunks = extract_chunks_from_pdf(full_pdf_path, pages_per_chunk=2)
                
                if not data_chunks:
                    continue
                
                # Check for unrendered Adobe dynamic forms or empty extractions immediately
                first_chunk_sample = data_chunks[0]
                if "Please wait... If this message is not eventually replaced" in first_chunk_sample or not first_chunk_sample.strip():
                    print(f"   -> Flagged: Unrendered Adobe dynamic XFA form or empty document.")
                    master_records.append({
                        "file_name": relative_display_name,
                        "summary": "Error: This file is an unrendered Adobe Acrobat dynamic form or a corrupted non-text document. Text stream parsing unavailable."
                    })
                    continue
                
                # Step 2: Loop chunks sequentially through intermediate extraction
                extracted_notes_pool = []
                for idx, chunk_content in enumerate(data_chunks):
                    extracted_note = process_chunk_extraction(client, file, chunk_content, idx + 1, len(data_chunks))
                    if extracted_note:
                        extracted_notes_pool.append(extracted_note)
                
                # Step 3: Package intermediate extractions into a final structural template synthesis
                combined_notes_string = "\n\n".join(extracted_notes_pool)
                final_summary_report = compile_final_report(client, file, combined_notes_string)
                
                # Append formatted object directly to master array list
                master_records.append({
                    "file_name": relative_display_name,
                    "summary": final_summary_report
                })

    # Step 4: Output structured data list straight to target master file
    with open(target_json, 'w', encoding='utf-8') as target_output:
        json.dump(master_records, target_output, indent=4, ensure_ascii=False)
        
    print(f"\n[Pipeline Complete] Master records securely committed to: '{target_json}'")

if __name__ == "__main__":
    # Change this path string to reference your local main directory folder
    PARENT_DIRECTORY_PATH = "./customs_documents"
    MASTER_OUTPUT_FILE = "master-folder-file.json"
    
    run_local_directory_pipeline(PARENT_DIRECTORY_PATH, MASTER_OUTPUT_FILE)

```

### Key Elements of This Enhanced Architecture:

1. **Directory Awareness (`os.walk`)**: The script handles arbitrary deep nesting. If a document sits inside `./customs_documents/SubFolderA/SubFolderB/document.pdf`, the script locates it and logs its full relative path name directly into your JSON layout, preventing name collisions.
2. **Two-Stage Synthesis**: This explicitly protects the 1.5B parameter limits. Instead of asking it to remember layout rules while simultaneously extracting thousands of text strings over multiple pages, the workload is distributed:
* **Stage 1 (Extraction)**: Slices structural lines into a standard list.
* **Stage 2 (Formatting)**: Uses Few-Shot example structures to turn those raw bullet points into an advanced, polished summary matching your original example report structure.


3. **Adobe Safe-Failure Pathing**: The script continuously inspects the initial chunk. If it encounters the hidden message from a dynamic unrendered form (such as `WE CN1 - BA2950.pdf`), it handles it cleanly with an explicit error flag inside the JSON instead of failing the pipeline.

what aboue a change in apporach. a python script that goes and reads every pdf file in parent directory and creates a reference of all files into outout.json. or even a RAG database.

then call secondary script that creates a summary or each file, also adding to RAG database.

the a script that uses "file checklist.xlsx" to populate the empty fields as much  as possible

This decoupled, modular architecture is significantly more professional and scalable. Instead of attempting a single "all-in-one" script that handles file discovery, extraction, summarization, and spreadsheet matching simultaneously, you break the system down into isolated, single-purpose utilities.

This multi-script approach works ideally with local small language models (SLMs) like **Qwen2.5-1.5B** because it prevents context fatigue and minimizes system memory allocation.

---

### The Architecture Overview

```
                          ┌───────────────────────────┐
                          │   1. TEXT INGESTION STAGE │
                          └─────────────┬─────────────┘
                                        │ (Reads & Saves Raw Text)
                                        ▼
                          ┌───────────────────────────┐
                          │      raw_database.json    │
                          └─────────────┬─────────────┘
                                        │
                                        ▼
                          ┌───────────────────────────┐
                          │  2. LOCAL AI ANALYSIS STAGE│
                          └─────────────┬─────────────┘
                                        │ (Generates Structured Summaries)
                                        ▼
                          ┌───────────────────────────┐
                          │  master-folder-file.json  │
                          └─────────────┬─────────────┘
                                        │
                                        ▼
                          ┌───────────────────────────┐
                          │  3. SPREADSHEET ENRICHMENT│
                          └───────────────────────────┘
                                 (Fills FILE CHECKLIST)

```

Here is the three-script ecosystem built to process your exact folder layout.

---

### Script 1: File Discovery and Ingestion (`1_ingest_files.py`)

This script acts as your lightweight storage layer (a simple JSON database). It scans recursively through all folders, extracts the plain text from your PDFs, and indexes them safely into a file called `raw_database.json`. No AI models are called here.

```python
import os
import json
from pypdf import PdfReader

def extract_raw_text(pdf_path: str) -> str:
    """Extracts all text from a PDF document safely."""
    try:
        reader = PdfReader(pdf_path)
        full_text = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                full_text.append(text)
        return "\n".join(full_text)
    except Exception as e:
        return f"[ERROR] Failed reading file: {e}"

def build_raw_database(parent_dir: str, output_json: str):
    """Discovers every PDF in a parent directory and builds a simple reference index."""
    database = {}

    if not os.path.exists(parent_dir):
        print(f"Error: Directory {parent_dir} not found.")
        return

    print(f"Scanning '{parent_dir}' for PDF indexing...")
    for root, _, files in os.walk(parent_dir):
        for file in files:
            if file.lower().endswith('.pdf'):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, parent_dir)
                
                print(f" -> Indexing text from: {rel_path}")
                extracted_text = extract_raw_text(full_path)
                
                # Check for unrendered dynamic XFA forms immediately
                if "Please wait... If this message is not eventually replaced" in extracted_text:
                    status = "UNRENDERED_ADOBE_FORM"
                elif not extracted_text.strip():
                    status = "EMPTY_OR_SCAN"
                else:
                    status = "READY"

                database[rel_path] = {
                    "file_name": file,
                    "relative_path": rel_path,
                    "status": status,
                    "raw_text": extracted_text
                }

    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(database, f, indent=4, ensure_ascii=False)
    print(f"Success! Indexed {len(database)} documents into '{output_json}'")

if __name__ == "__main__":
    build_raw_database("./customs_documents", "raw_database.json")

```

---

### Script 2: Summarization Engine (`2_summarize_engine.py`)

This script reads from `raw_database.json`, loops through files marked as `READY`, passes the text chunks to your running `llama-server`, and generates your structured markdown summary into `master-folder-file.json`.

```python
import json
from openai import OpenAI

def chunk_text(text: str, max_words: int = 1000) -> list:
    """Slices text into minor components to prevent SLM context limit crash."""
    words = text.split()
    return [" ".join(words[i:i + max_words]) for i in range(0, len(words), max_words)]

def generate_report(client, file_name: str, text: str) -> str:
    """Passes text chunks to local Qwen model and structures a cohesive briefing."""
    chunks = chunk_text(text)
    extractions = []

    # Stage 1: Fast bullet-point data collection from chunks
    for idx, chunk in enumerate(chunks):
        prompt = f"Extract all raw logistical data, reference IDs, values, and names found here:\n\n{chunk}"
        try:
            response = client.chat.completions.create(
                model="qwen2.5-1.5b-instruct",
                messages=[
                    {"role": "system", "content": "You are a raw data extractor. Pull structural points into a brief bulleted list."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.0,
                max_tokens=400
            )
            extractions.append(response.choices[0].message.content)
        except Exception as e:
            print(f"      Chunk {idx+1} analysis error: {e}")

    # Stage 2: Pattern-match synthesis into your exact formatting template
    combined_notes = "\n".join(extractions)
    final_prompt = f"""
Using the consolidated data notes extracted below for the file '{file_name}', create a structured summary matching the exact format layout template:

## 1. Executive Summary
[Clear descriptive paragraph on clearance status and movement scope]

## 2. Key Transaction & Logistics Details
* **The Goods**: [Descriptions, model names, Serials, Engine IDs, PIN codes]
* **The Value**: [State full custom values or invoice totals]
* **Weight & Packing**: [Gross metrics, package counts]

## 3. Supply Chain Entities Involved
* **Exporter / Consignor**: [Enterprise identity and locations]
* **Importer / Consignee**: [Destination business name]
* **Clearing Agent**: [Brokerage firm details and address]
* **Licensed Remover (Carrier)**: [Assigned cargo hauler identity]

## 4. Customs & Route Mechanics
* **Customs Office of Clearance**: [Origin custom houses or warehouse numbers]
* **Movement Type**: [Customs procedure codes, purpose declarations like R.I.B/XE, security bond details]
* **Port of Exit**: [Border checkpoint tags or gateway locations]
* **Transport Mode**: [Transit medium e.g., Road/Sea/Air]

## 5. Duties, Financials, and Reference Numbers
* **Duties & Taxes Due**: [Explicit statement of duties or VAT obligations]
* **Key Reference Numbers for Tracking**: [Full list of MRN, LRN, Client References, and UCR tokens]

---
CONSOLIDATED NOTES:
{combined_notes}
"""
    try:
        res = client.chat.completions.create(
            model="qwen2.5-1.5b-instruct",
            messages=[
                {"role": "system", "content": "You are an expert customs analyst. Structure notes using the template rigidly."},
                {"role": "user", "content": final_prompt}
            ],
            temperature=0.1,
            max_tokens=1000
        )
        return res.choices[0].message.content
    except Exception as e:
        return f"Failed report consolidation: {e}"

def process_summaries():
    client = OpenAI(base_url="http://localhost:8000/v1", api_key="local-no-key-needed")
    
    with open("raw_database.json", "r", encoding="utf-8") as f:
        raw_db = json.load(f)

    master_summaries = []

    for path, data in raw_db.items():
        print(f"Processing: {path}")
        if data["status"] != "READY":
            summary_content = f"Error: Cannot generate summary. Document status flag: {data['status']}"
        else:
            print(" -> Running local inference synthesis...")
            summary_content = generate_report(client, data["file_name"], data["raw_text"])

        master_summaries.append({
            "file_name": path,
            "summary": summary_content
        })

    with open("master-folder-file.json", "w", encoding="utf-8") as f:
        json.dump(master_summaries, f, indent=4, ensure_ascii=False)
    print("Completed! Master summaries generated and saved.")

if __name__ == "__main__":
    process_summaries()

```

---

### Script 3: Metadata Extractor & Excel Auto-Populator (`3_populate_checklist.py`)

This script accomplishes your final request. It targets your spreadsheet layout (based on your uploaded `FILE CHECKLIST` metadata structure: fields like *Client Ref, Consignee, Description, PIN No, Serial No, Vessel, Voyage, Tariff Code, and MRN/LRN*).

Instead of reading raw walls of text, it maps fields directly using structured extraction from the clean text database to update the checklist.

*(Requires pandas and openpyxl: `pip install pandas openpyxl`)*

```python
import json
import re
import pandas as pd
from openai import OpenAI

def extract_exact_metadata_fields(client, file_name: str, raw_text: str) -> dict:
    """Queries Qwen to pull exact, single-string values matching the checklist rows."""
    if not raw_text or "Please wait..." in raw_text:
        return {}

    prompt = f"""
Analyze the text from document '{file_name}'. Find and extract the following exact metadata properties. 
Respond ONLY with a valid, raw JSON object. Do not include markdown codeblocks, notes, or introductions.

Expected JSON schema response format:
{{
    "Client Ref": "Look for matching business context references like 2602DS12783 or BA2950",
    "Consignee": "Look for the importer company or business name, e.g., KAMOA COPPER SA",
    "Description": "Look for heavy equipment naming, e.g., ELPHINSTONE EG20 MOTOR GRADER",
    "PIN No": "Look for exact PIN numbers or product identifiers starting with CAT...",
    "Serial No": "Look for machine frame or engine serial markers",
    "Vessel": "Look for shipping vessels if named, else leave empty",
    "Voy": "Look for sea voyage routing indicators, else leave empty",
    "Tariff Code": "Look for HS Code combinations, e.g., 8429.20",
    "MRN/LRN": "Find any Customs Movement Reference or Local Reference strings"
}}

Document Text Segment:
{raw_text[:4000]} 
"""
    try:
        response = client.chat.completions.create(
            model="qwen2.5-1.5b-instruct",
            messages=[
                {"role": "system", "content": "You are a rigid data utility. Output only strict JSON records without conversational text."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0,
            max_tokens=400
        )
        # Standard clean to ensure no accidental markdown wrappings creep in
        clean_json_str = re.sub(r"```json|```", "", response.choices[0].message.content).strip()
        return json.loads(clean_json_str)
    except Exception as e:
        print(f"   Metadata lookup failed for {file_name}: {e}")
        return {}

def update_checklist_spreadsheet(checklist_path: str, output_path: str):
    client = OpenAI(base_url="http://localhost:8000/v1", api_key="local")
    
    # Load your raw database storage
    with open("raw_database.json", "r", encoding="utf-8") as f:
        raw_db = json.load(f)

    # 1. Pool extracted data profiles across all valid documents found
    aggregated_metadata = {}
    print("Gathering key metadata matrices from document library...")
    for path, data in raw_db.items():
        if data["status"] == "READY":
            print(f" -> Mapping values for file: {data['file_name']}")
            meta = extract_exact_metadata_fields(client, data["file_name"], data["raw_text"])
            if meta:
                aggregated_metadata[data["file_name"]] = meta

    if not aggregated_metadata:
        print("No readable document metadata found to map to spreadsheet.")
        return

    # For illustration, let's combine all found values to patch the single checklist template
    # (In production, if you have multiple checklists, match them via 'Client Ref' or file keys)
    master_patch = {}
    for f_name, fields in aggregated_metadata.items():
        for k, v in fields.items():
            if v and "unknown" not in str(v).lower() and k not in master_patch:
                master_patch[k] = v

    print("\nMaster Extraction Discovery:")
    print(json.dumps(master_patch, indent=2))

    # 2. Open and Update Excel Sheet Layout
    print(f"\nOpening checklist: {checklist_path}")
    # Read CSV or native XLSX (Using pandas configuration adjusting for your uploaded metadata)
    df = pd.read_csv(checklist_path, header=None)

    # In your Excel template layout:
    # Row 1 (Index 1) -> Client Ref:, BA2950
    # Row 2 (Index 2) -> Consignee:, KAMOA COPPER SA
    # Row 3 (Index 3) -> Description:, ELPHINSTONE EG20
    # Row 4 (Index 4) -> PIN No:
    # Row 5 (Index 5) -> Serial No:
    # Row 6 (Index 6) -> Vessel:
    # Row 7 (Index 7) -> Voy:

    # Map spreadsheet indices to match targets sequentially
    mapping_indices = {
        "Client Ref": 1,
        "Consignee": 2,
        "Description": 3,
        "PIN No": 4,
        "Serial No": 5,
        "Vessel": 6,
        "Voy": 7
    }

    for field_key, excel_row_idx in mapping_indices.items():
        if field_key in master_patch:
            # Column index 1 corresponds to the empty evaluation value slot next to the label header
            df.iloc[excel_row_idx, 1] = master_patch[field_key]
            print(f" Updated Excel Row {excel_row_idx} [{field_key}] -> {master_patch[field_key]}")

    # Patching Tariff lines further down
    # Row index 10 represents "Tarrif Code, Weight & Cube" -> Column 1 updates code
    if "Tariff Code" in master_patch:
        df.iloc[10, 1] = master_patch["Tariff Code"]

    # Save out file back to Excel framework layout format
    df.to_csv(output_path, index=False, header=False)
    print(f"\nDone! Updated spreadsheet saved as: '{output_path}'")

if __name__ == "__main__":
    # Point this to your FILE CHECKLIST path
    update_checklist_spreadsheet("FILE CHECKLIST.xlsx - Sheet1.csv", "FILE_CHECKLIST_POPULATED.csv")

```

### Why this change in approach is a significant improvement:

1. **The Ingestion Database (`raw_database.json`)** serves as a lightweight text-based **Vectorless RAG context store**. If you want to scale this to a true RAG database later (using Vector tools like ChromaDB or FAISS), you only need to update Script 1 to pass the text fragments to an embedding model.
2. **Deterministic Metadata Extraction**: Script 3 instructs the model to return *only structured JSON keys*. This constraints the small local Qwen model from generating paragraphs and forces it to strictly extract precise values (like pulling `CAT00120CE9601160` and placing it directly into cell row coordinates).

