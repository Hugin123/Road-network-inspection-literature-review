#!/usr/bin/env python3
"""
生成详细的文献综述Markdown文件
"""

import json
import re
from collections import Counter

def load_results():
    """加载提取结果"""
    with open('literature_extraction.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_abstract(text_preview):
    """从文本预览中提取摘要"""
    if not text_preview:
        return ""
    
    # 查找Abstract部分
    text_lower = text_preview.lower()
    abstract_start = text_lower.find('abstract')
    if abstract_start == -1:
        # 使用前500个字符
        return text_preview[:500].strip()
    
    # 查找结束位置
    abstract_text = text_preview[abstract_start:]
    end_positions = []
    
    # 查找可能的结束标记
    for marker in ['keywords', '1. introduction', 'introduction', 'index terms', '©', 'http://']:
        pos = abstract_text.lower().find(marker)
        if pos != -1:
            end_positions.append(pos)
    
    # 如果没有找到结束标记，使用前1500个字符
    end_pos = min(end_positions) if end_positions else min(1500, len(abstract_text))
    
    abstract = abstract_text[:end_pos].strip()
    # 移除开头的"abstract"单词
    abstract = re.sub(r'^abstract\s*[:.]?\s*', '', abstract, flags=re.IGNORECASE)
    # 清理空格
    abstract = ' '.join(abstract.split())
    
    return abstract[:800] if len(abstract) > 800 else abstract

def extract_keywords(metadata):
    """从元数据中提取关键词"""
    keywords = metadata.get('keywords', '')
    if not keywords:
        return ""
    
    # 清理关键词
    keywords = keywords.strip()
    # 移除引号
    if keywords.startswith('"') and keywords.endswith('"'):
        keywords = keywords[1:-1]
    
    # 分割关键词
    separators = [';', ',', '、', '|']
    for sep in separators:
        if sep in keywords:
            keyword_list = [k.strip() for k in keywords.split(sep)]
            break
    else:
        keyword_list = [keywords]
    
    # 过滤空值并限制数量
    keyword_list = [k for k in keyword_list if k and len(k) > 1]
    return ', '.join(keyword_list[:8])

def extract_journal(metadata):
    """提取期刊信息"""
    subject = metadata.get('subject', '')
    if not subject:
        return ""
    
    # 常见格式: "Journal Name, Volume (Year) pages"
    journal_match = re.search(r'([A-Za-z\s&]+),\s*(\d+)\s*\((\d{4})\)', subject)
    if journal_match:
        journal_name = journal_match.group(1).strip()
        volume = journal_match.group(2)
        return f"{journal_name}, Vol. {volume}"
    
    # 其他格式
    journal_match = re.search(r'([A-Za-z\s&]+),\s*(\d+)[,:]', subject)
    if journal_match:
        journal_name = journal_match.group(1).strip()
        volume = journal_match.group(2)
        return f"{journal_name}, Vol. {volume}"
    
    return ""

def generate_detailed_review():
    """生成详细的文献综述"""
    results = load_results()
    
    markdown_lines = []
    
    # 标题和概览
    markdown_lines.append("# 道路网络巡检文献详细综述")
    markdown_lines.append("\n> 基于自动提取的20篇文献信息生成\n")
    
    # 统计信息
    valid_results = [r for r in results if 'error' not in r]
    years = [r.get('year') for r in valid_results if r.get('year') and r.get('year') != 'Unknown']
    algorithms = []
    problems = []
    
    for r in valid_results:
        if r.get('core_algorithm'):
            algorithms.extend([alg.strip() for alg in r['core_algorithm'].split(',')])
        if r.get('problem_variant'):
            problems.extend([prob.strip() for prob in r['problem_variant'].split(',')])
    
    markdown_lines.append("## 文献概览")
    markdown_lines.append(f"\n- **文献总数**: {len(results)} 篇")
    markdown_lines.append(f"- **成功提取**: {len(valid_results)} 篇")
    if years:
        markdown_lines.append(f"- **发表年份**: {min(years)} - {max(years)}")
    markdown_lines.append(f"- **涉及算法类型**: {len(set(algorithms))} 种")
    markdown_lines.append(f"- **涉及问题变体**: {len(set(problems))} 类")
    
    # 按年份统计
    year_counter = Counter([r.get('year', 'Unknown') for r in valid_results])
    markdown_lines.append("\n### 按年份分布")
    for year, count in sorted(year_counter.items()):
        markdown_lines.append(f"- **{year}**: {count} 篇")
    
    # 按算法类型统计
    algorithm_counter = Counter(algorithms)
    markdown_lines.append("\n### 主要算法类型")
    for algo, count in algorithm_counter.most_common(10):
        markdown_lines.append(f"- **{algo}**: {count} 篇")
    
    # 详细文献表格
    markdown_lines.append("\n## 文献详细信息")
    markdown_lines.append("\n| ID | 文献标题 | 作者 | 年份 | 期刊/会议 | 关键词 | 问题变体 | 核心算法 | 算法原理摘要 | APA引用 |")
    markdown_lines.append("|----|----------|------|------|-----------|--------|-----------|-----------|---------------|----------|")
    
    for i, result in enumerate(valid_results, 1):
        # 提取信息
        title = result.get('title', result['filename'])
        authors = result.get('authors', [])
        year = result.get('year', 'Unknown')
        journal = extract_journal(result.get('metadata', {}))
        keywords = extract_keywords(result.get('metadata', {}))
        problem_variant = result.get('problem_variant', '')
        core_algorithm = result.get('core_algorithm', '')
        algorithm_principle = result.get('algorithm_principle', '')
        apa_citation = result.get('apa_citation', '')
        
        # 格式化作者（最多3位）
        if authors:
            if len(authors) <= 3:
                authors_str = ', '.join(authors)
            else:
                authors_str = ', '.join(authors[:3]) + ' et al.'
        else:
            authors_str = "Unknown"
        
        # 缩短长文本用于表格显示
        def shorten(text, max_len=60):
            if not text:
                return ""
            if len(text) <= max_len:
                return text
            return text[:max_len-3] + "..."
        
        # 添加到表格
        markdown_lines.append(
            f"| {i} | {shorten(title, 80)} | {shorten(authors_str, 40)} | {year} | "
            f"{shorten(journal, 40)} | {shorten(keywords, 50)} | {shorten(problem_variant, 50)} | "
            f"{shorten(core_algorithm, 40)} | {shorten(algorithm_principle, 80)} | "
            f"{shorten(apa_citation, 100)} |"
        )
    
    # 文献摘要部分
    markdown_lines.append("\n## 文献摘要")
    
    for i, result in enumerate(valid_results, 1):
        title = result.get('title', result['filename'])
        authors = result.get('authors', [])
        year = result.get('year', 'Unknown')
        abstract = extract_abstract(result.get('text_preview', ''))
        
        markdown_lines.append(f"\n### {i}. {shorten(title, 100)}")
        markdown_lines.append(f"\n**作者**: {', '.join(authors) if authors else 'Unknown'}")
        markdown_lines.append(f"\n**年份**: {year}")
        markdown_lines.append(f"\n**摘要**: {abstract[:500]}{'...' if len(abstract) > 500 else ''}")
        
        # 算法和方法
        markdown_lines.append(f"\n**核心算法**: {result.get('core_algorithm', 'N/A')}")
        markdown_lines.append(f"\n**问题变体**: {result.get('problem_variant', 'N/A')}")
        
        # 贡献和创新点（从算法原理中提取）
        principle = result.get('algorithm_principle', '')
        if principle:
            markdown_lines.append(f"\n**主要贡献**: {principle[:300]}{'...' if len(principle) > 300 else ''}")
        
        markdown_lines.append(f"\n**APA引用**: {result.get('apa_citation', 'N/A')}")
        markdown_lines.append("\n---")
    
    # 研究趋势分析
    markdown_lines.append("\n## 研究趋势分析")
    
    # 按问题变体分类
    problem_groups = {}
    for r in valid_results:
        problem = r.get('problem_variant', 'Unknown')
        if ',' in problem:
            primary_problem = problem.split(',')[0].strip()
        else:
            primary_problem = problem.strip() if problem else 'Unknown'
        
        if primary_problem not in problem_groups:
            problem_groups[primary_problem] = []
        problem_groups[primary_problem].append(r)
    
    markdown_lines.append("\n### 主要研究问题分类")
    for problem, papers in problem_groups.items():
        markdown_lines.append(f"\n#### {problem} ({len(papers)}篇)")
        for paper in papers[:3]:  # 显示前3篇
            title = paper.get('title', paper['filename'])
            authors = paper.get('authors', [])
            year = paper.get('year', 'Unknown')
            markdown_lines.append(f"- **{year}**: {', '.join(authors[:2]) if authors else 'Unknown'} - {shorten(title, 80)}")
        if len(papers) > 3:
            markdown_lines.append(f"- ... 还有 {len(papers)-3} 篇")
    
    # 按算法分类
    algorithm_groups = {}
    for r in valid_results:
        algorithms = r.get('core_algorithm', '').split(',')
        for algo in algorithms:
            algo = algo.strip()
            if algo:
                if algo not in algorithm_groups:
                    algorithm_groups[algo] = []
                algorithm_groups[algo].append(r)
    
    markdown_lines.append("\n### 主要算法应用")
    for algo, papers in sorted(algorithm_groups.items(), key=lambda x: len(x[1]), reverse=True)[:10]:
        markdown_lines.append(f"\n#### {algo} ({len(papers)}篇)")
        years = [p.get('year', 'Unknown') for p in papers]
        year_range = f"{min(years)}-{max(years)}" if years else "Unknown"
        markdown_lines.append(f"- **应用年份**: {year_range}")
        markdown_lines.append(f"- **代表文献**: {', '.join([p.get('title', p['filename'])[:50] for p in papers[:2]])}{'...' if len(papers) > 2 else ''}")
    
    return '\n'.join(markdown_lines)

if __name__ == "__main__":
    review_content = generate_detailed_review()
    
    # 写入文件
    with open('literature_review.md', 'w', encoding='utf-8') as f:
        f.write(review_content)
    
    print("详细文献综述已生成: literature_review.md")
    print(f"内容长度: {len(review_content)} 字符")