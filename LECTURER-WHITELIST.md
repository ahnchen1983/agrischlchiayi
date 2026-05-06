# 公開講師白名單（LECTURER-WHITELIST）

> **目的**：登記同時為農友資料庫個案、又以公開身分授課的講師。
> 這些人士的「授課身分」相關內容可在 `knowledge/<類別>/` 揭露姓名，但其「農友身分」相關個人資料仍受 `DEIDENTIFICATION-POLICY.md` 完整保護。
>
> **政策依據**：`DEIDENTIFICATION-POLICY.md` §「公開講師例外」
>
> **檢查邏輯**：`scripts/tools/deidentification-check.py` 在偵測到敏感雜湊命中時，會先比對本檔白名單；若命中雜湊在白名單**且檔案路徑屬於該 entry 的 `paths` 前綴**內，則視為合規、不阻擋 commit。

---

## 名單格式

每筆紀錄包含：

- `hash`：姓名 SHA256-16 雜湊（不揭露真名於檔案中）
- `notes`：授課依據（活動名稱、日期、Accupass 連結等公開資料佐證）
- `added_by`：登記人
- `added_date`：登記日期
- `paths`：例外生效路徑前綴，逗號分隔（預設 `knowledge/`）

---

## 已登記名單

### Entry 001
- `hash`: `e742a2e3ffb1c442`
- `notes`: 公開授課身分（蛤董／養殖負責人），國本學堂第四屆 0514 農業場域交流會主講人；課程公告於主辦單位活動頁
- `added_by`: ahnchen
- `added_date`: 2026-04-29
- `paths`: knowledge/

### Entry 002
- `hash`: `5fefdfb82164daa5`
- `notes`: 公開授課身分（耿赫智能農場負責人），國本學堂第五屆 0903 系列研習會主講人；課程公告於主辦單位活動頁
- `added_by`: ahnchen
- `added_date`: 2026-04-29
- `paths`: knowledge/

### Entry 003
- `hash`: `ad0d8570d4800fe7`
- `notes`: 公開授課身分（奕家果園負責人），國本學堂第五屆 0903 系列研習會首場主講人；課程公告於主辦單位活動頁
- `added_by`: ahnchen
- `added_date`: 2026-04-29
- `paths`: knowledge/

### Entry 004
- `hash`: `488fc84e240bd354`
- `notes`: 公開授課身分（蟹老闆），國本學堂主軸課程主講人；課程公告於主辦單位活動頁
- `added_by`: ahnchen
- `added_date`: 2026-05-01
- `paths`: knowledge/

### Entry 005
- `hash`: `663d056daf2172b2`
- `notes`: 公開授課身分（天賜的禮物負責人），國本學堂第四屆 0507 農業場域交流會主講人；課程公告於主辦單位活動頁
- `added_by`: ahnchen
- `added_date`: 2026-05-01
- `paths`: knowledge/

### Entry 006
- `hash`: `c4029b8f4cec01c9`
- `notes`: 公開授課單位「奕家果園」（陳奕宏 Entry 003 之服務機構），國本學堂第五屆 0903 系列研習會主辦背景揭露
- `added_by`: ahnchen
- `added_date`: 2026-05-01
- `paths`: knowledge/

### Entry 007
- `hash`: `372e3628b388ac4f`
- `notes`: 公開授課單位「耿赫智能農場」（張耿赫 Entry 002 之服務機構），國本學堂第五屆 0903 系列研習會主辦背景揭露
- `added_by`: ahnchen
- `added_date`: 2026-05-01
- `paths`: knowledge/

### Entry 008
- `hash`: `a045b97f73e6e1be`
- `notes`: 公開授課身分（東昀農場負責人），國本學堂第四屆進階班農耕場主講人；課程公告於主辦單位活動頁
- `added_by`: ahnchen
- `added_date`: 2026-05-04
- `paths`: knowledge/

### Entry 009
- `hash`: `c35ed26bfa642bd0`
- `notes`: 公開授課身分（裕泰農場負責人），國本學堂第四屆卓越班 1126 參訪場域主；課程公告於主辦單位活動頁
- `added_by`: ahnchen
- `added_date`: 2026-05-04
- `paths`: knowledge/

### Entry 010
- `hash`: `482a74826ba8660e`
- `notes`: 公開授課身分（旺萊山廠長），國本學堂第四屆卓越班核心課程「現代農企業管理」主講人；課程公告於主辦單位活動頁
- `added_by`: ahnchen
- `added_date`: 2026-05-04
- `paths`: knowledge/

### Entry 011
- `hash`: `f1945d872874447d`
- `notes`: 公開授課身分（卡維蘭 Kaviiland 執行長），國本學堂第四屆專業課程「銷售翻倍大作戰」主講人；課程公告於主辦單位活動頁
- `added_by`: ahnchen
- `added_date`: 2026-05-04
- `paths`: knowledge/

### Entry 012
- `hash`: `18e39d5aea52a9bc`
- `notes`: 公開授課身分（純淨農產合作社／最正農婦創辦人），國本學堂第二、三、四屆三場主講人；課程公告於主辦單位活動頁
- `added_by`: ahnchen
- `added_date`: 2026-05-04
- `paths`: knowledge/

### Entry 013
- `hash`: `f11837a8b0c1b5f2`
- `notes`: 公開授課身分（打寶蛤執行長），國本學堂第四屆文蛤戰略班 1210 跨縣參訪場域主；課程公告於主辦單位活動頁
- `added_by`: ahnchen
- `added_date`: 2026-05-04
- `paths`: knowledge/

### Entry 014
- `hash`: `811b63a1b66fe651`
- `notes`: 公開授課身分（哈哈魚場場長），國本學堂第四屆文蛤戰略班 1210 跨縣參訪場域主；課程公告於主辦單位活動頁
- `added_by`: ahnchen
- `added_date`: 2026-05-04
- `paths`: knowledge/

### Entry 015
- `hash`: `b44cb7a8bee2bd27`
- `notes`: 公開授課身分（新農果菜生產合作社理事主席），國本學堂第四屆進階班 0619 下午場參訪場域主；課程公告於主辦單位活動頁
- `added_by`: ahnchen
- `added_date`: 2026-05-04
- `paths`: knowledge/

### Entry 016
- `hash`: `b6804d2259f98796`
- `notes`: 公開授課單位「東昀農場」（陳昆懷 Entry 008 之服務機構）
- `added_by`: ahnchen
- `added_date`: 2026-05-04
- `paths`: knowledge/

### Entry 017
- `hash`: `42e29287985d9bb7`
- `notes`: 公開授課單位「裕泰農場」（陳明輝 Entry 009 之服務機構）
- `added_by`: ahnchen
- `added_date`: 2026-05-04
- `paths`: knowledge/

### Entry 018
- `hash`: `4911aff898a372aa`
- `notes`: 公開授課單位「旺萊山」（陳俊翰 Entry 010 之服務機構）
- `added_by`: ahnchen
- `added_date`: 2026-05-04
- `paths`: knowledge/

### Entry 019
- `hash`: `6dd35305966ad86c`
- `notes`: 公開授課單位「卡維蘭」（洪睿弘 Entry 011 之服務機構）
- `added_by`: ahnchen
- `added_date`: 2026-05-04
- `paths`: knowledge/

### Entry 020
- `hash`: `e58896bc0a03753e`
- `notes`: 公開授課單位「純淨農產合作社」（陳惠琪 Entry 012 之服務機構）
- `added_by`: ahnchen
- `added_date`: 2026-05-04
- `paths`: knowledge/

### Entry 021
- `hash`: `ccae09805beeb75e`
- `notes`: 公開授課單位「打寶蛤」（楊宜樺 Entry 013 之服務機構）
- `added_by`: ahnchen
- `added_date`: 2026-05-04
- `paths`: knowledge/

### Entry 022
- `hash`: `54694b20592b29e8`
- `notes`: 公開授課單位「哈哈魚場」（陳明瞭 Entry 014 之服務機構）
- `added_by`: ahnchen
- `added_date`: 2026-05-04
- `paths`: knowledge/

### Entry 023
- `hash`: `befd6fde3b50a3bd`
- `notes`: 公開授課單位「新農果菜生產合作社」（詹勝仁 Entry 015 之服務機構）
- `added_by`: ahnchen
- `added_date`: 2026-05-04
- `paths`: knowledge/

---

## 加入新名單流程

```bash
# 1. 計算姓名雜湊
python3 -c "import hashlib; print(hashlib.sha256('姓名'.encode()).hexdigest()[:16])"

# 2. 確認公開授課依據
#    - Accupass 課程連結
#    - 主辦單位活動公告
#    - 媒體報導

# 3. 在本檔新增 Entry，填寫四個欄位

# 4. 提 PR，由 repo 維護者 review
```

---

## 移除流程

當該講師明確表示不再公開揭露其授課身分時：

1. 從本檔刪除對應 Entry（保留歷史 git log）
2. 在 `knowledge/` 內搜尋該人姓名與相關課程，下架對應內容
3. 必要時推 hotfix 重建索引

---

## 稽核

- **頻率**：每季一次
- **內容**：核對名單上每位講師於該季是否仍有公開授課活動，無則移除
- **負責人**：repo 維護者

---

## 版本歷史

| 版本 | 日期 | 變更 |
|------|------|------|
| 1.0 | 2026-04-29 | 初版，登記 3 位國本學堂第四／第五屆主講人 |
| 1.1 | 2026-05-01 | 補登記 2 位（謝雲龍／高信明），共 5 位 |
| 1.2 | 2026-05-01 | 補登記 2 個公開授課單位（奕家果園、耿赫智能農場），共 5 位 + 2 機構 |
| 1.3 | 2026-05-04 | 補登記 8 位公開講師（陳昆懷、陳明輝、陳俊翰、洪睿弘、陳惠琪、楊宜樺、陳明瞭、詹勝仁）+ 8 個對應公開授課單位，共 13 位 + 10 機構 = 23 entries |
