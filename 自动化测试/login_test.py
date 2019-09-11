from selenium import webdriver
driver=webdriver.Chrome(r"E:\chromedriver_win32\chromedriver.exe")
driver.get("https://github.com/login")

ele=driver.find_element_by_id("login_field")
ele.send_keys("18986032799@163.com")
# print(ele.text)
ele1=driver.find_element_by_id("password")
ele1.send_keys("wxq19910930..")

ele2=driver.find_element_by_name("commit")
ele2.click()


# driver.quit()