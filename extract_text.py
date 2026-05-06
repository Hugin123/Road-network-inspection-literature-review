#!/usr/bin/env python3
import pdfplumber
import sys
import os

def extract_pdf_text(path, max_pages=25):
    text = ''
    try:
        with pdfplumber.open(path) as pdf:
            for i, page in enumerate(pdf.pages[:max_pages]):
                t = page.extract_text()
                if t:
                    text += t + '\n'
    except Exception as e:
        text = f"Error: {e}"
    return text

if __name__ == '__main__':
    pdf_path = sys.argv[1]
    max_chars = int(sys.argv[2]) if len(sys.argv) > 2 else 10000
    text = extract_pdf_text(pdf_path)
    print(text[:max_chars])
