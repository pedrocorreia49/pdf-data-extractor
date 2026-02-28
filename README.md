# 📄 PDF Data Extractor

A robust Python tool that extracts tables and text from PDF files and exports to Excel/CSV.

## 🚀 Features
- **Table Extraction:** Automatically detects and extracts all tables from PDF
- **Text Extraction:** Pulls all text content with page markers
- **Multiple Formats:** Export to Excel (multi-sheet) or individual CSV files
- **Batch Ready:** Easy to extend for processing multiple PDFs
- **Error Handling:** Graceful handling of corrupted or protected PDFs
- **Logging:** Detailed console logs for monitoring

## 🛠 Tech Stack
- Python 3.9+
- pdfplumber (PDF parsing)
- Pandas (data handling)
- OpenPyXL (Excel export)

## 📖 Usage
```bash
# Install dependencies
pip install -r requirements.txt

# Place your PDF in the project folder
# Update pdf_path in pdf_extractor.py

# Run extractor
python pdf_extractor.py

# Check output/ folder for results