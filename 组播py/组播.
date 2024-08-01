from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# 设置Selenium WebDriver
driver = webdriver.Chrome()

# 包含多个网页URL的列表
urls = [
    'http://tonkiang.us/?page=1&name=东森',
    # 'http://example.com/page2',
]

# 保存网页内容的文件名
output_file = 'visible_text_content.txt'

# 打开文件准备写入
with open(output_file, 'w', encoding='utf-8') as file:
    for url in urls:
        try:
            # 访问网页
            driver.get(url)

            # 设置最大等待时间
            timeout = 10  # 10秒

            try:
                # 等待某个特定元素出现，例如页面的某个ID或类名
                element = WebDriverWait(driver, timeout).until(
                    EC.presence_of_element_located((By.ID, "some-id"))
                )
            except TimeoutException:
                print(f"在网页 {url} 中等待元素超时，跳过。")
                continue

            # 确保页面完全加载
            driver.implicitly_wait(timeout)  # 隐式等待

            # 获取所有可见的文本
            text = driver.find_element(By.TAG_NAME, 'body').text

            # 将文本写入文件
            file.write(text + '\n')

            print(f'网页 {url} 的可见文本已保存。')

        except Exception as e:
            print(f'处理网页 {url} 时发生错误：{e}')

# 关闭WebDriver
driver.quit()

print(f'所有网页的可见文本已保存到 {output_file} 文件中。')
