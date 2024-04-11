from selenium import webdriver
import unittest
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
         self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        #张三
        self.browser.get('http://localhost:8000')
        #他注意到
        self.assertIn('To-Do',self.browser.title)
            #,"browser title was:" + self.browser.title
        header_text=self.browser.find_element(By.TAG_NAME,'h1').text
        self.assertIn('To-Do',header_text)

        #应用有
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        # self.assertEqual(
        #     inputbox.get_attribute('placeholder'),
        #     'Enter a to-do item'
        # )
        #他在文本输入框
        # inputbox.send_keys('Buy flowers')
        #他按了
        inputbox.send_keys('Give a gift to Lisi')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # 页面再次更新
        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertIn('1: Buy flowers', [row.text for row in rows])
        self.assertIn('2: Give a gift to Lisi', [row.text for row in rows])
#页面中
        self.fail('Finish the test!')
if __name__== '__main__':
    unittest.main()
# 张三听说有一个在线待办事项的应用#