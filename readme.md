# Container/BL Redirect Tracker

A web application for redirecting users to the appropriate shipping company tracking page based on Container Number or Bill of Lading (BL) Number.

## Features

- Input Container Number or BL Number
- Automatic detection of shipping company based on input
- Redirect to shipping company tracking page in a new tab
- Display of supported shipping companies with logos
- Mobile responsive design
- Google Analytics integration

## Tech Stack

- Next.js 14
- React 18
- TypeScript
- Tailwind CSS

## Getting Started

### Prerequisites

- Node.js 16+
- npm or yarn

### Installation

1. Clone the repository
   ```
   git clone https://github.com/yourusername/container-bl-redirect-tracker.git
   cd container-bl-redirect-tracker
   ```

2. Install dependencies
   ```
   npm install
   # or
   yarn install
   ```

3. Configure environment variables
   Create a `.env.local` file in the root directory with:
   ```
   NEXT_PUBLIC_GA_ID=your-google-analytics-id
   ```

4. Add shipping company logos
   Place shipping company logo images in the `public/images` directory. The image filenames should match those defined in `app/utils/shippingCompanies.ts`.

5. Start the development server
   ```
   npm run dev
   # or
   yarn dev
   ```

6. Open [http://localhost:3000](http://localhost:3000) in your browser

## Deployment

The application can be deployed to Vercel, Netlify, or any other platform supporting Next.js.

```
npm run build
npm run start
```

## License

MIT

📦 Container/BL Redirect Tracker - Product Specification (MVP)

🧭 產品目標

建立一個供 B2B 使用者 使用的網站，能夠根據輸入的 Container Number 或 Bill of Lading Number (BL)，自動判斷應跳轉至哪一家航運公司，並於新分頁中開啟查詢結果頁面，協助客戶快速進行物流追蹤查詢。

⸻

🧑‍💼 目標用戶
	•	國內外 B2B 用戶（如：貨運代理、報關行、倉儲物流人員）
	•	對象熟悉貨櫃、提單操作流程
	•	語言：英文

⸻

🖥️ 使用流程（User Flow）
	1.	使用者進入網站首頁
	2.	選擇「BL Number」或「Container Number」欄位並輸入查詢碼
	3.	按下「Search」
	4.	系統自動根據編碼前綴判斷應屬航運公司
	5.	開啟一個新分頁，導向該航運公司網站的查詢結果頁（非首頁）
	6.	若無法匹配或格式錯誤，顯示錯誤訊息，不跳轉

⸻

🔡 輸入欄位
	•	共三個欄位（僅其中兩個 MVP 開發）：
	
	1.	BL Number
	2.	Container Number
	3.	Booking Number（暫不實作）
	•	不進行欄位類型自動識別
	•	使用者需手動輸入對應欄位
	•	基本格式驗證（例如 Container 號應為4碼字母end with letter "U"+7碼數字）

⸻

🔍 航運公司支援清單（含簡碼對應）

航運公司名稱	常見代碼/簡碼	Logo 檔名
Maersk	MAEU	maersk.png
COSCO	COSU	cosco.png
Wan Hai	WHLC	wanhai.png
SeaLead	SEAU	sealead.png
HMM	HDMU	hmm.png
MSC	MSCU	msc.png
ONE	ONEU	one.png
ZIM	ZIMU	zim.png
Yang Ming	YMLU	yangming.png
OOCL	OOLU	oocl.png
Hapag-Lloyd	HLCU	hlcu.png
CMA CGM	CMDU	cmdu.png
Evergreen	EGLV	eglv.png

※ 若一組編號對應多家航運公司，系統隨機選擇一間跳轉。

⸻

🌐 跳轉邏輯
	•	所有查詢均在新分頁開啟
	•	跳轉 URL 為含參數的查詢結果頁，而非首頁
	•	會根據輸入自動拼接網址格式（如 https://exampleline.com/track?bl=XXXX）

⸻

📱 UI 設計
	•	簡約設計，具備航運公司 Logo 輔助識別
	•	Logo 命名規則為：公司名.png
	•	必須具備基礎 Mobile Responsive 設計（不支援微信/內建瀏覽器）
	•	輸入後按下「Search」按鈕即執行跳轉（不可 auto-submit）

⸻

❗ 錯誤處理
	•	若輸入不符合格式或無法判別公司：
	•	顯示錯誤訊息（如：「Invalid container number format」）
	•	不執行跳轉

⸻

📊 第三方追蹤（Analytics）
	•	加入 Google Analytics v4 追蹤碼
	•	追蹤項目：
	•	查詢次數
	•	進站來源
	•	航運公司分佈
	•	錯誤輸入次數

⸻

🚫 不包含的功能（MVP 排除）
	•	Booking Number 支援
	•	後台管理系統
	•	使用者帳號/登入功能
	•	批次查詢（CSV/Excel 上傳）
	•	API 查詢或整合
	•	CAPTCHA、濫用防範
	•	SEO 優化

⸻

✅ 未來功能計劃（可擴充）
	•	批量查詢功能（CSV 上傳）
	•	API 接入第三方物流系統
	•	替航運公司網址提供 CMS 管理
	•	多語言支援
	•	提供查詢歷史紀錄
	•	支援訂艙號 Booking No. 查詢
