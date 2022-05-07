import os
import time
import random
import pygame
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import JavascriptException
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(verbose=True, dotenv_path=dotenv_path)

user_id = os.getenv("JRA_USER") #会員番号
pwd = os.getenv("JRA_PASS") #ネットパスワード

print("日付を yyyymmdd の形式で入力してください")
date = input()
print("競馬場IDを入力してください\n--------------------------\n新潟 : 4\n東京 : 5\n中京 : 7\n阪神 : 9\n--------------------------")
course_id = input()
date_id = date + "_" + course_id #日付_競馬場id 阪神→9 中京→7

browser = webdriver.Chrome(ChromeDriverManager().install())
browser.maximize_window()

def overlay_handle():
  if(browser.find_element_by_class_name('attention-agree-checkbox') > 0):
    browser.find_element_by_class_name('attention-agree-checkbox').click()
    browser.find_element_by_class_name('attention-button-area').click()

def sound_notice():
  pygame.mixer.init(frequency = 44100) #初期化
  pygame.mixer.music.load("horseracing_fanfare.mp3")  #音楽ファイルの読み込み
  pygame.mixer.music.play(10)
  while(1):
      a = input("Finish? --->")
      if(a == 'y'): break
  pygame.mixer.music.stop() #yが入力されるまでファンファーレをかける
  return 0

def choice_area():
  while True:
    pulldown_omakase = browser.find_element_by_id('p03A_auto_open')
    browser.execute_script('arguments[0].click();', pulldown_omakase)
    reservable_area_list = browser.find_elements_by_class_name('ticket_auto_link')

    if(len(reservable_area_list) > 0):
      break
    else:
      print("area is not found")
      browser.refresh()
      time.sleep(2) #インターバル

  random_num = random.randint(0, len(reservable_area_list)-1)
  choice_area_button = reservable_area_list[random_num] #アルゴリズム改善の余地
  return choice_area_button

def kariosae():
  while True:
    choice_area_button = choice_area()

    try:
      browser.execute_script('arguments[0].click();', choice_area_button)
    except JavascriptException:
      print("JavascriptException")
      print("\007")
      kariosae()

    kariosae_button = browser.find_element_by_id('submitAButton') #仮押さえするボタン
    browser.execute_script('arguments[0].click();', kariosae_button)
    cancel_button = browser.find_elements_by_class_name('kariosae_cancel')

    if(len(cancel_button) > 0): #仮押さえキャンセルボタンがある = 仮押さえができている
      break
    else:
      print("kariosae_failed")
      time.sleep(2) #インターバル

  sound_notice()

def main():
  browser.get('https://jra.flpjp.com/')

  browser.find_element_by_id('userid').send_keys(user_id)
  browser.find_element_by_id('passwd').send_keys(pwd)
  browser.find_element_by_id('btn_login_submit').click()

  browser.get(f'https://jra.flpjp.com/seatSelect/{date_id}')

  kariosae()

  time.sleep(1000)
  browser.quit()

if __name__ == '__main__':
  main()

