from django.test import TestCase
from splinter import Browser
import time

# Create your tests here.
class PyPoetTestCase(TestCase):
    with Browser() as browser:
        url = "http://localhost:8000/"
        browser.visit(url)
        submit = browser.find_by_id('submit_button')
        submit.click()
        print("Clicked submit [default]")
        while browser.is_text_not_present('100%'):
            time.sleep(3)
            print("Sleeping [default]")
        print("Done [default]")
        time.sleep(10)

    def test_quick(self):
        with Browser() as browser:
            url = "http://localhost:8000/"
            browser.visit(url)
            browser.fill('TotalLines', "1")
            print("Filled forms [quick]")
            submit = browser.find_by_id('submit_button')
            submit.click()
            print("Clicked submit [quick]")
            while browser.is_text_not_present('100%'):
                time.sleep(3)
                print("Sleeping [quick]")
            print("Done [quick]")
            time.sleep(10)

    def test_long(self):
        with Browser() as browser:
            url = "http://localhost:8000/"
            browser.visit(url)
            browser.fill('TotalLines', "11")
            print("Filled forms [long]")
            submit = browser.find_by_id('submit_button')
            submit.click()
            print("Clicked submit [long]")
            while browser.is_text_not_present('100%'):
                time.sleep(3)
                print("Sleeping [long]")
            print("Done [long]")
            time.sleep(10)