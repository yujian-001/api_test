from selenium import webdriver

driver=webdriver.Chrome(r"E:\chromedriver_win32\chromedriver.exe")
driver.implicitly_wait(10) #后面的操作都会等待操作

driver.get("http://www.baidu.com")

element_value=driver.find_element_by_id('kw')
element_value.send_keys("松勤")

element_button=driver.find_element_by_id("su")
element_button.click()

ret=driver.find_element_by_id("1")
print(ret.text,type(ret.text))

#通过字符串判断搜索到的内容
if ret.text.startswith("松勤网 - 松勤软件测试-软件测试在线教育领跑者-国内最专业的软件..."):
    print("测试通过")
else:
    print("测试不通过")

driver.quit()