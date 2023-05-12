from selenium import webdriver
import time


def take_screenshot(url):
    """

    Takes a screenshot of a webpage using Google Chrome browser and returns the path of the saved image.

    Args:
        url (str): The URL of the webpage to be captured.

    Returns:
        str: The path of the saved screenshot image.

    Example:
        take_screenshot('https://www.google.com')

    """
    # Tạo driver cho trình duyệt Chrome
    driver = webdriver.Chrome()

    # Mở trang web được nhập từ người dùng
    driver.get(url)

    # Đợi cho trang web được tải hoàn tất
    time.sleep(5)

    # Chụp màn hình của trang web
    screenshot = driver.save_screenshot("screenshot.png")

    # Đóng trình duyệt
    driver.quit()

    # Trả về đường dẫn của hình ảnh screenshot
    return screenshot
