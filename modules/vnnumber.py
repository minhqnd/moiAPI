from vietnam_number import n2w, w2n

def is_integer_string(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def convert_data(data):
    try:
        if is_integer_string(data):
            # Nếu chuỗi là số nguyên
            result = n2w(data)
        elif isinstance(data, str):
            # Nếu là chuỗi thông thường
            result = w2n(data)
        else:
            raise ValueError("Dữ liệu không hợp lệ")
        
        return result
    except Exception as e:
        return "Số không hợp lệ"
