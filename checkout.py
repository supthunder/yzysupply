from selenium import webdriver
from selenium.webdriver.common import action_chains, keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import time
import requests
from seleniumrequests import Firefox
from info import *
import requests
from bs4 import BeautifulSoup
import json
from printColor import*

variants = {}
link = ""



def getLink():
	# link = input("Enter link: ")
	link = "https://yeezysupply.com/products/womens-tubular-boot-pvc-transparent"


	sizeBrowser = webdriver.PhantomJS()
	sizeBrowser.get('https://yeezysupply.com/products/womens-tubular-boot-pvc-transparent')
	soup = BeautifulSoup(sizeBrowser.page_source,"html.parser")
	# print(soup.prettify())

	global variants
	startCheck = 0
	for option in soup.find_all('option'):
		if startCheck == 1:
			if option.get('class') == None:
				variants[str(option.text)] = str(option.get('value'))
		if str(option.text) == "SIZE":
			startCheck = 1
	print(variants)
	# print_green("Creating file...")
	# with open('variants.txt', 'w') as outfile:
	# 	json.dump(variants, outfile)

def atc():
	browser = Firefox()
	browser2 = Firefox()

	getLink()
	link = "https://yeezysupply.com/products/womens-tubular-boot-pvc-transparent"
	atc = "https://yeezysupply.com/cart/add.js"
	size = variants[input("Enter size: ")]
	payload = {
		"quantity":"1",
		"id":size
	}
	input("Press Enter load and add to cart...")

	# -------------- Go to link and ATC---------------
	browser.get(link)
	response = browser.request('POST', atc, data=payload)
	browser.get("https://yeezysupply.com/cart")
	browser.execute_script("document.getElementsByClassName('K__button CA__button-checkout')[0].click();")

	browser2.get(link)
	response = browser2.request('POST', atc, data=payload)
	browser2.get("https://yeezysupply.com/cart")
	browser2.execute_script("document.getElementsByClassName('K__button CA__button-checkout')[0].click();")



	# -------------- Go to shipping --------------
	input("CONTINUE TO SHIPPING...")
	for i in checkoutPayload:
		inputMsg = browser.find_element_by_id(i[0])
		inputMsg.send_keys(i[1])

	mySelect = Select(browser.find_element_by_id("checkout_shipping_address_province"))
	mySelect.select_by_value('Maryland')
	browser.execute_script("document.getElementsByClassName('step__footer__continue-btn btn')[0].click();")

	for i in checkoutPayload:
		inputMsg = browser2.find_element_by_id(i[0])
		inputMsg.send_keys(i[1])

	mySelect = Select(browser2.find_element_by_id("checkout_shipping_address_province"))
	mySelect.select_by_value('Maryland')
	browser2.execute_script("document.getElementsByClassName('step__footer__continue-btn btn')[0].click();")


	# -------------- Go to payment --------------
	input("CONTINUE TO PAYMENT METHOD...")
	browser.execute_script("document.getElementsByClassName('step__footer__continue-btn btn')[0].click();")
	browser2.execute_script("document.getElementsByClassName('step__footer__continue-btn btn')[0].click();")



	# -------------- Fill card --------------
	input("FILL CREDIT CARD...")
	eachFrame = 0
	for i in creditCard:
		frame = browser.find_elements_by_xpath('//iframe[@frameborder="0"]')[eachFrame]
		browser.switch_to.frame(frame);
		inputMsg = browser.find_element_by_id(i[0])
		for e in range(0,len(i)):
			inputMsg.send_keys(i[e])
		browser.switch_to.default_content()
		eachFrame += 1

	eachFrame = 0
	for i in creditCard:
		frame = browser2.find_elements_by_xpath('//iframe[@frameborder="0"]')[eachFrame]
		browser2.switch_to.frame(frame);
		inputMsg = browser2.find_element_by_id(i[0])
		for e in range(0,len(i)):
			inputMsg.send_keys(i[e])
		browser2.switch_to.default_content()
		eachFrame += 1



	# -------------- FINAL STEP CHECKOUT --------------
	print_warn("CHECKOUT?")
	input("")
	browser.execute_script("document.getElementsByClassName('step__footer__continue-btn btn')[0].click();")
	browser2.execute_script("document.getElementsByClassName('step__footer__continue-btn btn')[0].click();")





	time.sleep(10)
	browser.quit()

if __name__ == '__main__':
	atc()
