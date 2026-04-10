#!/usr/bin/env python3
"""
fetch-cloudflare.py — 抓 Cloudflare Analytics crawler + request 資料

用法:
    python3 scripts/tools/fetch-cloudflare.py [--days 1]

憑證來源（優先序）:
    1. ~/.config/taiwan-md/credentials/.env 裡的 CF_API_TOKEN, CF_ZONE_ID
    2. 環境變數 CF_API_TOKEN, CF_ZONE_ID

輸出:
    ~/.config/taiwan-md/cache/cloudflare-latest.json
    ~/.config/taiwan-md/cache/cloudflare-{YYYY-MM-DD}.json

這個檔案:
    - 純 Python stdlib（不需要 pip install）
    - 憑證絕對不從 repo 讀取
    - 失敗時 exit 1，錯誤訊息指向 setup guide

來源: 2026-04-11 session α 建造，為 heartbeat Beat 1 的三源感知鋪路
"""
import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime, timedelta, timezone
from pathlib import Path

CONFIG_DIR = Path.home() / ".config" / "taiwan-md"
CREDENTIALS_DIR = CONFIG_DIR / "credentials"
CACHE_DIR = CONFIG_DIR / "cache"
ENV_FILE = CREDENTIALS_DIR / ".env"
SETUP_GUIDE = "docs/pipelines/SENSE-FETCHER-SETUP.md"


def load_env():
    """Load env vars from ~/.config/taiwan-md/credentials/.env"""
    env = dict(os.environ)
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                k, _, v = line.partition("=")
                env[k.strip()] = v.strip().strip("'\"")
    return env


def fail(msg, code=1):
    print(f"❌ {msg}", file=sys.stderr)
    print(f"   Setup guide: {SETUP_GUIDE}", file=sys.stderr)
    sys.exit(code)


def cf_graphql(token, query, variables=None):
    """Send GraphQL query to Cloudflare Analytics API."""
    url = "https://api.cloudflare.com/client/v4/graphql"
    body = json.dumps({"query": query, "variables": variables or {}}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        fail(f"Cloudflare API HTTP {e.code}: {body[:300]}")
    except urllib.error.URLError as e:
        fail(f"Cloudflare API unreachable: {e.reason}")

    if data.get("errors"):
        fail(f"Cloudflare GraphQL errors: {json.dumps(data['errors'], ensure_ascii=False)[:500]}")
    return data.get("data", {})


def fetch_crawler_stats(token, zone_tag, days=1):
    """Fetch verified bot requests grouped by user agent (crawler family)."""
    end = datetime.now(timezone.utc).replace(microsecond=0)
    start = end - timedelta(days=days)
    start_iso = start.isoformat().replace("+00:00", "Z")
    end_iso = end.isoformat().replace("+00:00", "Z")

    # httpRequestsAdaptiveGroups with verified bot dimensions
    # Docs: https://developers.cloudflare.com/analytics/graphql-api/
    query = """
    query CrawlerStats($zoneTag: String!, $start: Time!, $end: Time!) {
      viewer {
        zones(filter: { zoneTag: $zoneTag }) {
          httpRequestsAdaptiveGroups(
            filter: {
              datetime_geq: $start,
              datetime_leq: $end,
              botManagementVerifiedBot: true
            },
            limit: 200,
            orderBy: [count_DESC]
          ) {
            count
            dimensions {
              clientRequestHTTPHost
              edgeResponseStatus
              clientCountryName
              botManagementVerifiedBotCategory: botManagementVerifiedBotCategory
            }
          }
          total: httpRequestsAdaptiveGroups(
            filter: {
              datetime_geq: $start,
              datetime_leq: $end
            },
            limit: 1
          ) {
            count
          }
        }
      }
    }
    """
    variables = {"zoneTag": zone_tag, "start": start_iso, "end": end_iso}
    return cf_graphql(token, query, variables), start_iso, end_iso


def fetch_traffic_by_country(token, zone_tag, days=1):
    """Fetch total requests by country (human + bot)."""
    end = datetime.now(timezone.utc).replace(microsecond=0)
    start = end - timedelta(days=days)
    query = """
    query Countries($zoneTag: String!, $start: Time!, $end: Time!) {
      viewer {
        zones(filter: { zoneTag: $zoneTag }) {
          httpRequests1dGroups(
            filter: { date_geq: $start, date_leq: $end },
            limit: 100,
            orderBy: [sum_requests_DESC]
          ) {
            sum {
              countryMap {
                clientCountryName
                requests
                threats
              }
            }
          }
        }
      }
    }
    """
    variables = {
        "zoneTag": zone_tag,
        "start": start.strftime("%Y-%m-%d"),
        "end": end.strftime("%Y-%m-%d"),
    }
    return cf_graphql(token, query, variables)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Fetch Cloudflare crawler + traffic stats")
    parser.add_argument("--days", type=int, default=1, help="How many days back to fetch")
    args = parser.parse_args()

    env = load_env()
    token = env.get("CF_API_TOKEN", "").strip()
    zone_tag = env.get("CF_ZONE_ID", "").strip()

    if not token or not zone_tag:
        fail(
            f"CF_API_TOKEN or CF_ZONE_ID not set.\n"
            f"   Expected in {ENV_FILE} or environment.\n"
            f"   See {SETUP_GUIDE} for how to create the token."
        )

    # Guard rail: refuse if env file is inside the repo
    if ENV_FILE.resolve().is_relative_to(Path.cwd().resolve()):
        fail(
            "SECURITY: credentials .env file is inside the repo! "
            "Move it to ~/.config/taiwan-md/credentials/.env"
        )

    print(f"📡 Fetching Cloudflare crawler stats ({args.days}d)...", file=sys.stderr)
    crawler_data, start_iso, end_iso = fetch_crawler_stats(token, zone_tag, args.days)

    print(f"🌍 Fetching country breakdown...", file=sys.stderr)
    country_data = fetch_traffic_by_country(token, zone_tag, args.days)

    # Aggregate crawler counts by category
    zones = crawler_data.get("viewer", {}).get("zones", [])
    if not zones:
        fail("No zone data returned — check CF_ZONE_ID")

    zone = zones[0]
    groups = zone.get("httpRequestsAdaptiveGroups", [])
    total_requests = zone.get("total", [{}])[0].get("count", 0) if zone.get("total") else 0

    by_category = {}
    by_host = {}
    for g in groups:
        dims = g.get("dimensions", {})
        cat = dims.get("botManagementVerifiedBotCategory", "Unknown") or "Unknown"
        host = dims.get("clientRequestHTTPHost", "unknown") or "unknown"
        count = g.get("count", 0)
        by_category[cat] = by_category.get(cat, 0) + count
        by_host[host] = by_host.get(host, 0) + count

    bot_total = sum(by_category.values())

    # Build output
    output = {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "period": {"start": start_iso, "end": end_iso, "days": args.days},
        "summary": {
            "total_requests": total_requests,
            "bot_requests": bot_total,
            "human_requests": max(0, total_requests - bot_total),
            "bot_ratio": round(bot_total / total_requests, 3) if total_requests else 0,
        },
        "crawlers_by_category": dict(
            sorted(by_category.items(), key=lambda x: x[1], reverse=True)
        ),
        "requests_by_host": dict(
            sorted(by_host.items(), key=lambda x: x[1], reverse=True)[:20]
        ),
        "_raw_country": country_data,
    }

    # Write to cache
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    latest_path = CACHE_DIR / "cloudflare-latest.json"
    dated_path = CACHE_DIR / f"cloudflare-{today}.json"

    latest_path.write_text(json.dumps(output, indent=2, ensure_ascii=False))
    dated_path.write_text(json.dumps(output, indent=2, ensure_ascii=False))

    print(f"✅ Cloudflare: {bot_total:,} bot / {total_requests:,} total requests", file=sys.stderr)
    print(f"   → {latest_path}", file=sys.stderr)
    print(f"   Top categories: {list(by_category.items())[:5]}", file=sys.stderr)

    # Print summary JSON to stdout for piping
    print(json.dumps({
        "source": "cloudflare",
        "period_days": args.days,
        "total_requests": total_requests,
        "bot_requests": bot_total,
        "top_crawlers": dict(list(sorted(by_category.items(), key=lambda x: x[1], reverse=True))[:8]),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
