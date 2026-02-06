import os
import requests
from datetime import datetime
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def get_btc_usd():
    api_key = os.environ.get("COIN_API_KEY")
    if not api_key:
        return "실패: COIN_API_KEY가 비어있음 (GitHub Secrets / env 주입 확인)"

    # ✅ Data API (예시) - Latest Tick
    # 문서 예시처럼 data-api.coindesk.com + latest/tick 계열 사용
    url = "https://data-api.coindesk.com/index/cc/v1/latest/tick"

    params = {
        "market": "cadli",        # 대표 시장 예시(문서/상품에 따라 ccix 등도 있음)
        "instruments": "BTC-USD", # 또는 instrument(s) 파라미터 형태는 문서에 맞춰 조정
        "api_key": api_key,       # ✅ 쿼리로 키 붙이기(가장 확실)
    }

    headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (GitHubActions; +https://github.com/)"
    }

    r = requests.get(url, params=params, headers=headers, timeout=20)
    if r.status_code != 200:
        return f"실패: HTTP {r.status_code} - {r.text[:160]}"

    data = r.json()

    # 응답 구조는 market/상품마다 달라질 수 있어서 안전하게 접근
    # (예: Data -> BTC-USD -> VALUE 같은 형태로 오는 케이스가 있음)
    try:
        value = data["Data"]["BTC-USD"]["VALUE"]
        return f"현재 비트코인 시세: ${value}"
    except Exception:
        return f"성공은 했는데 파싱 실패: {str(data)[:200]}"

def update_readme():
    price_info = get_btc_usd()
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    content = f"""# 🚀 Crypto Auto Tracker (CoinDesk Data API)

### 💰 BTC-USD
> **{price_info}**

⏳ 마지막 갱신: {now} (UTC)
"""
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    update_readme()
