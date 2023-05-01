from PIL import Image
import io

def create_image(input_color):
    """
    Tạo hình ảnh từ mã hex hoặc RGB

    Args:
        color (str or tuple): Chuỗi mã hex color hoặc tuple RGB.

    Returns:
        PIL.Image: Hình ảnh với kích thước 200x200 và màu sắc tương ứng.
    """
    # Kiểm tra nếu chuỗi đầu vào là một tuple RGB dưới dạng chuỗi
    if isinstance(input_color, str) and input_color.startswith("(") and input_color.endswith(")"):
        # Sử dụng hàm eval() để chuyển chuỗi thành tuple RGB
        rgb_color = eval(input_color)
    # Nếu không, giả sử đầu vào là chuỗi hex color
    else:
        # Chuyển đổi mã hex color thành tuple RGB
        rgb_color = tuple(int(input_color.lstrip(
            '#')[i:i+2], 16) for i in (0, 2, 4))

    # Tạo hình ảnh với kích thước 200x200 và màu sắc tương ứng
    img = Image.new('RGB', (200, 200), rgb_color)
    # Trả về hình ảnh
    return img

def get_image_from_hex(color, size=None):
    """
    Lấy hình ảnh tương ứng với mã hex color

    Args:
        color (str or tuple): Chuỗi mã hex color hoặc tuple RGB.
        size (tuple, optional): Kích thước mới của hình ảnh. Defaults to None.

    Returns:
        bytes: Hình ảnh tương ứng với mã hex color.
    """
    # Tạo hình ảnh từ mã hex color hoặc tuple RGB
    img = create_image(color)

    # Resize hình ảnh nếu có yêu cầu kích thước
    if size:
        img = img.resize(size)

    # Chuyển hình ảnh thành bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)

    return img_bytes.getvalue()

def is_rgb(color):
    """
    Kiểm tra xem một giá trị có phải là một tuple RGB hợp lệ hay không

    Args:
        color (Any): Giá trị cần kiểm tra.

    Returns:
        bool: True nếu giá trị là một tuple RGB hợp lệ, False nếu không.
    """
    return isinstance(color, tuple) and len(color) == 3 and all(0 <= c <= 255 for c in color)
