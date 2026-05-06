#!/usr/bin/env python3
"""
PDF文献信息提取脚本
提取以下信息：
1. 作者
2. 年份
3. 解决的特定问题变体
4. 核心算法（如启发式、精确算法或强化学习）
5. 算法核心原理
6. APA格式的引用

使用pdfplumber和pypdf库
"""

import os
import re
import json
import pdfplumber
import pypdf
from typing import Dict, List, Optional, Any, Tuple
import glob
from collections import Counter

def extract_text_with_pdfplumber(pdf_path: str) -> str:
    """使用pdfplumber提取PDF文本（保留布局）"""
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"使用pdfplumber提取{os.path.basename(pdf_path)}失败: {e}")
        # 回退到pypdf
        text = extract_text_with_pypdf(pdf_path)
    return text

def extract_text_with_pypdf(pdf_path: str) -> str:
    """使用pypdf提取PDF文本"""
    text = ""
    try:
        reader = pypdf.PdfReader(pdf_path)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    except Exception as e:
        print(f"使用pypdf提取{os.path.basename(pdf_path)}失败: {e}")
    return text

def extract_metadata(pdf_path: str) -> Dict[str, Any]:
    """提取PDF元数据"""
    metadata = {}
    try:
        reader = pypdf.PdfReader(pdf_path)
        if reader.metadata:
            metadata = {
                'title': reader.metadata.get('/Title', ''),
                'author': reader.metadata.get('/Author', ''),
                'subject': reader.metadata.get('/Subject', ''),
                'keywords': reader.metadata.get('/Keywords', ''),
                'creator': reader.metadata.get('/Creator', ''),
                'producer': reader.metadata.get('/Producer', ''),
                'creation_date': reader.metadata.get('/CreationDate', ''),
                'mod_date': reader.metadata.get('/ModDate', '')
            }
    except Exception as e:
        print(f"提取{os.path.basename(pdf_path)}元数据失败: {e}")
    return metadata

def extract_authors_year_from_text(text: str, metadata: Dict) -> tuple:
    """从文本和元数据中提取作者和年份"""
    authors = []
    year = None
    
    # 1. 首先从元数据中提取作者
    if metadata.get('author'):
        # 尝试解析元数据中的作者字段
        author_str = metadata['author']
        # 常见的作者分隔符: 逗号、分号、"and"
        # 例如: "Smith, J., Doe, A., and Johnson, B." 或 "J. Smith; A. Doe"
        author_parts = re.split(r',\s*(?:and\s*)?|;\s*|\s+and\s+', author_str)
        authors = [a.strip() for a in author_parts if a.strip()]
    
    # 2. 如果元数据中没有，从文本开头提取
    if not authors:
        lines = text.split('\n')
        first_few_lines = lines[:20]  # 查看前20行
        
        # 尝试查找作者行（通常包含"et al."、"Department"、"University"等）
        for i, line in enumerate(first_few_lines):
            line = line.strip()
            # 跳过空行、太长的行（可能为标题）、包含特定关键词的行
            if not line or len(line) > 200 or any(word in line.lower() for word in ['abstract', 'keywords', 'journal', 'volume', 'doi:', 'http']):
                continue
            
            # 作者模式：包含逗号和点号的名字格式
            if re.search(r'[A-Z][a-z]+,\s*[A-Z]\.', line) or re.search(r'[A-Z]\.\s*[A-Z][a-z]+', line):
                # 清理行：移除邮箱、机构信息
                clean_line = re.sub(r'<[^>]+>|\([^)]+\)|\[[^\]]+\]', '', line)
                clean_line = re.sub(r'\b(?:university|department|school|college|institute|laboratory)\b', '', clean_line, flags=re.IGNORECASE)
                clean_line = re.sub(r'\b\w+@\w+\.\w+\b', '', clean_line)  # 移除邮箱
                
                # 分割作者
                author_parts = re.split(r',\s*(?:and\s*)?|;\s*|\s+and\s+', clean_line)
                authors = [a.strip() for a in author_parts if a.strip() and len(a.strip()) > 3]
                if authors:
                    break
    
    # 3. 从元数据中提取年份（从创建日期或主题）
    year = None
    if metadata.get('creation_date'):
        # 日期格式: D:YYYYMMDDHHMMSSZ
        date_match = re.search(r'D:(\d{4})', metadata['creation_date'])
        if date_match:
            year = date_match.group(1)
    
    if not year and metadata.get('subject'):
        # 从主题中提取年份，如 "Transportation Research Part B, 166 (2022) 143-182"
        year_match = re.search(r'\((\d{4})\)', metadata['subject'])
        if year_match:
            year = year_match.group(1)
    
    # 4. 从文本中提取年份
    if not year:
        # 在标题附近查找年份
        lines = text.split('\n')
        for i, line in enumerate(lines[:30]):
            # 查找包含年份的模式
            year_match = re.search(r'\b(20[0-2][0-9]|19[0-9]{2})\b', line)
            if year_match:
                candidate = year_match.group(1)
                # 验证是否为合理的年份
                if 1900 <= int(candidate) <= 2026:
                    year = candidate
                    break
    
    return authors, year

def extract_problem_variant(text: str) -> str:
    """从文本中提取解决的问题变体"""
    # 常见的问题变体关键词
    problem_keywords = [
        'Capacitated Arc Routing Problem',
        'CARP',
        'Vehicle Routing Problem',
        'VRP',
        'Arc Routing Problem',
        'ARP',
        'Rural Postman Problem',
        'RPP',
        'Drone routing',
        'UAV routing',
        'Uncertain Capacitated Arc Routing',
        'Stochastic',
        'Multi-depot',
        'Multi-period',
        'Time-dependent',
        'Dynamic',
        'General Routing Problem',
        'GRP',
        'Mixed Capacitated Arc Routing Problem',
        'MCARP'
    ]
    
    text_lower = text.lower()
    problems_found = []
    
    for keyword in problem_keywords:
        if keyword.lower() in text_lower:
            problems_found.append(keyword)
    
    # 返回找到的问题变体
    if problems_found:
        return ', '.join(problems_found[:3])  # 返回前3个
    return ""

def extract_core_algorithm(text: str) -> str:
    """从文本中提取核心算法"""
    algorithm_keywords = [
        'Genetic Algorithm',
        'GA',
        'Genetic Programming',
        'GP',
        'Heuristic',
        'Metaheuristic',
        'Local Search',
        'Tabu Search',
        'Simulated Annealing',
        'Ant Colony',
        'Particle Swarm',
        'Reinforcement Learning',
        'RL',
        'Deep Learning',
        'Neural Network',
        'Exact algorithm',
        'Mixed Integer Programming',
        'MIP',
        'Linear Programming',
        'LP',
        'Integer Programming',
        'IP',
        'Branch and Bound',
        'Branch and Cut',
        'Dynamic Programming',
        'Greedy algorithm',
        'Approximation algorithm',
        'Matheuristic',
        'Hybrid algorithm'
    ]
    
    text_lower = text.lower()
    algorithms_found = []
    
    for keyword in algorithm_keywords:
        if keyword.lower() in text_lower:
            algorithms_found.append(keyword)
    
    if algorithms_found:
        return ', '.join(algorithms_found[:3])
    return ""

def extract_algorithm_principle(text: str) -> str:
    """提取算法核心原理（从摘要或引言中）"""
    # 查找摘要部分（通常包含"Abstract"关键词）
    abstract_start = text.lower().find('abstract')
    if abstract_start != -1:
        # 提取摘要内容（通常到"Keywords"或"1. Introduction"为止）
        abstract_end = text.lower().find('keywords', abstract_start)
        if abstract_end == -1:
            abstract_end = text.lower().find('1. introduction', abstract_start)
        if abstract_end == -1:
            abstract_end = abstract_start + 2000  # 如果没有找到结束，取2000字符
        
        abstract_text = text[abstract_start:abstract_end]
    else:
        # 如果没有找到"Abstract"，取前1500个字符
        abstract_text = text[:1500]
    
    # 在摘要中查找描述算法的句子
    sentences = re.split(r'[.!?]', abstract_text)
    
    algorithm_phrases = []
    algorithm_keywords = [
        'algorithm', 'approach', 'method', 'propose', 'introduce', 'develop',
        'present', 'formulate', 'solve', 'design', 'implement', 'proposed',
        'developed', 'introduced', 'designed', 'formulated'
    ]
    
    for sentence in sentences:
        sentence_lower = sentence.lower().strip()
        if any(keyword in sentence_lower for keyword in algorithm_keywords):
            # 清理句子
            clean_sentence = ' '.join(sentence.split()).strip()
            if len(clean_sentence) > 30 and len(clean_sentence) < 300:
                # 确保句子包含算法相关内容
                if any(word in clean_sentence.lower() for word in ['genetic', 'heuristic', 'exact', 'programming', 'search', 'learning', 'optimization']):
                    algorithm_phrases.append(clean_sentence)
    
    if algorithm_phrases:
        # 返回最重要的1-2个句子
        return ' '.join(algorithm_phrases[:2])
    
    # 如果摘要中没有找到，在整个文本中查找
    all_sentences = re.split(r'[.!?]', text[:5000])
    for sentence in all_sentences:
        sentence_lower = sentence.lower().strip()
        if any(keyword in sentence_lower for keyword in ['algorithm', 'approach', 'method']):
            clean_sentence = ' '.join(sentence.split()).strip()
            if len(clean_sentence) > 30 and len(clean_sentence) < 300:
                return clean_sentence
    
    return ""

def generate_apa_citation(title: str, authors: List[str], year: str, 
                         journal: str = "", volume: str = "", 
                         pages: str = "", doi: str = "") -> str:
    """生成APA格式引用"""
    if not authors:
        authors_str = "Unknown"
    else:
        # 格式化作者：Last, F. I., Last2, F. I., & Last3, F. I.
        formatted_authors = []
        for author in authors:
            # 清理作者名中的多余空格
            author = author.strip()
            
            # 尝试不同的作者名格式
            # 格式1: "Last, First" 或 "Last, F."
            if ',' in author:
                parts = [p.strip() for p in author.split(',')]
                if len(parts) >= 2:
                    last_name = parts[0]
                    first_names = parts[1]
                    # 提取首字母
                    initials = ''.join([name[0].upper() + '.' for name in first_names.split() if name])
                    formatted_authors.append(f"{last_name}, {initials}")
                else:
                    formatted_authors.append(author)
            # 格式2: "First Last" 或 "F. Last"
            else:
                parts = author.split()
                if len(parts) >= 2:
                    # 可能是 "First Last" 或 "F. Last"
                    last_name = parts[-1]
                    first_parts = parts[:-1]
                    initials = ''.join([name[0].upper() + '.' for name in first_parts if name and name[0].isupper()])
                    if initials:
                        formatted_authors.append(f"{last_name}, {initials}")
                    else:
                        formatted_authors.append(author)
                else:
                    formatted_authors.append(author)
        
        # APA格式：用逗号分隔作者，最后两个作者用&连接
        if len(formatted_authors) == 1:
            authors_str = formatted_authors[0]
        elif len(formatted_authors) == 2:
            authors_str = f"{formatted_authors[0]} & {formatted_authors[1]}"
        elif len(formatted_authors) > 7:  # APA: 超过7个作者用et al.
            authors_str = ', '.join(formatted_authors[:3]) + ', et al.'
        elif len(formatted_authors) > 2:
            # 前n-1个作者用逗号分隔，最后一个用&连接
            authors_str = ', '.join(formatted_authors[:-1]) + ', & ' + formatted_authors[-1]
        else:
            authors_str = ', '.join(formatted_authors)
    
    # 构建引用
    if year and year != 'Unknown':
        citation = f"{authors_str} ({year}). {title}."
    else:
        citation = f"{authors_str}. {title}."
    
    if journal:
        citation += f" {journal}"
        if volume:
            citation += f", {volume}"
        if pages:
            citation += f", {pages}."
        else:
            citation += "."
    elif doi:
        citation += f" https://doi.org/{doi}"
    
    return citation

def extract_info_from_pdf(pdf_path: str) -> Dict[str, Any]:
    """从单个PDF文件中提取信息"""
    print(f"处理: {os.path.basename(pdf_path)}")
    
    # 提取文本
    text = extract_text_with_pdfplumber(pdf_path)
    if not text or len(text.strip()) < 100:
        print(f"  警告: {os.path.basename(pdf_path)} 文本提取可能失败")
    
    # 提取元数据
    metadata = extract_metadata(pdf_path)
    
    # 提取信息
    authors, year = extract_authors_year_from_text(text, metadata)
    problem_variant = extract_problem_variant(text)
    core_algorithm = extract_core_algorithm(text)
    algorithm_principle = extract_algorithm_principle(text)
    
    # 从元数据获取标题，或从文本中提取
    title = metadata.get('title', '')
    if not title:
        # 尝试从文本第一行提取标题
        lines = text.split('\n')
        for line in lines[:5]:
            line = line.strip()
            if line and len(line) > 20 and len(line) < 300:
                # 跳过明显的页眉页脚
                if not any(word in line.lower() for word in ['journal', 'volume', 'issue', 'page', 'doi:', 'http']):
                    title = line
                    break
    
    # 提取期刊信息和DOI
    journal_info = ""
    doi = ""
    
    # 从元数据主题中提取期刊信息
    if metadata.get('subject'):
        subject = metadata['subject']
        # 尝试提取期刊名称和卷期
        journal_match = re.search(r'([A-Za-z\s]+),\s*(\d+)\s*\((\d{4})\)', subject)
        if journal_match:
            journal_name = journal_match.group(1).strip()
            volume = journal_match.group(2)
            year_from_subject = journal_match.group(3)
            journal_info = f"{journal_name}, {volume}"
            
            # 如果年份还没有，使用主题中的年份
            if not year and year_from_subject:
                year = year_from_subject
        
        # 提取DOI
        doi_match = re.search(r'doi:([^\s,]+)', subject, re.IGNORECASE)
        if doi_match:
            doi = doi_match.group(1).strip()
    
    # 如果没有从元数据中找到，尝试从文本中提取
    if not doi:
        doi_match = re.search(r'doi:\s*([^\s,]+)', text[:2000], re.IGNORECASE)
        if doi_match:
            doi = doi_match.group(1).strip()
    
    # 生成APA引用
    apa_citation = generate_apa_citation(
        title=title if title else os.path.basename(pdf_path),
        authors=authors,
        year=year if year else 'Unknown',
        journal=journal_info,
        volume="",
        pages="",
        doi=doi
    )
    
    result = {
        'filename': os.path.basename(pdf_path),
        'title': title,
        'authors': authors,
        'year': year,
        'problem_variant': problem_variant,
        'core_algorithm': core_algorithm,
        'algorithm_principle': algorithm_principle[:500] if algorithm_principle else '',  # 限制长度
        'apa_citation': apa_citation,
        'text_preview': text[:1000] if text else '',  # 前1000字符作为预览
        'metadata': metadata
    }
    
    return result

def process_all_pdfs(pdf_dir: str) -> List[Dict[str, Any]]:
    """处理目录中的所有PDF文件"""
    pdf_files = glob.glob(os.path.join(pdf_dir, "*.pdf"))
    pdf_files.sort()  # 按文件名排序
    
    results = []
    total = len(pdf_files)
    
    print(f"找到 {total} 个PDF文件")
    
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"[{i}/{total}] 处理: {os.path.basename(pdf_file)}")
        try:
            result = extract_info_from_pdf(pdf_file)
            results.append(result)
            print(f"  完成")
        except Exception as e:
            print(f"  处理失败: {e}")
            results.append({
                'filename': os.path.basename(pdf_file),
                'error': str(e)
            })
    
    return results

def save_results(results: List[Dict[str, Any]], output_file: str):
    """保存结果到JSON和Markdown文件"""
    # 保存为JSON
    json_file = output_file.replace('.md', '.json')
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"结果已保存到: {json_file}")
    
    # 保存为Markdown表格
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# 文献信息提取结果\n\n")
        f.write("| 文件名 | 作者 | 年份 | 问题变体 | 核心算法 | 算法原理摘要 | APA引用 |\n")
        f.write("|--------|------|------|-----------|-----------|---------------|----------|\n")
        
        for result in results:
            if 'error' in result:
                f.write(f"| {result['filename']} | 提取失败 | - | - | - | - | - |\n")
                continue
            
            # 格式化表格内容
            authors_str = ', '.join(result['authors'][:2]) if result['authors'] else 'Unknown'
            if len(result['authors']) > 2:
                authors_str += ' et al.'
            
            year_str = result['year'] if result['year'] else 'Unknown'
            problem_str = result['problem_variant'][:50] + '...' if len(result['problem_variant']) > 50 else result['problem_variant']
            algorithm_str = result['core_algorithm'][:30] + '...' if len(result['core_algorithm']) > 30 else result['core_algorithm']
            principle_str = result['algorithm_principle'][:80] + '...' if len(result['algorithm_principle']) > 80 else result['algorithm_principle']
            citation_str = result['apa_citation'][:100] + '...' if len(result['apa_citation']) > 100 else result['apa_citation']
            
            f.write(f"| {result['filename']} | {authors_str} | {year_str} | {problem_str} | {algorithm_str} | {principle_str} | {citation_str} |\n")
    
    print(f"Markdown表格已保存到: {output_file}")

def main():
    """主函数"""
    pdf_dir = "literature"
    output_file = "literature_extraction.md"
    
    if not os.path.exists(pdf_dir):
        print(f"目录不存在: {pdf_dir}")
        return
    
    # 处理所有PDF
    results = process_all_pdfs(pdf_dir)
    
    # 保存结果
    save_results(results, output_file)
    
    # 打印摘要
    print(f"\n处理完成!")
    print(f"成功处理: {len([r for r in results if 'error' not in r])}/{len(results)} 个文件")
    
    # 显示部分结果
    print("\n=== 前3个文献提取结果 ===")
    for i, result in enumerate(results[:3]):
        if 'error' not in result:
            print(f"\n{i+1}. {result['filename']}")
            print(f"   标题: {result['title'][:80]}..." if len(result['title']) > 80 else f"   标题: {result['title']}")
            print(f"   作者: {', '.join(result['authors']) if result['authors'] else 'Unknown'}")
            print(f"   年份: {result['year']}")
            print(f"   问题变体: {result['problem_variant'][:80]}..." if len(result['problem_variant']) > 80 else f"   问题变体: {result['problem_variant']}")
            print(f"   核心算法: {result['core_algorithm']}")
            print(f"   APA引用: {result['apa_citation'][:120]}..." if len(result['apa_citation']) > 120 else f"   APA引用: {result['apa_citation']}")

if __name__ == "__main__":
    main()