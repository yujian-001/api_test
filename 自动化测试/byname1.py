from selenium import webdriver
driver=webdriver.Chrome(r"E:\chromedriver_win32\chromedriver.exe")
driver.get(r"C:\Users\Administrator\PycharmProjects\selenium_test\自动化测试\test1.html")
eles=driver.find_elements_by_name("button") #ele为webelement列表对象
print(eles)  #webelement对象列表
for ele in eles:
    print(ele.text)
    print(ele.get_attribute("outerHTML"))
# print(ele.get_attribute("name"))
driver.quit()