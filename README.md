# 初始化
啟動與驗證第一步在 fullstack-e2e-docker 
- 根目錄執行：`Bashdocker compose up -d --build`

1. 啟動後打開瀏覽器驗證：前端操作介面：http://localhost:8080
 - 1. 新增「購買機械鍵盤」、金額 3500、分類 3C周邊。
 - 2. 點擊該列的 編輯，將金額改為 3200 後按 儲存，再按 F5 重新整理確認資料已寫入資料庫。
 - 3. 測試 刪除 按鈕是否正常移除該項目。後端 Swagger 文件：http://localhost:8030/docs
2. 後端 Swagger 文件：http://localhost:8030/docs