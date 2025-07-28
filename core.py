import datetime
import urllib.parse
import httpx
import json
from persiantools.jdatetime import JalaliDate
from asyncio import run

all_func = [
    "chat_gpt", "speack", "time", "date_fa", "joke", "translate",
    "weather", "music_8d", "ip", "dan", "video", "birth_info", "send_email", "dastan", "get_en_fonts", "get_fa_fonts", "get_anime_image", "get_music"
]
version = '0.1.0'

# ---------- تابع کمکی برای GET ---------- #
async def fetch_json(url: str, params: dict = None, timeout: int = 10):
    try:
        async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            try:
                return response.json()
            except json.JSONDecodeError:
                return {"error": f"❌ پاسخ JSON معتبر نیست:\n{response.text}"}
    except httpx.RequestError as e:
        return {"error": f"❌ خطا در اتصال: {e}"}
    except httpx.HTTPStatusError as e:
        return {"error": f"❌ وضعیت HTTP نامعتبر: {e.response.status_code}"}

async def fetch_text(url: str, params: dict = None, timeout: int = 10):
    try:
        async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.text
    except httpx.RequestError as e:
        return f"❌ خطا در اتصال: {e}"
    except httpx.HTTPStatusError as e:
        return f"❌ وضعیت HTTP نامعتبر: {e.response.status_code}"

# ---------- توابع اصلی ---------- #
async def get_update():
	data = await fetch_text('https://amirpython.pythonanywhere.com/Version')
	if data != version:
		print('⚠️ Update Found\nTo update the command pip install --upgrade Api_free')
	
async def chat_gpt(text: str, user_id: str = '1234') -> str:
    if not text.strip():
        return "❌ متن نمی‌تواند خالی باشد."
    url = "http://api.cactus-dev.ir/gpt-4o-mini.php"
    data = await fetch_json(url, {"prompt": text, "userid": user_id})
    return data.get('response', data.get("error", "❌ پاسخی دریافت نشد."))
    
async def voice(text: str) -> str:
    if not text.strip():
        return "❌ متن نمی‌تواند خالی باشد."
    url = "https://api.cactus-dev.ir/voice"
    data = await fetch_json(url, {"text": text})
    return data.get('result', data.get("error", "❌ پاسخی دریافت نشد."))
    
async def video() -> str:
	url = 'http://api-free.ir/api/video'
	data = await fetch_json(url)
	return data.get('result','خطایی رخ داد ❌')

async def speack(text: str, token: str = 'e5bf7aec056a43f5d79cbaedd03cee87') -> str:
    if not text.strip():
        return "❌ متن نمی‌تواند خالی باشد."
    url = "http://v3.api-free.ir/speaker/"
    data = await fetch_json(url, {"text": text, "token": token})
    return data.get('step', {}).get('answer', data.get("error", "❌ پاسخ نامشخص"))

def time() -> str:
    return datetime.datetime.now().strftime("%H:%M:%S")

def date_fa() -> str:
    return JalaliDate.today().strftime("%Y/%m/%d")

async def jok() -> str:
    url = "https://api-free.ir/api/jok.php"
    data = await fetch_json(url)
    return data.get("result", data.get("error", "❌ جوکی یافت نشد."))
    
async def dialog() -> str:
    url = "https://api-free.ir/api2/dialog"
    data = await fetch_json(url)
    return data.get("result", data.get("error", "❌ دیالوگی یافت نشد."))

async def ip() -> str:
    url = "https://api-free.ir/api/ip.php"
    data = await fetch_json(url)
    return data.get("ip", data.get("error", "❌ آی‌پی یافت نشد."))

async def dan() -> str:
    url = "https://api-free.ir/api/danes.php"
    return await fetch_text(url)

async def translate(text: str, to_lang: str = "en") -> str:
    if not text.strip():
        return "❌ لطفاً متنی برای ترجمه وارد کنید."
    url = "http://api.codebazan.ir/translate/"
    return await fetch_text(url, {"to": to_lang, "text": text})

async def weather(city: str) -> str:
    if not city.strip():
        return "❌ لطفاً نام شهر را وارد کنید."
    url = "http://api.codebazan.ir/weather/index.php"
    return await fetch_text(url, {"city": city})

async def music_8d(url: str) -> str:
    if not url.strip():
        return "❌ لینک فایل موزیک نمی‌تواند خالی باشد."
    api = "https://v3.api-free.ir/8D"
    data = await fetch_json(api, {"url": url})
    return data.get("result", data.get("error", "❌ مشکلی در دریافت خروجی رخ داد."))
    
async def birth_info(year: int, month: int, day: int) -> dict:
    if not (1300 <= year <= 2500):
        return {"error": "❌ سال وارد شده معتبر نیست."}
    if not (1 <= month <= 12):
        return {"error": "❌ ماه وارد شده معتبر نیست."}
    if not (1 <= day <= 31):
        return {"error": "❌ روز وارد شده معتبر نیست."}

    url = "http://v3.api-free.ir/birth2"
    params = {"year": year, "month": month, "day": day}

    data = await fetch_json(url, params)

    if not isinstance(data, dict):
        return {"error": "❌ پاسخ دریافتی نامعتبر است."}
    
    if not data.get("ok"):
        return {"error": f"❌ خطا از سمت API: {data.get('message', 'نامشخص')}"}

    result = data.get("result")
    if not result:
        return {"error": "❌ داده‌ای در پاسخ یافت نشد."}

    return result
    
async def send_email(to: str, subject: str, body: str, title: str = "Api_free") -> str:
    if not to or not subject or not body:
        return "❌ پارامترهای الزامی (to, subject, body) باید وارد شوند."
    
    url = "https://v3.api-free.ir/email/"
    params = {
        "to": to,
        "subject": subject,
        "body": body,
        "title": title
    }

    data = await fetch_json(url, params)
    
    if isinstance(data, dict) and data.get("code") == 200:
        return True
    
    return f"❌ خطا در ارسال ایمیل: {data.get('text', data.get('error', 'پاسخ نامشخص'))}"
    
async def dastan() -> str:
    url = "https://api-free.ir/api2/dastan"
    data = await fetch_json(url)
    return data.get('result','داستانی یافت نشد ❌')
    
async def get_fa_fonts(text: str) -> list:
    if not text.strip():
        return ["❌ لطفاً متنی برای تبدیل به فونت وارد کنید."]
    
    url = "https://api-free.ir/api/font.php"
    params = {"fa": text}
    data = await fetch_json(url, params)
    
    if not isinstance(data, dict) or not data.get("ok"):
        return [f"❌ خطا در دریافت فونت‌ها: {data.get('error', 'پاسخ نامعتبر')}"]

    fonts = data.get("result")
    if not fonts:
        return ["❌ فونتی در پاسخ یافت نشد."]
    
    return fonts

async def get_en_fonts(text: str) -> list:
    if not text.strip():
        return ["❌ Please enter a valid text to convert."]
    
    url = "https://api-free.ir/api/font.php"
    params = {"en": text}
    data = await fetch_json(url, params)

    if not isinstance(data, dict) or not data.get("ok"):
        return [f"❌ Error getting fonts: {data.get('error', 'Invalid response.')}"]

    fonts = data.get("result")
    if not fonts:
        return ["❌ No fonts found in the response."]
    
    return fonts

async def get_anime_image(token: str = "e5bf7aec056a43f5d79cbaedd03cee87") -> str:
    url = "https://api-free.ir/api2/enime.php"
    params = {"token": token}
    data = await fetch_json(url, params)

    if not isinstance(data, dict):
        return "❌ پاسخ معتبر دریافت نشد."

    if not data.get("ok"):
        return f"❌ خطا در دریافت تصویر: {data.get('error', 'نامشخص')}"

    return data.get("result", "❌ تصویری یافت نشد.")

async def get_music() -> dict:
    url = "https://api-free.ir/api/music"
    data = await fetch_json(url)

    if not isinstance(data, dict):
        return {"error": "❌ پاسخ معتبر دریافت نشد."}

    if not data.get("ok"):
        return {"error": f"❌ خطا در دریافت موزیک: {data.get('error', 'پاسخ نامعتبر')}"}

    result = data.get("result")
    if not result:
        return {"error": "❌ اطلاعات موزیک در پاسخ یافت نشد."}

    return {
        "title": result.get("title", "❌ عنوانی یافت نشد."),
        "song": result.get("song", "❌ لینک آهنگ یافت نشد.")
    }
	
if __name__ == '__main__':
	run(get_update())