# OSごとに安全に動くインポート
try:
    import certifi_win32  # Windowsの証明書ストアをrequestsに反映（Windows以外では無視される）
except Exception:
    pass

import os
import requests
from datetime import datetime
from zoneinfo import ZoneInfo

# certifi は存在すれば使う（Linux/MacではなくてもOK）
try:
    import certifi
    CERT_VERIFY = certifi.where()
except Exception:
    CERT_VERIFY = True  # デフォルト検証に任せる（UbuntuランナーはこれでOK）

API_KEY = os.getenv("OPENWEATHER_API_KEY")
if not API_KEY:
    raise RuntimeError("OPENWEATHER_API_KEY が設定されていません。")

city = os.getenv("CITY", "Tokyo,jp")

url = (
    "https://api.openweathermap.org/data/2.5/weather"
    f"?q={city}&units=metric&lang=ja&appid={API_KEY}"
)

# ここで verify=CERT_VERIFY を使う（UbuntuならTrue、Windowsローカルならcertifiのパス）
resp = requests.get(url, timeout=15, verify=CERT_VERIFY)
resp.raise_for_status()
weather = resp.json()

if not isinstance(weather, dict) or "weather" not in weather or "main" not in weather:
    raise RuntimeError(f"返り値が想定外: {weather}")

description = weather["weather"][0]["description"]
temp_max = weather["main"]["temp_max"]
temp_min = weather["main"]["temp_min"]
city_name = weather.get("name", city)

# --- 簡易ロジック（任意で②のランダム差し替え可） ---
if "雨" in description:
    comment = "雨模様。移動は少し余裕を持つと安心です。"
elif temp_max is not None and temp_max >= 30:
    comment = "暑くなりそう。無理せずペース配分を意識しましょう。"
elif temp_min is not None and temp_min <= 5:
    comment = "冷え込みます。防寒を意識して体調ファーストで。"
else:
    comment = "天候は穏やか。計画通りにじっくり進めるチャンスです。"

print(f"☀ 今日の天気（{city_name}）")
print(f"天気：{description}")
print(f"最高気温：{temp_max}℃")
print(f"最低気温：{temp_min}℃")
print()
print("🧠 判断コメント")
print(comment)
print()

print(f"実行時刻（JST）：{datetime.now(ZoneInfo('Asia/Tokyo')).isoformat(timespec='seconds')}")
