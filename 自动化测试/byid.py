from selenium import webdriver
driver=webdriver.Chrome(r"E:\chromedriver_win32\chromedriver.exe")
driver.get(r"C:\Users\Administrator\PycharmProjects\selenium_test\自动化测试\test1.html")
#head里面的内容不能通过by_id找到元素
ele=driver.find_element_by_id("testing")

print(ele.text)