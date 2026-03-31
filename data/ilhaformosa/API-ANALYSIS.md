# 臺灣史新手村 CMS API 逆向分析報告

> 分析日期：2026-03-31  
> 目標：https://ilhaformosa.nmth.gov.tw/home/zh-tw  
> CMS 基底：https://themedata.culture.tw  
> 版權：© 國立臺灣歷史博物館 National Museum of Taiwan History

---

## 1. 背景

臺灣史新手村是 Angular 5.2.0 SPA（Single Page Application），部署於 `ilhaformosa.nmth.gov.tw`，底層 CMS 是文化部統一主題網站平台 `themedata.culture.tw`（Cloudflare 代理）。

---

## 2. 發現的認證資訊

### 2.1 hardcoded in main.js bundle

| 參數           | 值                                     |
| -------------- | -------------------------------------- |
| `apiHost`      | `https://themedata.culture.tw`         |
| `common_token` | `8CC1C549-35D7-4691-9E1D-67D8EC7951B5` |
| `projectCode`  | `busker`                               |
| `pamApiHost`   | `https://publicartap.moc.gov.tw/data`  |
| `bochUrl`      | `https://nchdb.boch.gov.tw`            |

### 2.2 siteToken 列表（從 `/api/site/config` 取得）

| 語言    | siteToken                              | 是否預設 |
| ------- | -------------------------------------- | -------- |
| `zh-tw` | `40436d63-e191-46e1-855e-1f8dea5a5eb7` | ✅ 是    |
| `en-us` | `29cbb58d-7a55-4ace-a657-2d21c28e6d63` | 否       |
| `ja-jp` | `7acd3fdf-61fb-4678-8b49-fb2abf0a7c57` | 否       |
| `es-es` | `844f9b69-23a6-41bc-ba03-a16802fc5674` | 否       |
| `fr-fr` | `91a2d5be-d8d0-4330-918d-8adaec513f9f` | 否       |

---

## 3. 認證機制

### 3.1 關鍵發現：Referer 驗證

CMS API 使用 **Cloudflare WAF + Referer 驗證**，而非 token header。

- ❌ 無 Referer → HTTP 500「系統異常」
- ❌ siteToken 作為 query param → HTTP 402（WAF 攔截）
- ❌ curl User-Agent → HTTP 402（WAF TLS fingerprint 攔截）
- ✅ 正確的 Referer header → HTTP 200
- ✅ 瀏覽器（Playwright/真實 Chrome） → HTTP 200

### 3.2 正確的請求格式

```
GET https://themedata.culture.tw/api/cms/{path}
Referer: https://ilhaformosa.nmth.gov.tw/
Content-Type: application/json
```

**關鍵**：Cloudflare WAF 需要真實瀏覽器的 TLS fingerprint，curl 被封鎖，需使用 Playwright 或真實瀏覽器。

### 3.3 siteToken 使用方式

從 JS bundle 分析，siteToken 是從 `/api/site/config` 動態取得後存在記憶體中，**不需在 API 請求 header 中傳遞**——WAF 已透過 Referer domain 識別請求來源。

---

## 4. 已確認可用的 API Endpoints

### 4.1 站台設定類（不需 auth，只需正確 Referer）

| Endpoint                      | 說明           | 回傳格式 |
| ----------------------------- | -------------- | -------- |
| `GET /api/site/config`        | siteToken 列表 | Array    |
| `GET /api/site/menu`          | 導覽選單結構   | Array    |
| `GET /api/site/sitemap`       | 網站地圖       | Array    |
| `GET /api/site/header`        | 網站標題/LOGO  | Object   |
| `GET /api/site/footer`        | 頁尾資訊       | Object   |
| `GET /api/site/structure`     | 版型設定       | Object   |
| `GET /api/site/metadata`      | SEO metadata   | Object   |
| `GET /api/site/banner`        | 首頁橫幅       | Object   |
| `GET /api/site/bannerMobile`  | 手機橫幅       | Object   |
| `GET /api/site/hit`           | 總瀏覽次數     | Number   |
| `GET /api/site/static/module` | 靜態模組       | Object   |
| `GET /api/siteSeries`         | 系列資料       | Array    |
| `GET /api/option/news`        | 新聞分類選項   | Array    |

### 4.2 內容類（核心）

| Endpoint                          | 說明         | 回傳欄位                                                                                                                                      |
| --------------------------------- | ------------ | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `GET /api/cms/{path}`             | 頁面完整內容 | `id`, `title`, `description`, `content` (HTML), `keywords`, `people`, `events`, `objects`, `videos`, `annals`, `digital`, `gallery`, `images` |
| `GET /api/site/module/{path}`     | 頁面模組類型 | `moduleKey`, `templateKey`                                                                                                                    |
| `GET /api/cms/menuSetting/{path}` | 頁面側欄設定 | 各欄位開關狀態                                                                                                                                |

### 4.3 Admin/CMS 後台類（需 OAuth token）

| Endpoint                      | 說明                                |
| ----------------------------- | ----------------------------------- |
| `POST /backend/oauth/token`   | 登入取得 access_token               |
| `POST /backend/oauth/reflash` | Token 刷新                          |
| `POST /backend/oauth/del`     | 登出                                |
| `GET/POST /api/{generic}`     | 通用 CRUD（需 access_token header） |

---

## 5. 內容路徑結構

網站路由格式：`/home/zh-tw/{path}`  
CMS API 格式：`GET /api/cms/{path}`

### 完整路徑清單

| Path   | 標題                                     |
| ------ | ---------------------------------------- |
| `00-1` | 前言 臺灣的特色                          |
| `00-2` | 網站說明                                 |
| `01-0` | 原生之島（單元一總覽）                   |
| `01-1` | 1-1 臺灣島嶼最早的住民                   |
| `01-2` | 1-2 臺灣玉漂洋過海                       |
| `01-3` | 1-3 千年來的各種舶來品                   |
| `01-4` | 1-4 南島：語言與神話裡的史前史           |
| `01-5` | 1-5 外來勢力來臨前原住民自主社會         |
| `02-0` | 海陸交會（單元二總覽）                   |
| `02-1` | 2-1 航道地標：浮現在海圖上的福爾摩沙     |
| `02-2` | 2-2 內海：各據一方的歷史舞台             |
| `02-3` | 2-3 異文化相遇：東亞港市的物質流通       |
| `02-4` | 2-4 東寧王國：鄭氏王朝的21年             |
| `02-5` | 2-5 臺灣小府：清帝國統治的開始           |
| `03-0` | 在地生根（單元三總覽）                   |
| `03-1` | 3-1 統治的邊界：持續變動的番界           |
| `03-2` | 3-2 追功逐名：成為仕紳家族               |
| `03-3` | 3-3 由幽入優：浮出歷史地表的女性         |
| `03-4` | 3-4 合境平安：凝聚眾生的信仰             |
| `04-0` | 世界競逐（單元四總覽）                   |
| `04-1` | 4-1 開港通商：臺灣茶走向世界             |
| `04-2` | 4-2 觀察臺灣：西方人的博物探索之旅       |
| `04-3` | 4-3 「開山撫番」政策下的族群激烈競爭     |
| `04-4` | 4-4 保衛鄉土大作戰                       |
| `04-5` | 4-5 邁向近代：近代基礎建設的美麗與哀愁   |
| `05-0` | 烽火邊緣（單元五總覽）                   |
| `05-1` | 5-1 從總督府到總統府：殖民體制到威權體制 |
| `05-2` | 5-2 民主的香火：臺灣本土政治運動的脈絡   |
| `05-3` | 5-3 都市憂鬱：大眾流行文化的本土印記     |
| `05-4` | 5-4 運用科學「改造」環境的時代           |
| `05-5` | 5-5 社會急速變動下的臺灣扶助事業         |
| `05-6` | 5-6 戰爭與臺灣人群的移動                 |
| `06-0` | 民主轉型（單元六總覽）                   |
| `06-1` | 6-1 狂飆前夕，鬆動威權的一場大審         |
| `06-2` | 6-2 經濟起飛與公民的抬頭                 |
| `06-3` | 6-3 解嚴未完成，追求百分百的言論自由     |
| `06-4` | 6-4 新臺灣人，開放的族群觀與社會互動     |
| `06-5` | 6-5 持續的挑戰，沒有人是局外人           |
| `07-0` | 參考文獻                                 |
| `08-0` | 寫作團隊                                 |

---

## 6. API 回傳資料結構（/api/cms/{path}）

```json
{
  "id": 123614,
  "title": "前言  臺灣的特色",
  "description": "摘要文字...",
  "content": "<div class=\"single_04\">...(HTML 正文)...</div>",
  "views": 2042,
  "dataProvider": null,
  "keywords": [],
  "people": [],
  "events": [],
  "objects": [],
  "videos": [],
  "annals": [],
  "digital": [],
  "gallery": [],
  "normal": [],
  "single": [],
  "images": []
}
```

---

## 7. 爬取方法

### 7.1 為何 curl 不行

Cloudflare WAF 以 TLS ClientHello fingerprint（JA3/JA4）識別 bot，curl 的 TLS fingerprint 被封鎖（HTTP 402）。

### 7.2 有效方法：Playwright

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    intercepted = {}
    def on_response(response):
        if 'themedata.culture.tw/api/cms/' in response.url:
            path = response.url.split('/api/cms/')[-1]
            intercepted[path] = response.json()

    page.on("response", on_response)
    page.goto("https://ilhaformosa.nmth.gov.tw/home/zh-tw/{path}")
    page.wait_for_load_state("networkidle")
```

### 7.3 Lazy-loaded Angular Chunks

Angular 動態載入 chunks（0-5），內容 API 在 chunk-1（19MB）。chunk 對照表（inline bundle）：

```
0: 4478990ba970d8543679
1: ad8dc77a2626f240c017
2: d190af79c7785271770f
3: 5a758d1f6de52ba540bb
4: b3cea43d4037ac107350
5: 8bfc695fd8b65037b901
```

---

## 8. 輸出結果

- **原始 JSON**：`raw/` 目錄，40 個 JSON 檔案 + `all-cms-data.json`
- **Markdown 文件**：
  - `00-intro.md`（前言、網站說明）
  - `01-indigenous-origins.md`（單元一：原生之島，6 節）
  - `02-maritime-crossroads.md`（單元二：海陸交會，6 節）
  - `03-local-roots.md`（單元三：在地生根，5 節）
  - `04-global-competition.md`（單元四：世界競逐，6 節）
  - `05-wartime-edge.md`（單元五：烽火邊緣，7 節）
  - `06-democratic-transition.md`（單元六：民主轉型，6 節）
  - `07-references.md`（參考文獻）
  - `08-writing-team.md`（寫作團隊）

**成功率：40/40 頁面（100%）**

---

## 9. 注意事項

- 本分析僅供學術研究參考
- 版權歸屬：© 國立臺灣歷史博物館 National Museum of Taiwan History
- 爬取節奏：每頁間隔 2 秒，溫和訪問
- 網站目前（2026-03-31）處於維修狀態（`/page/` 路徑重定向到 `/maintain/`），但 `/home/` 路徑仍可訪問

---

_報告產生時間：2026-03-31_
