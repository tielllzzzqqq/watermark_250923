#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import argparse
from PIL import Image, ImageDraw, ImageFont
from PIL.ExifTags import TAGS
import datetime
import glob

def get_exif_date(image_path):
    """从图片中提取EXIF拍摄日期信息"""
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()
        if exif_data is None:
            return None
        
        # 查找日期时间原始数据标签
        date_time = None
        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)
            if tag == 'DateTimeOriginal':
                date_time = value
                break
            elif tag == 'DateTime':
                date_time = value
        
        # 如果找到日期，提取年月日
        if date_time:
            # 日期格式通常为 "YYYY:MM:DD HH:MM:SS"
            date_parts = date_time.split()
            if date_parts and len(date_parts) > 0:
                ymd = date_parts[0].replace(':', '-')
                return ymd
        
        return None
    except Exception as e:
        print(f"读取EXIF信息时出错: {e}")
        return None

def add_watermark(image_path, output_path, font_size=30, font_color=(255, 255, 255), position='right_bottom'):
    """向图片添加水印"""
    try:
        # 打开图片
        image = Image.open(image_path)
        
        # 获取拍摄日期
        date_text = get_exif_date(image_path)
        if not date_text:
            # 如果无法从EXIF获取日期，尝试从文件名获取
            filename = os.path.basename(image_path)
            if "IMG" in filename and len(filename) > 8:
                # 尝试从类似 "IMG20250920182241.jpg" 的文件名中提取日期
                try:
                    date_part = filename.split("IMG")[1][:8]
                    year = date_part[:4]
                    month = date_part[4:6]
                    day = date_part[6:8]
                    date_text = f"{year}-{month}-{day}"
                except:
                    date_text = "未知日期"
            else:
                date_text = "未知日期"
        
        # 创建绘图对象
        draw = ImageDraw.Draw(image)
        
        # 设置字体
        try:
            # 尝试使用系统字体
            font = ImageFont.truetype("Arial", font_size)
        except:
            # 如果找不到指定字体，使用默认字体
            font = ImageFont.load_default()
        
        # 计算文本大小 (使用textbbox代替已弃用的textsize)
        left, top, right, bottom = font.getbbox(date_text)
        text_width = right - left
        text_height = bottom - top
        
        # 确定水印位置，增加边距使水印不挨着图片边缘
        width, height = image.size
        margin = 50  # 设置更大的边距
        if position == 'left_top':
            position = (margin, margin)
        elif position == 'center':
            position = ((width - text_width) // 2, (height - text_height) // 2)
        elif position == 'right_bottom':
            position = (width - text_width - margin, height - text_height - margin)
        else:  # 默认右下角
            position = (width - text_width - margin, height - text_height - margin)
        
        # 直接绘制水印文本，不添加背景
        draw.text(position, date_text, font_color, font=font)
        
        # 保存图片
        image.save(output_path)
        print(f"已保存水印图片: {output_path}")
        return True
    except Exception as e:
        print(f"添加水印时出错: {e}")
        return False

def process_directory(input_dir, font_size=30, font_color=(255, 255, 255), position='right_bottom'):
    """处理目录中的所有图片文件"""
    # 创建输出目录
    output_dir = os.path.join(input_dir, os.path.basename(input_dir) + "_watermark")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 支持的图片格式
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp']
    image_files = []
    
    # 获取所有图片文件
    for ext in image_extensions:
        pattern = os.path.join(input_dir, ext)
        image_files.extend(glob.glob(pattern))
    
    # 处理每个图片
    success_count = 0
    for image_path in image_files:
        filename = os.path.basename(image_path)
        output_path = os.path.join(output_dir, filename)
        if add_watermark(image_path, output_path, font_size, font_color, position):
            success_count += 1
    
    print(f"处理完成! 共处理 {len(image_files)} 个文件，成功添加水印 {success_count} 个。")
    return output_dir

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='给图片添加拍摄日期水印')
    parser.add_argument('input_dir', help='输入图片目录路径')
    parser.add_argument('--font-size', type=int, default=30, help='水印字体大小 (默认: 30)')
    parser.add_argument('--font-color', default='white', help='水印颜色 (默认: white，支持: white, black, red, green, blue)')
    parser.add_argument('--position', default='right_bottom', 
                        choices=['left_top', 'center', 'right_bottom'],
                        help='水印位置 (默认: right_bottom)')
    
    args = parser.parse_args()
    
    # 检查输入目录是否存在
    if not os.path.isdir(args.input_dir):
        print(f"错误: 目录 '{args.input_dir}' 不存在")
        return 1
    
    # 颜色映射
    color_map = {
        'white': (255, 255, 255),
        'black': (0, 0, 0),
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255)
    }
    
    font_color = color_map.get(args.font_color.lower(), (255, 255, 255))
    
    # 处理目录
    output_dir = process_directory(args.input_dir, args.font_size, font_color, args.position)
    print(f"水印图片已保存到: {output_dir}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())