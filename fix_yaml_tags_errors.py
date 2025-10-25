#!/usr/bin/env python3
"""
修复Markdown文件中YAML前置元数据的格式错误
将tags数组中的键值对项目（如难度、前置知识）移动为独立字段
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
        
        # 查找tags数组中的键值对
        lines = yaml_content.strip().split('\n')
        new_lines = []
        extracted_fields = {}
        in_tags = False
        modified = False
        
        for line in lines:
            # 检查是否在tags数组中
            if line.strip().startswith('tags:'):
                in_tags = True
                new_lines.append(line)
            elif in_tags and line.startswith('  - '):
                # 检查是否是键值对格式
                if ':' in line and not line.strip().startswith('- "[['):
                    # 提取键值对
                    match = re.match(r'^\s*-\s*([^:]+):\s*(.+)', line)
                    if match:
                        key = match.group(1).strip()
                        value = match.group(2).strip()
                        
                        # 特殊处理前置知识字段
                        if key == '前置知识':
                            # 解析逗号分隔的多个值
                            if ',' in value:
                                # 分割并清理每个值
                                values = [v.strip() for v in value.split(',')]
                                extracted_fields[key] = values
                            else:
                                extracted_fields[key] = [value]
                        else:
                            extracted_fields[key] = value
                        modified = True
                    else:
                        new_lines.append(line)
                else:
                    new_lines.append(line)
            elif in_tags and not line.startswith('  '):
                # 退出tags数组
                in_tags = False
                new_lines.append(line)
            else:
                new_lines.append(line)
        
        if not modified:
            return False, "没有需要修复的内容"
        
        # 重新构建YAML内容
        new_yaml_lines = []
        for line in new_lines:
            new_yaml_lines.append(line)
        
        # 添加提取的字段
        for key, value in extracted_fields.items():
            if key == '前置知识' and isinstance(value, list):
                new_yaml_lines.append(f'{key}:')
                for v in value:
                    new_yaml_lines.append(f'  - {v}')
            else:
                new_yaml_lines.append(f'{key}: {value}')
        
        # 重新组装文件内容
        new_content = '---\n' + '\n'.join(new_yaml_lines) + '\n---' + body_content
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True, f"修复了字段: {', '.join(extracted_fields.keys())}"
        
    except Exception as e:
        return False, f"处理错误: {str(e)}"

def process_directory(directory_path):
    """处理目录中的所有Markdown文件"""
    if not os.path.exists(directory_path):
        print(f"错误: 目录 {directory_path} 不存在")
        return
    
    total_files = 0
    fixed_files = 0
    
    print(f"开始处理目录: {directory_path}")
    
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                total_files += 1
                
                success, message = fix_yaml_frontmatter(file_path)
                if success:
                    fixed_files += 1
                    print(f"✓ {file}: {message}")
                else:
                    print(f"- {file}: {message}")
    
    print(f"\n处理完成: 共检查 {total_files} 个文件，修复 {fixed_files} 个文件")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python fix_yaml_tags_errors.py <目录路径>")
        sys.exit(1)
    
    directory = sys.argv[1]
    process_directory(directory)