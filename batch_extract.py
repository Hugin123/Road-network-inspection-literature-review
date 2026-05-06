#!/usr/bin/env python3
"""批量提取所有PDF文本，保存到临时文件"""
import pdfplumber
import os
import json

literature_dir = "/Users/lipeixuan/PycharmProjects/文献调研/Road-network-inspection-literature-review/literature"
output_dir = "/Users/lipeixuan/PycharmProjects/文献调研/Road-network-inspection-literature-review/pdf_texts"

os.makedirs(output_dir, exist_ok=True)

pdfs = [f for f in os.listdir(literature_dir) if f.endswith('.pdf')]
pdfs.sort()

for pdf_file in pdfs:
    pdf_path = os.path.join(literature_dir, pdf_file)
    output_path = os.path.join(output_dir, pdf_file.replace('.pdf', '.txt'))
    
    if os.path.exists(output_path):
        print(f"Already extracted: {pdf_file}")
        continue
    
    print(f"Extracting: {pdf_file}")
    text = ''
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages[:30]):
                t = page.extract_text()
                if t:
                    text += t + '\n'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"  -> Saved {len(text)} chars")
    except Exception as e:
        print(f"  -> Error: {e}")

print("Done!")
