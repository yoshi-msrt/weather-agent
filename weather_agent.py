import certifi_win32
import os
import requests
import certifi
from datetime import datetime

API_KEY = os.getenv("OPENWEATHER_API_KEY")
if not API_KEY:
    raise RuntimeError("OPENWEATHER_API_KEY が設定されていません。")

city = "Tokyo,jp"
url = (
    "https://api.openweathermap.org/data/2.5/weather"
    f"?q={city}&units=metric&lang=ja&appid={API_KEY}"
)

resp = requests.get(url, timeout=15, verify=certifi.where())
print("DEBUG: status code =", resp.status_code)
print("DEBUG: raw text =", resp.text[:300])

resp.raise_for_status()
weather = resp.json()

if not isinstance(weather, dict) or "weather" not in weather or "main" not in weather:
    raise RuntimeError(f"返り値が想定外。APIキー/URLを確認してください。返り値: {weather}")

description = weather["weather"][0]["description"]
temp_max = weather["main"]["temp_max"]
temp_min = weather["main"]["temp_min"]

if "雨" in description:
    comment = "雨のため、移動や外出は少し余裕を持つと安心です。"
elif temp_max is not None and temp_max >= 30:
    comment = "暑くなりそうなので、無理せずペース配分を意識すると良さそうです。"
elif temp_min is not None and temp_min <= 5:
    comment = "冷え込みそうなので、防寒を意識した一日にしましょう。"
else:
    comment = "比較的穏やかな天気で、落ち着いて作業できそうです。"

print()
print("☀ 今日の天気（東京）")
print(f"天気：{description}")
print(f"最高気温：{temp_max}℃")
print(f"最低気温：{temp_min}℃")
print()
print("🧠 判断コメント")
print(comment)
print()
print(f"実行時刻：{datetime.now().isoformat(timespec='seconds')}")