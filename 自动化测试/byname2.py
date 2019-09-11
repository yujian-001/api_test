from selenium import webdriver
import selenium
driver=webdriver.Chrome(r"E:\chromedriver_win32\chromedriver.exe")
driver.get(r"C:\Users\Administrator\PycharmProjects\selenium_test\自动化测试\test1.html")
#当name不存在，selenium.common.exceptions.NoSuchElementException（没有对应的element对象）
#根据name属性的值查找
try:
    ele=driver.find_element_by_name("button1")
except selenium.common.exceptions.NoSuchElementException:
    print("不存在的name")
driver.quit()