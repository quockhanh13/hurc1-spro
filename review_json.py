#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script Review JSON Configuration
Phân tích file cấu hình workflow JSON
"""

import json
import sys
from datetime import datetime

def load_json_file(filename):
    """Load file JSON"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Không tìm thấy file: {filename}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Lỗi JSON: {e}")
        return None

def analyze_workflow_structure(data):
    """Phân tích cấu trúc workflow"""
    print("=" * 60)
    print("📋 PHÂN TÍCH CẤU HÌNH WORKFLOW")
    print("=" * 60)
    
    # Phân tích relatives (các bước trong workflow)
    if 'relatives' in data:
        print(f"\n🔄 WORKFLOW STEPS ({len(data['relatives'])} bước):")
        for i, step in enumerate(data['relatives'], 1):
            print(f"  {i}. {step.get('summary', 'N/A')}")
            print(f"     - ID: {step.get('id', 'N/A')}")
            print(f"     - Type: {step.get('type', 'N/A')}")
            print(f"     - Status: {step.get('status', 'N/A')}")
            print(f"     - Phase Type: {step.get('phaseType', 'N/A')}")
            if 'sla' in step:
                print(f"     - SLA: Response {step['sla'].get('res', 'N/A')}h, Fix {step['sla'].get('fix', 'N/A')}h")
            print()

def analyze_form_fields(data):
    """Phân tích các trường form"""
    print("📝 PHÂN TÍCH FORM FIELDS:")
    print("-" * 40)
    
    if 'individual' in data:
        fields = data['individual']
        print(f"Tổng số trường: {len(fields)}")
        
        # Thống kê theo loại
        field_types = {}
        required_fields = []
        optional_fields = []
        
        for field in fields:
            field_type = field.get('type', 'unknown')
            field_types[field_type] = field_types.get(field_type, 0) + 1
            
            # Kiểm tra required
            conditions = field.get('conditions', {})
            if conditions.get('required', False):
                required_fields.append(field.get('name', 'N/A'))
            else:
                optional_fields.append(field.get('name', 'N/A'))
        
        print(f"\n📊 Thống kê theo loại:")
        for field_type, count in field_types.items():
            print(f"  - {field_type}: {count}")
        
        print(f"\n🔴 Trường bắt buộc ({len(required_fields)}):")
        for field in required_fields[:10]:  # Hiển thị 10 đầu
            print(f"  - {field}")
        if len(required_fields) > 10:
            print(f"  ... và {len(required_fields) - 10} trường khác")
        
        print(f"\n🟢 Trường tùy chọn ({len(optional_fields)}):")
        for field in optional_fields[:10]:  # Hiển thị 10 đầu
            print(f"  - {field}")
        if len(optional_fields) > 10:
            print(f"  ... và {len(optional_fields) - 10} trường khác")

def analyze_table_structure(data):
    """Phân tích cấu trúc bảng"""
    print("\n📊 PHÂN TÍCH CẤU TRÚC BẢNG:")
    print("-" * 40)
    
    if 'table' in data:
        table = data['table']
        columns = table.get('columns', [])
        print(f"Số cột: {len(columns)}")
        
        for i, column in enumerate(columns, 1):
            print(f"  {i}. {column.get('name', 'N/A')}")
            print(f"     - Type: {column.get('type', 'N/A')}")
            print(f"     - Required: {column.get('conditions', {}).get('required', False)}")

def analyze_relationships(data):
    """Phân tích mối quan hệ"""
    print("\n🔗 PHÂN TÍCH MỐI QUAN HỆ:")
    print("-" * 40)
    
    if 'relationships' in data:
        relationships = data['relationships']
        print(f"Số mối quan hệ: {len(relationships)}")
        
        for rel in relationships:
            print(f"  - Từ {rel.get('from', 'N/A')} → {rel.get('to', 'N/A')}")
            print(f"    Type: {rel.get('type', 'N/A')}")
            print(f"    Status: {rel.get('status', 'N/A')}")

def analyze_print_config(data):
    """Phân tích cấu hình in ấn"""
    print("\n🖨️ PHÂN TÍCH CẤU HÌNH IN ẤN:")
    print("-" * 40)
    
    for relative in data.get('relatives', []):
        if 'print-config' in relative:
            print_config = relative['print-config']
            print(f"Template: {print_config.get('filename', 'N/A')}")
            print(f"URL: {print_config.get('template-url', 'N/A')}")
            print(f"Landscape: {print_config.get('landscape', False)}")
            
            parameters = print_config.get('parameters', [])
            print(f"Số tham số: {len(parameters)}")

def validate_json_structure(data):
    """Validate cấu trúc JSON"""
    print("\n✅ VALIDATION:")
    print("-" * 40)
    
    errors = []
    warnings = []
    
    # Kiểm tra các trường bắt buộc
    required_sections = ['relatives', 'relationships']
    for section in required_sections:
        if section not in data:
            errors.append(f"Thiếu section: {section}")
    
    # Kiểm tra workflow steps
    if 'relatives' in data:
        if len(data['relatives']) < 2:
            warnings.append("Workflow có ít hơn 2 bước")
        
        for step in data['relatives']:
            if 'id' not in step:
                errors.append(f"Step thiếu ID: {step.get('summary', 'N/A')}")
            if 'type' not in step:
                errors.append(f"Step thiếu type: {step.get('summary', 'N/A')}")
    
    # Hiển thị kết quả
    if errors:
        print("❌ LỖI:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("✅ Không có lỗi cấu trúc")
    
    if warnings:
        print("⚠️ CẢNH BÁO:")
        for warning in warnings:
            print(f"  - {warning}")

def main():
    """Main function"""
    filename = "Untitled-1.json"
    
    print(f"🔍 REVIEW FILE: {filename}")
    print(f"⏰ Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Load JSON
    data = load_json_file(filename)
    if not data:
        sys.exit(1)
    
    # Phân tích
    analyze_workflow_structure(data)
    analyze_form_fields(data)
    analyze_table_structure(data)
    analyze_relationships(data)
    analyze_print_config(data)
    validate_json_structure(data)
    
    print("\n" + "=" * 60)
    print("🎉 REVIEW HOÀN THÀNH!")
    print("=" * 60)

if __name__ == "__main__":
    main() 