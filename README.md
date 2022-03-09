# get_horseracing_ticket
## 編集内容
- user_id = 会員番号
- pwd = ネットパスワード
- data_id = 日付(year + month + day)_競馬場のID(阪神 = 9)

以上の3点を編集。

## 環境
- Python 3.9.2
- Chrome 96.0.4664.45
- chromedriver-binary 96.0.4664.45.0
- selenium 4.0.0
- pygame 2.1.0

## 使用方法(2022年3月現在、2-2不要)
### 1. python3のインストール
   1. `python3 --version`でバージョンの確認
   2. インストールされていたらOK. されていないならインストール.
### 2-1. webdriver_managerのインストール (https://yuki.world/python-selenium-chromedriver-auto-update/)
   1. `pip install webdriver-manager`でインストール
---
### 2-2. chromedriver-binaryのインストール (https://taku-info.com/python-chromedriver-only-supports-chrome-vestion/)
   1. `pip install chromedriver-binary==<chromeのバージョン>`でchromeのドライバーをインストール
---
### 3. seleniumのインストール
   1. `pip install selenium`でseleniumのインストール
### 4. pygameのインストール
   1. `pip install pygame`でpygameのインストール
### 5. chromedriver, selenium, pygameがインストールされているか確認.
   1. `pip list`
### 6. 上記の3点の編集をソースコードに加える。
### 7. 実行
   1. `python script.py`