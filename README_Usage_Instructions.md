# Directory Analyzer - Usage Instructions

## Copying to Other Shipping Folders

Yes, you can absolutely copy the `directory_analyzer.py` script to other active shipping folders and run it to achieve the same goal. Here's how:

### Method 1: Copy Script to Each Folder
1. Copy `directory_analyzer.py` to your target shipping folder
2. Open command prompt/terminal in that folder
3. Run: `python directory_analyzer.py`

### Method 2: Run from Original Location
You can also run the script from the original location and specify a different target directory:

```python
# Modify the main() function in directory_analyzer.py:
def main():
    # Change this line to point to your target directory
    target_dir = "C:\\Path\\To\\Your\\Other\\Shipping\\Folder"
    
    # Initialize analyzer with the target directory
    analyzer = DirectoryAnalyzer(target_dir)
    # ... rest of the code remains the same
```

## What the Script Will Do in Other Folders

When you run the script in other shipping folders, it will:

1. **Analyze the directory structure** of that specific folder
2. **Extract file metadata** (names, sizes, dates)
3. **Parse file names** to extract reference data (PIN numbers, container numbers, etc.)
4. **Generate a new `directory_analysis.json`** file in that folder
5. **Create/update a `checklist.md`** file with populated data specific to that folder

## Key Benefits

- **Portable**: Works in any directory without modification
- **Self-contained**: All logic is in the single Python file
- **Adaptive**: Automatically detects and analyzes whatever files are present
- **Consistent output**: Always generates the same JSON structure and checklist format

## Example Usage

```bash
# Navigate to your other shipping folder
cd "C:\Users\Jason\Other\Shipping\Folder"

# Copy the script there
copy "C:\Users\Jason\FML Freight Solutions\FML Doc Share - Documents\BARTRAC\2602DRE2775 - BA2867 - ETT 90T DIESEL TANK FOR CAT777 - SAKANIA\directory_analyzer.py" .

# Run the analysis
python directory_analyzer.py
```

## Output Files Created

For each folder you analyze, the script will create:
- `directory_analysis.json` - Detailed analysis data
- `checklist.md` - Populated checklist ready for use

The script is completely reusable and will adapt to any shipping folder structure you have!