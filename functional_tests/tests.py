from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common.exceptions import WebDriverException

MAX_WAIT=10

class NewVisitorTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
         self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:  # (2)
            try:
                table = self.browser.find_element(By.ID, 'id_list_table')  # (3)
                rows = table.find_elements(By.TAG_NAME,'tr')
                self.assertIn(row_text, [row.text for row in rows])
                return  # (4)
            except(AssertionError,WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

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
        self.wait_for_row_in_list_table('1: Buy flowers')

        # 页面中又显示了一个文本框，可以输入其他的待办事项
        # 他输入了“Give a gift to Lisi”
        inputbox = self.browser.find_element(By.ID,'id_new_item')
        inputbox.send_keys('Give a gift to Lisi')
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: Buy flowers')
        self.wait_for_row_in_list_table('2: Give a gift to Lisi')
        #张三想知道这个网站

    def test_multiple_users_can_start_lists_at_different_urls(self):
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Buy flowers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy flowers')

        #他注意到
        zhangsan_list_url = self.browser.current_url
        self.assertRegex(zhangsan_list_url, '/lists/.+') #(1)
        #现在有一个新用户
        self.browser.quit()
        self.browser = webdriver.Chrome()
        #王五访问首页
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Buy flowers', page_text)
        self.assertNotIn('BGive a gift to Lisi', page_text)
        #王五输入
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        #王五获得了
        wangwu_list_url = self.browser.current_url
        self.assertRegex(wangwu_list_url, '/lists/.+')
        self.assertNotEqual(wangwu_list_url, zhangsan_list_url)
        #这个页面还是
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Buy flowers', page_text)
        self.assertIn('Buy milk', page_text)

    def test_layout_and_styling(self):
        # 访问首页
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)
        # 她完美的居中
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )
        #他居中
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )

