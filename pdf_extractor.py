import pdfplumber
import pandas as pd
import logging
from datetime import datetime
import os
import json

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def extract_tables_from_pdf(pdf_path):
    """Extracts all tables from a PDF file."""
    tables = []
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            logger.info(f"Opened PDF: {pdf_path}")
            logger.info(f"Total pages: {len(pdf.pages)}")
            
            for i, page in enumerate(pdf.pages):
                logger.info(f"Processing page {i+1}...")
                page_tables = page.extract_tables()
                
                for j, table in enumerate(page_tables):
                    if table:
                        tables.append({
                            'page': i + 1,
                            'table_number': j + 1,
                            'data': table,
                            'rows': len(table),
                            'columns': len(table[0]) if table else 0
                        })
                        logger.info(f"  Found table {j+1} on page {i+1}: {len(table)} rows x {len(table[0]) if table else 0} columns")
        
        logger.info(f"Total tables extracted: {len(tables)}")
        return tables
    
    except Exception as e:
        logger.error(f"Failed to extract tables: {e}")
        return []

def extract_text_from_pdf(pdf_path):
    """Extracts all text content from a PDF file."""
    text = ""
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                if page_text:
                    text += f"--- Page {i+1} ---\n{page_text}\n\n"
        
        logger.info(f"Extracted {len(text)} characters of text")
        return text
    
    except Exception as e:
        logger.error(f"Failed to extract text: {e}")
        return ""

def save_tables_to_excel(tables, output_path):
    """Saves extracted tables to Excel with separate sheets."""
    if not tables:
        logger.warning("No tables to save")
        return False
    
    try:
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            for i, table in enumerate(tables):
                df = pd.DataFrame(table['data'])
                sheet_name = f"Page{table['page']}_Table{table['table_number']}"
                # Excel sheet names max 31 chars
                sheet_name = sheet_name[:31]
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        logger.info(f"Saved {len(tables)} tables to {output_path}")
        return True
    
    except Exception as e:
        logger.error(f"Failed to save Excel: {e}")
        return False

def save_tables_to_csv(tables, output_folder):
    """Saves each table to a separate CSV file."""
    if not tables:
        logger.warning("No tables to save")
        return False
    
    try:
        os.makedirs(output_folder, exist_ok=True)
        
        for i, table in enumerate(tables):
            df = pd.DataFrame(table['data'])
            filename = f"table_page{table['page']}_num{table['table_number']}.csv"
            filepath = os.path.join(output_folder, filename)
            df.to_csv(filepath, index=False, encoding='utf-8-sig')
        
        logger.info(f"Saved {len(tables)} CSV files to {output_folder}")
        return True
    
    except Exception as e:
        logger.error(f"Failed to save CSVs: {e}")
        return False

def save_text_to_file(text, output_path):
    """Saves extracted text to a text file."""
    if not text:
        logger.warning("No text to save")
        return False
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        
        logger.info(f"Saved text to {output_path}")
        return True
    
    except Exception as e:
        logger.error(f"Failed to save text: {e}")
        return False

def main():
    # Configuration
    pdf_path = 'sample.pdf'  # Change to your PDF file
    output_folder = 'output'
    
    logger.info("="*60)
    logger.info("PDF Data Extractor - Starting")
    logger.info("="*60)
    
    # Check if PDF exists
    if not os.path.exists(pdf_path):
        logger.error(f"PDF file not found: {pdf_path}")
        return
    
    # Create output folder
    os.makedirs(output_folder, exist_ok=True)
    
    # Extract tables
    tables = extract_tables_from_pdf(pdf_path)
    
    # Extract text
    text = extract_text_from_pdf(pdf_path)
    
    # Generate timestamp for filenames
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Save tables to Excel
    excel_path = os.path.join(output_folder, f'tables_{timestamp}.xlsx')
    save_tables_to_excel(tables, excel_path)
    
    # Save tables to CSVs
    csv_folder = os.path.join(output_folder, f'csv_{timestamp}')
    save_tables_to_csv(tables, csv_folder)
    
    # Save text
    text_path = os.path.join(output_folder, f'text_{timestamp}.txt')
    save_text_to_file(text, text_path)
    
    # Summary
    logger.info("="*60)
    logger.info("EXTRACTION COMPLETE")
    logger.info(f"  Tables found: {len(tables)}")
    logger.info(f"  Text characters: {len(text)}")
    logger.info(f"  Output folder: {output_folder}")
    logger.info("="*60)

if __name__ == "__main__":
    main()