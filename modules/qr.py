import qrcode


def generate_qr_code(data, size):
    if size[0] != size[1]:
        raise ValueError("Size x and y must be equal")
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=size[0]//len(data),
        border=1,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img
