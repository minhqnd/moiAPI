import qrcode


def generate_qr_code(data, size):
    """

    Generates a QR code image for the given data and size.

    Args:
        data (str): The data to be encoded in the QR code.
        size (tuple): A tuple of two integers representing the size of the QR code image.

    Returns:
        PIL.Image: The generated QR code image.

    Raises:
        ValueError: If the size x and y are not equal.

    """
    if size[0] != size[1]:
        raise ValueError("Size x and y must be equal")
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=size[0] // len(data),
        border=1,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img
