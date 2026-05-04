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
