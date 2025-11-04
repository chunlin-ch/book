#!/usr/bin/env python3
"""
修复Markdown文件中YAML前置元数据的格式错误
将tags数组中的双方括号链接项移动为独立的前置知识字段
"""

import os
import re
import sys

def fix_yaml_frontmatter(file_path):
    """修复单个文件的YAML前置元数据"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否有YAML前置元数据
        if not content.startswith('---'):
            return False, "没有YAML前置元数据"
        
        # 分离YAML前置元数据和正文
        parts = content.split('---', 2)
        if len(parts) < 3:
            return False, "YAML前置元数据格式不正确"
        
        yaml_content = parts[1]
        body_content = parts[2]
        
        # 查找tags数组中的双方括号链接
        lines = yaml_content.strip().split('\n')
        new_lines = []
        prerequisite_links = []
        in_tags = False
        
        for line in lines:
            # 检查是否在tags数组中
            if line.strip().startswith('tags:'):
                in_tags = True
                new_lines.append(line)
                continue

            if in_tags and line.startswith('  - '):
                # 检查是否是双方括号链接（允许带或不带引号）
                if re.match(r'^\s*-\s*"?\[\[.*\]\]"?\s*$', line):
                    # 提取链接内容（不重复包裹引号）
                    match = re.search(r'\[\[(.*?)\]\]', line)
                    if match:
                        prerequisite_links.append(f'"[[{match.group(1)}]]"')
                    # 不将该行保留在 tags 中
                    continue
                else:
                    new_lines.append(line)
                    continue

            if in_tags and not line.startswith('  '):
                # 退出tags数组
                in_tags = False
                new_lines.append(line)
                continue

            # 标准化顶层的前置知识行，避免出现双重引号
            if re.match(r'^\s*前置知识:\s*"+\[\[.*\]\]"+\s*$', line):
                line = re.sub(r'^(\s*前置知识:\s*)"+(\[\[.*\]\])"+\s*$', r'\1"\2"', line)
                new_lines.append(line)
                continue

            # 规范日期字段：如果为 0 或 "0" 则替换为有效日期字符串
            if re.match(r'^\s*date:\s*"?0"?\s*$', line):
                new_lines.append('date: "1970-01-01"')
                continue

            new_lines.append(line)
        
        # 如果找到了前置知识链接，添加前置知识字段（顶层）
        if prerequisite_links:
            if len(prerequisite_links) == 1:
                new_lines.append(f'前置知识: {prerequisite_links[0]}')
            else:
                new_lines.append('前置知识:')
                for link in prerequisite_links:
                    new_lines.append(f'  - {link}')
        
        # 重新组装文件内容
        new_yaml = '\n'.join(new_lines)
        new_content = f'---\n{new_yaml}\n---{body_content}'
        
        # 只有在内容发生变化时才写入文件
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True, f"修复了 {len(prerequisite_links)} 个前置知识链接"
        else:
            return False, "没有需要修复的内容"
            
    except Exception as e:
        return False, f"处理文件时出错: {str(e)}"

def process_directory(directory_path):
    """处理目录下的所有Markdown文件"""
    if not os.path.exists(directory_path):
        print(f"目录不存在: {directory_path}")
        return
    
    fixed_count = 0
    total_count = 0
    
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                total_count += 1
                
                success, message = fix_yaml_frontmatter(file_path)
                if success:
                    fixed_count += 1
                    print(f"✓ {file}: {message}")
                else:
                    print(f"- {file}: {message}")
    
    print(f"\n处理完成: 共检查 {total_count} 个文件，修复 {fixed_count} 个文件")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python fix_yaml_errors.py <目录路径>")
        sys.exit(1)
    
    directory = sys.argv[1]
    process_directory(directory)
