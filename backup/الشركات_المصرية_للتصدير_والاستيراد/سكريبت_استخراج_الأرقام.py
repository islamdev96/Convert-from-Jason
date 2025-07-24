#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريبت لاستخراج أرقام الهواتف المحمولة الصحيحة من ملف JSON
يدعم أرقام الشبكات المصرية: 010, 011, 012, 015
"""

import json
import re
from typing import List, Dict, Any

def is_valid_egyptian_mobile(phone: str) -> bool:
    """
    فحص صحة رقم الهاتف المحمول المصري
    
    Args:
        phone (str): رقم الهاتف
        
    Returns:
        bool: True إذا كان الرقم صحيح، False إذا لم يكن كذلك
    """
    # إزالة المسافات والرموز الإضافية
    phone = re.sub(r'[^\d]', '', phone)
    
    # فحص الطول (11 رقم)
    if len(phone) != 11:
        return False
    
    # فحص أن الرقم يبدأ بأحد بادئات الشبكات المصرية
    valid_prefixes = ['010', '011', '012', '015']
    return any(phone.startswith(prefix) for prefix in valid_prefixes)

def extract_mobile_numbers(json_file: str) -> List[Dict[str, str]]:
    """
    استخراج أرقام الهواتف المحمولة الصحيحة من ملف JSON
    
    Args:
        json_file (str): مسار ملف JSON
        
    Returns:
        List[Dict]: قائمة بالأرقام الصحيحة مع أسماء أصحابها
    """
    try:
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        valid_numbers = []
        invalid_numbers = []
        
        # البحث في البيانات - التعامل مع البنية الجديدة
        if 'companies' in data and isinstance(data['companies'], list):
            print(f"عدد الشركات في البيانات: {len(data['companies'])}")
            for company in data['companies']:
                if 'contact_info' in company and 'phone' in company['contact_info']:
                    phone = str(company['contact_info']['phone'])
                    company_name = company.get('company_name_arabic', 'غير محدد')
                    
                    print(f"فحص الرقم: {phone} للشركة: {company_name}")
                    
                    # استخراج الأرقام من النص (قد يحتوي على أرقام متعددة)
                    phone_numbers = re.findall(r'\d{11}', phone)
                    
                    for single_phone in phone_numbers:
                        if is_valid_egyptian_mobile(single_phone):
                            valid_numbers.append({
                                'name': company_name,
                                'phone': single_phone,
                                'id': company.get('id', 'N/A')
                            })
                            print(f"  ✓ رقم صحيح: {single_phone}")
                        else:
                            invalid_numbers.append({
                                'name': company_name,
                                'phone': single_phone,
                                'reason': 'غير صحيح'
                            })
                            print(f"  ✗ رقم غير صحيح: {single_phone}")
        else:
            print("لا توجد بيانات شركات في الملف أو البيانات ليست في الشكل المتوقع")
        
        print(f"\nالأرقام غير الصحيحة:")
        for invalid in invalid_numbers:
            print(f"  - {invalid['name']}: {invalid['phone']}")
        
        return valid_numbers
        
    except FileNotFoundError:
        print(f"خطأ: لم يتم العثور على الملف {json_file}")
        return []
    except json.JSONDecodeError:
        print(f"خطأ: الملف {json_file} ليس ملف JSON صحيح")
        return []
    except Exception as e:
        print(f"خطأ غير متوقع: {e}")
        return []

def save_results(numbers: List[Dict[str, str]], output_file: str = 'valid_mobile_numbers.txt'):
    """
    حفظ النتائج في ملف نصي
    
    Args:
        numbers (List[Dict]): قائمة الأرقام الصحيحة
        output_file (str): اسم ملف الإخراج
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write("أرقام الهواتف المحمولة الصحيحة\n")
            file.write("=" * 40 + "\n\n")
            
            for i, number in enumerate(numbers, 1):
                file.write(f"{i}. {number['name']} - {number['phone']}\n")
            
            file.write(f"\nإجمالي الأرقام الصحيحة: {len(numbers)}\n")
        
        print(f"تم حفظ النتائج في الملف: {output_file}")
        
    except Exception as e:
        print(f"خطأ في حفظ الملف: {e}")

def main():
    """الدالة الرئيسية"""
    json_file = 'progress_page_460.json'
    
    print("بدء استخراج أرقام الهواتف المحمولة...")
    print("-" * 50)
    
    # التحقق من وجود الملف
    import os
    if not os.path.exists(json_file):
        print(f"خطأ: الملف {json_file} غير موجود")
        return
    
    print(f"تم العثور على الملف: {json_file}")
    
    # استخراج الأرقام
    valid_numbers = extract_mobile_numbers(json_file)
    
    if valid_numbers:
        print(f"تم العثور على {len(valid_numbers)} رقم صحيح:")
        print()
        
        # طباعة النتائج
        for i, number in enumerate(valid_numbers, 1):
            print(f"{i}. {number['name']} - {number['phone']}")
        
        # حفظ النتائج
        save_results(valid_numbers)
        
        # إنشاء ملف يحتوي على الأرقام فقط
        with open('mobile_numbers_only.txt', 'w', encoding='utf-8') as file:
            for number in valid_numbers:
                file.write(f"{number['phone']}\n")
        
        print(f"\nتم أيضاً حفظ الأرقام فقط في: mobile_numbers_only.txt")
        
    else:
        print("لم يتم العثور على أرقام صحيحة.")

if __name__ == "__main__":
    main()