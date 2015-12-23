import unittest
from selenium import webdriver


class NewVisitorTest(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(2)

	def tearDown(self):
		self.browser.quit()

	def test_can_retrive_categories(self):
		self.browser.get('http://localhost:8000/rango')

		self.assertIn('Rango', self.browser.title)
		self.fail('Finish the test!')

# if __name__ == '__main__':
# 	unittest.main(warnings='ignore')


