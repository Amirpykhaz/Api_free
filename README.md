# Api_free

کتابخونه ای پر از وب سرویس های کاربردی برای راحتی کار شما

## نصب

```bash
pip install Api_free
```

## استفاده

```python
import asyncio
from Api_free import chat_gpt, speack, time

async def main():
    print(await chat_gpt("سلام GPT!"))
    print(await speack("خوش اومدی"))
    print(time())

asyncio.run(main())
```