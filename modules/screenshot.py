from selenium import webdriver
import time


def take_screenshot(url):
    # Tạo driver cho trình duyệt Chrome
    driver = webdriver.Chrome()

    # Mở trang web được nhập từ người dùng
    driver.get(url)

    # Đợi cho trang web được tải hoàn tất
    time.sleep(5)

    # Chụp màn hình của trang web
    screenshot = driver.save_screenshot('screenshot.png')

    # Đóng trình duyệt
    driver.quit()

    # Trả về đường dẫn của hình ảnh screenshot
    return screenshot
