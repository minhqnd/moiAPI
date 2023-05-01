# color.py

from PIL import Image
import io

# Hàm tạo hình ảnh từ mã hex color
def create_image(hex_color):
    
    # Chuyển đổi mã hex color thành tuple RGB
    rgb_color = tuple(int(hex_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

    # Tạo hình ảnh với kích thước 200x200 và màu sắc tương ứng
    img = Image.new('RGB', (200, 200), rgb_color)

    # Trả về hình ảnh
    return img

# API trả về hình ảnh tương ứng với mã hex color
def get_image_from_hex(hex_color):
    """
    Lấy ảnh của màu từ mã hex
    """
    print(hex_color)
    # Tạo hình ảnh từ mã hex color
    img = create_image(hex_color)

    # Chuyển hình ảnh thành bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)

    # Trả về hình ảnh
    return img_bytes.getvalue()
