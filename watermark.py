import os
import sys
sys.path.append(r"D:\Lib\site-packages")
from PIL import Image, ImageDraw, ImageFont
import piexif
import datetime

def get_photo_time(image_path):
    """获取取EXIF拍摄时间"""
    try:
        img = Image.open(image_path)
        exif = img._getexif()
        if exif:
            for tag, value in exif.items():
                tag_name = ExifTags.TAGS.get(tag, tag)
                if tag_name == "DateTimeOriginal":
                    return value
    except Exception:
        pass

def add_watermark(image_path, text, font_size=30, color="white", position="right_bottom"):
    """加水印"""
    img = Image.open(image_path).convert("RGBA")

    # 创建透明图层
    txt_layer = Image.new("RGBA", img.size, (255,255,255,0))
    draw = ImageDraw.Draw(txt_layer)
    try:
        font = ImageFont.truetype("arial.ttf", font_size)  # Windows下常见字体
    except:
        font = ImageFont.load_default()
    # 获取文字大小
    bbox = draw.textbbox((0,0), text, font=font)
    text_w, text_h = bbox[2]-bbox[0], bbox[3]-bbox[1]
    # 定位
    if position == "left_top":
        pos = (10, 10)
    elif position == "right_top":
        pos = (img.width - text_w - 10, 10)
    elif position == "left_bottom":
        pos = (10, img.height - text_h - 10)
    elif position == "center":
        pos = ((img.width - text_w)//2, (img.height - text_h)//2)
    else:  # 默认右下角
        pos = (img.width - text_w - 10, img.height - text_h - 10)
    # 画文字
    draw.text(pos, text, font=font, fill=color)
    # 合并图层
    watermarked = Image.alpha_composite(img, txt_layer).convert("RGB")
    return watermarked

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python watermark.py <图片文件夹路径>")
        sys.exit(1)

    folder = sys.argv[1]
    font_size = int(input("水印字体大小 (默认 30): ") or 30)
    color = input("水印颜色 (默认 white): ") or "white"
    position = input("水印位置 (left_top, right_top, left_bottom, right_bottom, center，默认 right_bottom): ") or "right_bottom"

    for filename in os.listdir(folder):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            path = os.path.join(folder, filename)
            try:
                time_text = get_photo_time(path)
                wm = add_watermark(path, time_text, font_size, color, position)
                output_path = os.path.join(folder, f"wm_{filename}")
                wm.save(output_path)
                print(f"已处理并保存: {output_path}")
            except Exception as e:
                print(f"处理 {filename} 出错:", e)
