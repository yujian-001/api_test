from selenium import webdriver
driver=webdriver.Chrome(r"E:\chromedriver_win32\chromedriver.exe")
driver.get(r"C:\Users\Administrator\PycharmProjects\selenium_test\自动化测试\test1.html")
#当name不存在，selenium.common.exceptions.NoSuchElementException（没有对应的element对象）
#根据name属性的值查找
ele=driver.find_element_by_name("button")

print(ele.text)
print(type(ele))
print(ele.get_attribute("name"))
driver.quit()