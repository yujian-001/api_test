from selenium import webdriver
import time

#指定chrome的webdriver驱动，返回一个驱动对象--driver
driver=webdriver.Chrome(r"E:\chromedriver_win32\chromedriver.exe")

#get方法打开指定的网页
driver.get("https://www.baidu.com")

#根据id查找网页输入框对象，返回一个webelement对象(element_value)
element_value=driver.find_element_by_id('kw')

#在输入框输入关键字
element_value.send_keys("松勤")

#根据id查找网页button对象
element_button=driver.find_element_by_id("su")
#调用click（）方法
element_button.click()

time.sleep(3)

ret=driver.find_element_by_id("1")
print(ret.text,type(ret.text))

#通过字符串判断搜索到的内容
if ret.text.startswith("松勤网 - 松勤软件测试-软件测试在线教育领跑者-国内最专业的软件..."):
    print("测试通过")
else:
    print("测试不通过")
ret.click()
# driver.quit()