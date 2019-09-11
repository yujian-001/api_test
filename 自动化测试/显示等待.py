from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as es
from selenium.webdriver.common.by import By

driver=webdriver.Chrome(r"E:\chromedriver_win32\chromedriver.exe")
driver.get("https://www.baidu.com")

ele1=driver.find_element_by_id("kw")
ele1.send_keys("松勤")

ele2=driver.find_element_by_id("su1")
ele2.click()
#显示等待，对特定元素的等待动作
ele3=WebDriverWait(driver,60).until(es.presence_of_element_located((By.ID,"1")))
print(ele3.text)

if ele3.text.startswith("松勤网 - 松勤软件测试-软件测试在线教育领跑者-国内最专业的软件..."):
    print("pass")
else:
    print("failed")