from selenium import webdriver
from pyvirtualdisplay import Display
display = Display(visible=0, size=(1024, 768))
display.start()
path = '/home/ubuntu/sparta/chromedriver'
browser = webdriver.Chrome(path)

