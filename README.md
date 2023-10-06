# 作業機器人/Homework Bot
一個可以幫你記下作業並提醒你完成作業且功能強大的Discord機器人
A powerful Discord Bot that can help you to note your homework and remind you to complete it.

## 連結/Links
[![Discord Server](https://img.shields.io/badge/Discord%20Server-Join-brightgreen)](https://discord.gg/5UrGWXf3ba)
[![YouTube Channel](https://img.shields.io/badge/YouTube-Subscribe-red)](https://www.youtube.com/@JimmyXiaoXi)

- **加入Discord伺服器** 👉 (https://discord.gg/5UrGWXf3ba)
- **訂閱我👉** (https://www.youtube.com/@JimmyXiaoXi)

## 特色/功能
- ✅ 可以記下各科的作業
- ✅ 在 Discord 就可以輕鬆看到你今天獲知後要完成的作業
- ✅ 可選擇作業類型
- ✅ 可新增最多三個檔案，第一個如為圖片可直接顯示
- ✅ 可排定作業時間
- ⚠️ 定時私訊使用者作業
- ⚠️ 顯示作業完成/遲交等狀態

## 指令列表
- 被()括起來表示只能從選項中選一個
- 被<>括起來表示需替換為實際值
- 被[]括起來表示為選填
- 科目的選項: ["班級", "國文","英文","數學","物理","化學","生物","歷史","地理","公民與社會","地球科學","音樂","美術","體育","資訊科技"]
- 作業類型的選項: ["考試", "讀書", "寫作業", "攜帶物品", "填東西", "提醒"]
- 時間格式: YYYY/MM/DD
- `/添加作業 (科目) (作業類型) <作業名稱> <作業說明> [排定時間] [附件1] [附件2] [附件3]`
- `/移除作業 <時間> (科目) (作業類型) <作業名稱>`
- `/作業列表 [時間] [科目] [作業類型] [作業名稱]`

# **不想用我的機器人? 想自己架?**

## 需求
- Python 3.11 或更高之版本
- py-cord 2.4.1

## 操作方式(在自己電腦上跑)
- 請參考影片或是底下內容
1. 點右上角的 Download 按鈕，把檔案下載到您的電腦上並解壓縮
2. 輸入以下指令或是在你存放檔案資料夾裡面點右鍵 -> 在終端機中開啟
   ```bash
   cd <你的檔案存放的資料夾名稱>
3. 輸入以下指令來安裝必要之套件
   ```bash
   pip install -r requirements.txt
4. 接著使用底下的指令來執行
   ```bash
   python main.py
## 操作方式(在repl.it上跑)
- [請看此影片](https://www.google.com)