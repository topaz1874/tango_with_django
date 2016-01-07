from selenium import webdriver
from django.test import LiveServerTestCase
import time



class NewVisitorTest(LiveServerTestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()

	def tearDown(self):
		self.browser.quit()

	def test_can_retrive_categories(self):
		self.browser.get('http://localhost:8000/rango')

		self.assertIn('Rango', self.browser.title)
		# self.fail('Finish the test!')
		
	# def switch_to_new_window(self, text_in_title):
	# 	retries = 60
	# 	while retries >0:
	# 		for handle in self.browser.window_handles:
	# 			self.browser.switch_to_window(handle)
	# 			if text_in_title in self.browser.title:
	# 				return 
	# 		retries -= 1
	# 		time.sleep(0.5)
	# 	self.fail('could not find window')

	# def test_login(self):
	# 	self.browser.get('http://localhost:8000/accounts/login')
	# 	username_input = self.browser.find_element_by_id('id_username')
	# 	username_input.send_keys('test')
	# 	username_input = self.browser.find_element_by_id('id_password')
	# 	username_input.send_keys('123')
	# 	username_input.send_keys('/n')
		# self.switch_to_new_window('rango')
		# navbar = self.browser.find_element_by_css_selector('.navbar')
		# print self.browser.find_element_by_class_name('main').text
    	# self.browser.find_element_by_xpath('//input[@value="Log in"]').click()

# if __name__ == '__main__':
# 	unittest.main(warnings='ignore')


