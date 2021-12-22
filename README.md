## 一級方程式 積分分析
### Python 爬蟲、視覺化、視窗化 整合專題

![image](https://i.ibb.co/2sk1s9z/jj.gif)
### 流程簡介
| 步驟 | 使用模組 | 補充說明 |
| --- | --- | --- |
| `1擷取網頁` | selenium webdriver | windows 使用者需額外<br>下載 chromedriver
| `2解析網頁` | BeautifulSoup |
|`3轉成csv`|pandas<br>csv| pandas to_csv 抓 table
|`4存進資料庫`|sqlite3| 
|`5視覺化`|matplotlib.pyplot| 產生 "chart.png" 圖檔
|`6視窗化`|tkinter| 

|按鈕|功能說明|
|---|---|
|`Search`|執行上表步驟1~5<br>自動刪除".csv"與".db"檔案|
|`Delete`|刪除右側目前圖表|
|`Close`|關閉視窗<br>自動刪除"chart.png"圖檔|
