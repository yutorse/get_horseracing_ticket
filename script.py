import time
import random
import pygame
import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

browser = webdriver.Chrome()
browser.maximize_window()

user_id='12345678' #会員番号
pwd='********' #ネットパスワード

date_id = "20000101_1" #日付_競馬場id 阪神→9 #名前変える必要あり

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
  pulldown_omakase = browser.find_element_by_id('p03A_auto_open') #これは日付, 競馬場が変わっても不変そう
  browser.execute_script('arguments[0].click();', pulldown_omakase)

  reservable_area_list = browser.find_elements_by_class_name('ticket_auto_link')
  if(len(reservable_area_list)>0):
    random_num = random.randint(0, len(reservable_area_list)-1)
    choice_area_button = reservable_area_list[random_num] #アルゴリズム改善の余地
    return choice_area_button
  else: #選択可能な指定席のエリアが見つかるまで更新を繰り返す。
    browser.refresh()
    print("area is not found")
    time.sleep(2) #インターバル
    choice_area()

def kariosae():
  choice_area_button = choice_area() #選択可能な指定席エリアのボタンが返ってくる。
  browser.execute_script('arguments[0].click();', choice_area_button)

  kariosae_button = browser.find_element_by_id('submitAButton') #仮押さえするボタン
  browser.execute_script('arguments[0].click();', kariosae_button)

  cancel_button = browser.find_elements_by_class_name('kariosae_cancel')
  if(len(cancel_button) > 0): #仮押さえキャンセルボタンがある = 仮押さえができている
    sound_notice()
  else:
    print("kariosae_failed")
    time.sleep(2) #インターバル
    kariosae()

def main():
  browser.get('https://jra.flpjp.com/')

  browser.find_element_by_id('userid').send_keys(user_id)
  browser.find_element_by_id('passwd').send_keys(pwd)
  browser.find_element_by_class_name('space-btm10').click()

  browser.get(f'https://jra.flpjp.com/seatSelect/{date_id}')

  kariosae()

  time.sleep(1000)
  browser.quit()

if __name__ == '__main__':
  main()

