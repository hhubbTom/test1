from selenium import webdriver
# import unittest
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from django.test import LiveServerTestCase

class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
         self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        #张三
        self.browser.get(self.live_server_url)
        #他注意到
        self.assertIn('To-Do', self.browser.title)
            #,"browser title was:" + self.browser.title
        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('To-Do', header_text)

        #应用邀请他输入一个待办事项
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )
        #他在文本框中输入了“Buy flowers”
        inputbox.send_keys('Buy flowers')
        # 他按回车键后，页面更新了
        # 待办事项表格中显示了“1: Buy flowers”

        inputbox.send_keys(Keys.ENTER)#（3）
        time.sleep(2)
        self.check_for_row_in_list_table('1: Buy flowers')

        # 页面中又显示了一个文本框，可以输入其他的待办事项
        # 他输入了“Give a gift to Lisi”
        inputbox = self.browser.find_element(By.ID,'id_new_item')
        inputbox.send_keys('Give a gift to Lisi')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        self.check_for_row_in_list_table('1: Buy flowers')
        self.check_for_row_in_list_table('2: Give a gift to Lisi')
        #张三想知道这个网站
        self.fail('Finish the test!')

# 张三听说有一个在线待办事项的应用#