import time
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import re
import os
import threading
from queue import Queue
from datetime import datetime
with open('合并.txt', 'r') as f:
    lines = f.readlines()

lines.sort()

with open('排序.txt', 'w') as f:
    for line in lines:
        f.write(line)
os.remove("合并.txt")
