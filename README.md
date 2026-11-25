# 英聯物業管理 ULINK Property Services：網站重新設計概念

UX CIRCLES 為英聯物業管理（利物浦）製作的**非官方**重新設計概念網站。內容取自英聯現有網站
（https://www.ulinkproperty.co.uk），網站已設 `noindex`，不會出現在搜尋結果。

- 網址：https://uxcircles.github.io/ulinkproperty/（中文）、/en/（English）
- 頁面：主頁（收費計算機）、服務及收費、Airbnb 管家、團隊、聯絡、私隱政策、404

## 如何修改

所有頁面由 `_build/pages.py` 產生，每句文字寫成 `L(英文, 中文)`。

```bash
python3 _build/pages.py && python3 _build/fonts.py   # 改中文字後要重跑 fonts.py（字型子集）
```

修改 CSS / JS 後，請將 `pages.py` 內的 `V` 加一（cache-bust）。

## 設計概念

- **招牌元素：香港街市「價錢牌」**。英聯的宗旨係「誠實、透明」、「如實報價，不會誇大和濫收費用」，
  而且現有網站已公開所有收費。所以每項收費都寫在一張打咗窿、掛喺繩上的價錢牌上：主頁計算機的結果、
  服務頁、網站圖示（favicon）、地圖標記、404 頁「賣晒」。
- **首屏類型：`tool-first`**。輸入月租、每晚租金或樓價，價錢牌即時顯示英聯收幾多、業主袋幾多
  （英鎊及港幣，匯率可自行修改）。
- **字型**：Big Shoulders Display（價錢及英文標題，似街市招牌）、霞鶩文楷 TC（中文標題，似麥克筆手寫價錢牌）、
  Atkinson Hyperlegible + Noto Sans TC（內文，易讀）。
- **顏色**：價錢牌紅 #c8102e、街市檔口綠 #0e5a45、白底。
- **與上兩個物業網站的分別**：UKPM、Withyou、JoyHome 都是左文右拱形相片；今次無拱形、無浮動標籤，
  首屏是可以用的工具，配色由海軍藍／紅磚改為街市紅綠。
- **主頁字數**：中文約 560 字、英文約 390 字；相片 9 張。

## 收費（全部來自現有網站 /service 及 /why-choose-us）

| 服務 | 收費 | 計算機算法 |
| --- | --- | --- |
| 代客睇樓報告 | HK$450，睇完先付 | 固定 |
| 物業購買一條龍 | 樓價 1%，成交後付 | 樓價 × 1% |
| 搵租客 | 一個月租金 | 月租 × 1 |
| 全方位管理 | 租金 12% | 月租 × 12%；第一年你袋 = 12 × 月租 − 搵租客 − 12 × 管理費 |
| Airbnb 管家 | 訂房收入 15% + VAT，另加清潔費 | 每晚 × 晚數 × 15% × 1.2（VAT 20%），未計清潔費 |

## 需要英聯確認

1. **電話／WhatsApp**：現有網站完全沒有電話號碼，概念網站只用電郵及 Facebook Messenger。如提供號碼，手機底部按鈕會改為「致電／WhatsApp」。
2. 12% 管理費是否另加 VAT（現網站未列明）。
3. 計算機預設匯率 £1 = HK$10.4 只作示範。
4. 住客評價的署名：現網站兩段評價下方依次寫「Michael, from FL, USA」「Jodie, From France」，本網站按此順序配對。
5. 私隱政策為草稿（現網站沒有），需英聯審閱。
6. 地圖位置用郵區 L5 6PU 的中心點（OpenStreetMap），請確認 299 Breck Road 位置。

## 圖片來源

| 檔案 | 來源 | 授權 | 英聯自己的？ |
| --- | --- | --- | --- |
| house.webp | 英聯網站主頁「代客親身睇樓」 | 英聯 | 是 |
| airbnb-room.webp | 英聯網站主頁頭圖 | 英聯 | 是（可能為圖庫，待確認） |
| superhost.webp | 英聯網站主頁 | Airbnb 標誌 | 是 |
| hallway.webp | 英聯網站主頁（Wix 圖庫） | Wix | 否 |
| anfield-street.webp | https://www.pexels.com/photo/trent-alexander-arnold-on-mural-in-town-24429494/ | Pexels | 否 |
| liver-building.webp | https://www.pexels.com/photo/the-clocks-of-the-royal-liver-building-in-liverpool-england-11843019/ | Pexels | 否 |
| terrace.webp | https://www.pexels.com/photo/photo-of-vehicles-on-road-near-houses-2611873/ | Pexels | 否 |
| hong-kong.webp | https://www.pexels.com/photo/evening-cityscape-of-hong-kong-downtown-and-harbor-18093482/ | Pexels | 否 |
| anfield-gates.webp | https://www.pexels.com/photo/gateway-entrance-to-anfield-stadium-in-liverpool-10463654/ | Pexels | 否 |
| keys.webp | https://www.pexels.com/photo/handing-the-keys-of-a-new-house-7641904/ | Pexels | 否 |
| pier-head.webp | https://www.pexels.com/photo/gray-structure-near-body-of-water-2536478/ | Pexels | 否 |

地圖：MapLibre GL JS（BSD）＋ OpenFreeMap / OpenStreetMap。

---
非官方概念設計：[UX CIRCLES](https://ux-circles.com/professionals)
