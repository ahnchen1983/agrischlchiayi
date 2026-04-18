#!/usr/bin/env python3
"""
register-ga4-custom-dimensions.py — 一次註冊 7 個 search event custom dimensions

背景：
  2026-04-13 γ session 上線 search_query / search_result_click 事件追蹤，但事件參數
  在 GA4 必須註冊為 custom dimension 後才能在 Explore/API 中查詢。
  2026-04-18 δ session 嘗試跑 fetch-search-events.py 失敗：
    Field customEvent:search_term is not a valid dimension.

  → 用 GA4 Admin API 一鍵註冊 7 個 event-scope custom dimensions。

需要的權限：
  服務帳號 taiwan-md-reader@taiwan-md-sense.iam.gserviceaccount.com
  必須在 GA4 property 528789281 具備 **Editor** 角色（原先可能只是 Viewer）。
  若跑出 PermissionDenied → 到 GA4 Admin → Account/Property access management 升級角色。

資料保留：
  註冊後只有「之後的」事件會帶這些維度。歷史事件參數無法回補。

用法:
    python3 scripts/tools/register-ga4-custom-dimensions.py [--dry-run]
"""
import argparse
import os
import sys
from pathlib import Path

CONFIG_DIR = Path.home() / ".config" / "taiwan-md"
CREDENTIALS_DIR = CONFIG_DIR / "credentials"
VENV_DIR = CONFIG_DIR / "venv"

if VENV_DIR.exists() and sys.prefix != str(VENV_DIR):
    venv_python = VENV_DIR / "bin" / "python3"
    if venv_python.exists() and __name__ == "__main__":
        os.execv(str(venv_python), [str(venv_python), __file__, *sys.argv[1:]])


DIMENSIONS = [
    ("search_term", "Search Term", "讀者在站內搜尋的 query 字串"),
    ("results_count", "Search Results Count", "該次搜尋回傳的結果筆數"),
    ("search_lang", "Search Language", "搜尋發生的語言介面 zh/en/ja/ko"),
    ("search_mode", "Search Mode", "搜尋模式 instant / submit / etc"),
    ("click_title", "Clicked Result Title", "從搜尋結果點擊的文章標題"),
    ("click_url", "Clicked Result URL", "從搜尋結果點擊的文章 URL"),
    ("click_position", "Clicked Result Position", "點擊結果在列表中的位置（1-based）"),
]


def fail(msg):
    print(f"❌ {msg}", file=sys.stderr)
    sys.exit(1)


def load_property_id():
    env_path = CREDENTIALS_DIR / ".env"
    for line in env_path.read_text().splitlines():
        if line.startswith("GA4_PROPERTY_ID="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    fail("GA4_PROPERTY_ID not found")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    from google.analytics.admin_v1beta import AnalyticsAdminServiceClient
    from google.analytics.admin_v1beta.types import CustomDimension
    from google.oauth2 import service_account
    from google.api_core.exceptions import AlreadyExists, PermissionDenied

    sa_path = CREDENTIALS_DIR / "google-service-account.json"
    creds = service_account.Credentials.from_service_account_file(
        str(sa_path),
        scopes=["https://www.googleapis.com/auth/analytics.edit"],
    )
    client = AnalyticsAdminServiceClient(credentials=creds)
    property_id = load_property_id()
    parent = f"properties/{property_id}"

    print(f"📝 Registering {len(DIMENSIONS)} custom dimensions on {parent}")
    if args.dry_run:
        for p, name, desc in DIMENSIONS:
            print(f"  [dry-run] {p} → {name}")
        return

    # List existing to skip duplicates
    try:
        existing = {cd.parameter_name for cd in client.list_custom_dimensions(parent=parent)}
    except PermissionDenied as e:
        fail(
            f"PermissionDenied: service account缺 Editor 角色\n"
            f"→ GA4 Admin → Property access management → "
            f"taiwan-md-reader@taiwan-md-sense.iam.gserviceaccount.com 升級為 Editor\n"
            f"詳細: {e}"
        )

    created, skipped = 0, 0
    for param_name, display_name, description in DIMENSIONS:
        if param_name in existing:
            print(f"  ⏭  {param_name} already exists")
            skipped += 1
            continue
        cd = CustomDimension(
            parameter_name=param_name,
            display_name=display_name,
            description=description,
            scope=CustomDimension.DimensionScope.EVENT,
        )
        try:
            result = client.create_custom_dimension(parent=parent, custom_dimension=cd)
            print(f"  ✅ {param_name} → {result.name}")
            created += 1
        except AlreadyExists:
            print(f"  ⏭  {param_name} (AlreadyExists race)")
            skipped += 1

    print(f"\n✅ Done: {created} created, {skipped} skipped")
    print("\n⏱  資料可用時間：新事件開始帶維度，歷史無法回補。")
    print("   建議 48h 後（2026-04-20）再跑 fetch-search-events.py 驗證。")


if __name__ == "__main__":
    main()
