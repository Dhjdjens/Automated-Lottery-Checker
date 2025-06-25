import time # 用於處理時間相關操作 (例如延遲)
import re # 正則表達式模組，用於文字模式匹配
from bs4 import BeautifulSoup # 網頁解析函式庫，用於從HTML中提取資料
from selenium import webdriver # 自動化瀏覽器工具，用於模擬使用者操作網頁
from selenium.webdriver.common.by import By # 用於定位網頁元素的方式
from selenium.webdriver.support.ui import WebDriverWait # 用於設定網頁元素等待時間
from selenium.webdriver.support import expected_conditions as EC # 用於設定等待條件
from selenium.common.exceptions import TimeoutException # Selenium中超時錯誤的例外處理

# 威力彩開獎日期與期數的對照表 (內建日曆)
# 實際應用中，這個列表需要定期更新以包含最新開獎資料，特別是春節加碼期間
LOTTERY_SCHEDULE = [
    # 113年 (2024) 的開獎日期與期數
    {'date': '113/01/01', 'period': '113000001'}, {'date': '113/01/04', 'period': '113000002'},
    {'date': '113/01/08', 'period': '113000003'}, {'date': '113/01/11', 'period': '113000004'},
    {'date': '113/01/15', 'period': '113000005'}, {'date': '113/01/18', 'period': '113000006'},
    {'date': '113/01/22', 'period': '113000007'}, {'date': '113/01/25', 'period': '113000008'},
    {'date': '113/01/29', 'period': '113000009'}, {'date': '113/02/01', 'period': '113000010'},
    {'date': '113/02/05', 'period': '113000011'}, {'date': '113/02/12', 'period': '113000013'},
    {'date': '113/02/15', 'period': '113000014'}, {'date': '113/02/19', 'period': '113000015'},
    {'date': '113/02/22', 'period': '113000016'}, {'date': '113/02/26', 'period': '113000017'},
    {'date': '113/02/29', 'period': '113000018'}, {'date': '113/03/04', 'period': '113000019'},
    {'date': '113/03/07', 'period': '113000020'}, {'date': '113/03/11', 'period': '113000021'},
    {'date': '113/03/14', 'period': '113000022'}, {'date': '113/03/18', 'period': '113000023'},
    {'date': '113/03/21', 'period': '113000024'}, {'date': '113/03/25', 'period': '113000025'},
    {'date': '113/03/28', 'period': '113000026'}, {'date': '113/04/01', 'period': '113000027'},
    {'date': '113/04/04', 'period': '113000028'}, {'date': '113/04/08', 'period': '113000029'},
    {'date': '113/04/11', 'period': '113000030'}, {'date': '113/04/15', 'period': '113000031'},
    {'date': '113/04/18', 'period': '113000032'}, {'date': '113/04/22', 'period': '113000033'},
    {'date': '113/04/25', 'period': '113000034'}, {'date': '113/04/29', 'period': '113000035'},
    {'date': '113/05/02', 'period': '113000036'}, {'date': '113/05/06', 'period': '113000037'},
    {'date': '113/05/09', 'period': '113000038'}, {'date': '113/05/13', 'period': '113000039'},
    {'date': '113/05/16', 'period': '113000040'}, {'date': '113/05/20', 'period': '113000041'},
    {'date': '113/05/23', 'period': '113000042'}, {'date': '113/05/27', 'period': '113000043'},
    {'date': '113/05/30', 'period': '113000044'}, {'date': '113/06/03', 'period': '113000045'},
    {'date': '113/06/06', 'period': '113000046'}, {'date': '113/06/10', 'period': '113000047'},
    {'date': '113/06/13', 'period': '113000048'}, {'date': '113/06/17', 'period': '113000049'},
    {'date': '113/06/20', 'period': '113000050'}, {'date': '113/06/24', 'period': '113000051'},
    {'date': '113/06/27', 'period': '113000052'}, {'date': '113/07/01', 'period': '113000053'},
    {'date': '113/07/04', 'period': '113000054'}, {'date': '113/07/08', 'period': '113000055'},
    {'date': '113/07/11', 'period': '113000056'}, {'date': '113/07/15', 'period': '113000057'},
    {'date': '113/07/18', 'period': '113000058'}, {'date': '113/07/22', 'period': '113000059'},
    {'date': '113/07/25', 'period': '113000060'}, {'date': '113/07/29', 'period': '113000061'},
    {'date': '113/08/01', 'period': '113000062'}, {'date': '113/08/05', 'period': '113000063'},
    {'date': '113/08/08', 'period': '113000064'}, {'date': '113/08/12', 'period': '113000065'},
    {'date': '113/08/15', 'period': '113000066'}, {'date': '113/08/19', 'period': '113000067'},
    {'date': '113/08/22', 'period': '113000068'}, {'date': '113/08/26', 'period': '113000069'},
    {'date': '113/08/29', 'period': '113000070'}, {'date': '113/09/02', 'period': '113000071'},
    {'date': '113/09/05', 'period': '113000072'}, {'date': '113/09/09', 'period': '113000073'},
    {'date': '113/09/12', 'period': '113000074'}, {'date': '113/09/16', 'period': '113000075'},
    {'date': '113/09/19', 'period': '113000076'}, {'date': '113/09/23', 'period': '113000077'},
    {'date': '113/09/26', 'period': '113000078'}, {'date': '113/09/30', 'period': '113000079'},
    {'date': '113/10/03', 'period': '113000080'}, {'date': '113/10/07', 'period': '113000081'},
    {'date': '113/10/10', 'period': '113000082'}, {'date': '113/10/14', 'period': '113000083'},
    {'date': '113/10/17', 'period': '113000084'}, {'date': '113/10/21', 'period': '113000085'},
    {'date': '113/10/24', 'period': '113000086'}, {'date': '113/10/28', 'period': '113000087'},
    {'date': '113/10/31', 'period': '113000088'}, {'date': '113/11/04', 'period': '113000089'},
    {'date': '113/11/07', 'period': '113000090'}, {'date': '113/11/11', 'period': '113000091'},
    {'date': '113/11/14', 'period': '113000092'}, {'date': '113/11/18', 'period': '113000093'},
    {'date': '113/11/21', 'period': '113000094'}, {'date': '113/11/25', 'period': '113000095'},
    {'date': '113/11/28', 'period': '113000096'}, {'date': '113/12/02', 'period': '113000097'},
    {'date': '113/12/05', 'period': '113000098'}, {'date': '113/12/09', 'period': '113000099'},
    {'date': '113/12/12', 'period': '113000100'}, {'date': '113/12/16', 'period': '113000101'},
    {'date': '113/12/19', 'period': '113000102'}, {'date': '113/12/23', 'period': '113000103'},
    {'date': '113/12/26', 'period': '113000104'}, {'date': '113/12/30', 'period': '113000105'},
    # 114年 (2025) 的開獎日期與期數
    {'date': '114/01/02', 'period': '114000001'}, {'date': '114/01/06', 'period': '114000002'},
    {'date': '114/01/09', 'period': '114000003'}, {'date': '114/01/13', 'period': '114000004'},
    {'date': '114/01/16', 'period': '114000005'}, {'date': '114/01/20', 'period': '114000006'},
    {'date': '114/01/23', 'period': '114000007'}, {'date': '114/01/27', 'period': '114000008'},
    {'date': '114/01/30', 'period': '114000009'}, {'date': '114/02/03', 'period': '114000010'},
    {'date': '114/02/06', 'period': '114000011'}, {'date': '114/02/10', 'period': '114000012'},
    {'date': '114/02/13', 'period': '114000013'}, {'date': '114/02/17', 'period': '114000014'},
    {'date': '114/02/20', 'period': '114000015'}, {'date': '114/02/24', 'period': '114000016'},
    {'date': '114/02/27', 'period': '114000017'}, {'date': '114/03/03', 'period': '114000018'},
    {'date': '114/03/06', 'period': '114000019'}, {'date': '114/03/10', 'period': '114000020'},
    {'date': '114/03/13', 'period': '114000021'}, {'date': '114/03/17', 'period': '114000022'},
    {'date': '114/03/20', 'period': '114000023'}, {'date': '114/03/24', 'period': '114000024'},
    {'date': '114/03/27', 'period': '114000025'}, {'date': '114/03/31', 'period': '114000026'},
    {'date': '114/04/03', 'period': '114000027'}, {'date': '114/04/07', 'period': '114000028'},
    {'date': '114/04/10', 'period': '114000029'}, {'date': '114/04/14', 'period': '114000030'},
    {'date': '114/04/17', 'period': '114000031'}, {'date': '114/04/21', 'period': '114000032'},
    {'date': '114/04/24', 'period': '114000033'}, {'date': '114/04/28', 'period': '114000034'},
    {'date': '114/05/01', 'period': '114000035'}, {'date': '114/05/05', 'period': '114000036'},
    {'date': '114/05/08', 'period': '114000037'}, {'date': '114/05/12', 'period': '114000038'},
    {'date': '114/05/15', 'period': '114000039'}, {'date': '114/05/19', 'period': '114000040'},
    {'date': '114/05/22', 'period': '114000041'}, {'date': '114/05/26', 'period': '114000042'},
    {'date': '114/05/29', 'period': '114000043'}, {'date': '114/06/02', 'period': '114000044'},
    {'date': '114/06/05', 'period': '114000045'}, {'date': '114/06/09', 'period': '114000046'},
    {'date': '114/06/12', 'period': '114000047'},
]

def get_period_from_date(target_date):
    """
    根據給定的日期（民國年/月/日格式）查找對應的威力彩期數。
    """
    for draw in LOTTERY_SCHEDULE:
        if draw['date'] == target_date:
            return draw['period']
    return None

def get_html_by_period(period_number):
    """
    使用 Selenium 從台灣彩券官網抓取指定期數的威力彩開獎頁面原始碼。
    """
    url = 'https://www.taiwanlottery.com/lotto/result/super_lotto638'
    driver = None
    print(f"\n -> 正在用期數 {period_number} 進行查詢...")
    try:
        # 設定 Chrome 瀏覽器選項
        options = webdriver.ChromeOptions()
        options.add_argument('--headless') # 設定為無頭模式，即不顯示瀏覽器介面
        options.add_argument('--disable-gpu') # 禁用 GPU 加速，避免一些兼容性問題
        
        # 初始化 Chrome 瀏覽器驅動
        driver = webdriver.Chrome(options=options)
        
        # 設定最長等待時間，以確保網頁元素載入
        wait = WebDriverWait(driver, 15)
        
        # 開啟目標網頁
        driver.get(url)

        # 等待輸入期數的元素出現，然後輸入期數
        # 使用 XPath 定位輸入框，確保找到正確的元素
        period_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='請輸入九碼期別，例：113000001']")))
        period_input.send_keys(period_number) # 輸入期數

        # 找到查詢按鈕並點擊
        # 使用 CSS 選擇器定位查詢按鈕
        query_button = driver.find_element(By.CSS_SELECTOR, ".search-area-btn")
        # 使用 JavaScript 點擊按鈕，有時比直接 click() 方法更穩定
        driver.execute_script("arguments[0].click();", query_button)

        # 等待查詢結果的特定元素（包含期數的標題）出現，確認資料已載入
        # 使用 XPath 檢查包含目標期數的標題元素
        wait.until(EC.presence_of_element_located((By.XPATH, f"//div[@class='period-title' and contains(text(), '{period_number}')]")))
        print(" -> 查詢成功，已獲取網頁原始碼。")
        return driver.page_source # 返回網頁的原始HTML內容
    except TimeoutException:
        # 處理網頁載入或元素出現超時的錯誤
        print(f" -> 查詢期數 {period_number} 超時，可能網頁加載過慢或元素未出現。")
        return None
    except Exception as e:
        # 捕獲其他所有可能發生的錯誤
        print(f" -> 操作瀏覽器時發生錯誤: {e}")
        return None
    finally:
        # 無論是否發生錯誤，都確保瀏覽器被關閉
        if driver:
            driver.quit()

def parse_lotto_numbers(html_content):
    """
    解析 HTML 內容，提取威力彩開獎號碼。
    """
    # 使用 BeautifulSoup 解析 HTML 內容
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 查找包含開獎結果的主區塊 (通常會有特定的 class 名稱)
    item = soup.find('div', class_='result-item')
    if not item:
        # 如果找不到結果區塊，表示解析失敗或網頁結構變更，返回 None
        return None
    
    # 從結果區塊中提取期數
    period_tag = item.find('div', class_='period-title')
    period_number = period_tag.text.strip() if period_tag else "期數不明" # 提取文字並去除空白

    # 初始化號碼列表與特別號變數
    regular_numbers = [] # 用於儲存第一區中獎號碼
    special_number = '未找到' # 用於儲存第二區特別號碼

    # 查找包含所有號碼球的容器
    numbers_container = item.find('div', class_='winner-number-other-container')
    if numbers_container:
        # 找到所有具有 'ball' class 的 div 元素 (代表號碼球)
        all_balls = numbers_container.find_all('div', class_='ball')
        for ball in all_balls:
            # 根據號碼球的 class 判斷是否為特別號碼
            if 'color-super' in ball.get('class', []): # 檢查 class 列表中是否包含 'color-super'
                special_number = ball.text.strip() # 提取特別號碼
            else:
                regular_numbers.append(ball.text.strip()) # 提取第一區號碼
    
    # 返回解析後的字典格式數據
    return {'period': period_number, 'regular_numbers': regular_numbers, 'special_number': special_number}


# --- 主程式執行區塊 ---
while True: # 建立一個無限循環，讓使用者可以持續查詢
    # 提示使用者輸入查詢日期，並提供離開選項
    raw_date_input = input("\n請輸入要查詢的威力彩日期 (格式：年/月/日，民國年)，或按 Enter 離開: ")
    if not raw_date_input:
        print("程式已結束。") # 如果使用者按 Enter，則結束程式
        break
    
    # 日期格式化與合法性/範圍檢查
    try:
        # 將輸入的日期字串按 '/' 分割成 年、月、日 部分
        parts = raw_date_input.split('/')
        if len(parts) != 3: # 檢查分割後是否為三部分
            raise ValueError("日期格式錯誤，請確保為 '年/月/日'。")
        
        # 將年、月、日轉換為整數
        year_part = int(parts[0])
        month_part = f"{int(parts[1]):02d}" # 確保月份為兩位數格式（例如 01, 02）
        day_part = f"{int(parts[2]):02d}" # 確保日期為兩位數格式
        
        # <<< 日期範圍檢查 >>>
        # 限制查詢的年份必須在 113 年(含)以後
        if year_part < 113:
            print(" -> 112年以前的歷史資料，目前本系統不提供查詢")
            continue # 跳過本次循環，要求使用者重新輸入

        # 重新組合為標準化的日期格式
        normalized_date = f"{year_part}/{month_part}/{day_part}"
        # 如果原始輸入與標準化後的日期不同，則提示使用者
        if raw_date_input != normalized_date:
            print(f" -> 已將輸入日期標準化為: {normalized_date}")
            
    except Exception: # 捕獲任何在日期處理中發生的錯誤
        print(f" -> 錯誤：輸入的日期格式 '{raw_date_input}' 不正確。")
        continue # 跳過本次循環，要求使用者重新輸入
    
    # 查找期數
    # 根據標準化後的日期，在 LOTTERY_SCHEDULE 中查找對應的期數
    target_period = get_period_from_date(normalized_date)
    if not target_period:
        # 如果在內建日曆中找不到對應的期數，則提示錯誤
        print(f" -> 錯誤：在本程式的開獎日曆中找不到日期 {normalized_date}。")
        continue # 跳過本次循環

    print(f" -> 經查，日期 {normalized_date} 對應的期數為 {target_period}。")
    
    # 抓取並解析網頁資料
    html = get_html_by_period(target_period) # 呼叫函式獲取網頁原始碼
    if html:
        lotto_data = parse_lotto_numbers(html) # 呼叫函式解析原始碼，提取獎號
        if lotto_data: # 檢查是否成功解析到數據
            print("\n----------- 查詢結果 -----------")
            print(f"開獎日期: {normalized_date}")
            print(f"開獎期數: {lotto_data['period']}")
            print(f"第一區中獎號碼: {', '.join(lotto_data['regular_numbers'])}") # 將號碼列表用逗號連接
            print(f"第二區中獎號碼: {lotto_data['special_number']}")
            print("---------------------------------")
        else:
            print(" -> 在查詢結果頁面中找不到獎號資料。") # 若解析失敗或資料不完整
    else:
        print(" -> 抓取資料失敗。") # 若獲取網頁原始碼失敗

