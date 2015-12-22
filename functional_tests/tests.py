from selenium import webdriver

	
browser = webdriver.Firefox()
browser.get('localhost:8000/rango/')

assert 'Rango' in browser.title

browser.close()