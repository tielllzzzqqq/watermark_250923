# 图片水印添加工具

这个工具可以读取图片的EXIF信息中的拍摄时间，并将其作为水印添加到图片上。

## 功能特点

- 自动从图片EXIF数据中提取拍摄日期
- 如果EXIF数据不可用，尝试从文件名中提取日期信息
- 支持自定义水印字体大小、颜色和位置
- 批量处理目录中的所有图片
- 将处理后的图片保存到新的子目录中

## 使用方法

```bash
python image_watermark.py 图片目录路径 [选项]
```

### 选项

- `--font-size`: 水印字体大小（默认：30）
- `--font-color`: 水印颜色（默认：white，支持：white, black, red, green, blue）
- `--position`: 水印位置（默认：right_bottom，支持：left_top, center, right_bottom）

### 示例

```bash
# 使用默认设置
python image_watermark.py /path/to/images

# 自定义水印设置
python image_watermark.py /path/to/images --font-size 40 --font-color red --position center
```

## 依赖项

- Python 3.6+
- Pillow (PIL Fork)

## 安装依赖

```bash
pip install Pillow
```