مستندات کتابخانه api-free.ir
این کتابخانه برای تعامل با API های موجود در سایت api-free.ir طراحی شده است. این کتابخانه شامل توابعی برای ارسال ایمیل، آپلود فایل، جستجوی موسیقی، ایجاد صدا، ایجاد تصویر، دانلود پست و استوری از روبیکا، جستجوی صفحات روبینو و اینستاگرام، دریافت اطلاعات IP و جستجوی ویکی‌پدیا می‌باشد.

نصب
برای استفاده از این کتابخانه، ابتدا باید آن را نصب کنید:

bash
Copy code
pip install requests urllib3
کلاس client
این کلاس برای مدیریت ارتباط با سرویس‌های مختلف استفاده می‌شود. برای استفاده از این کلاس، باید یک توکن احراز هویت به آن بدهید.

نمونه کد استفاده
آپلود فایل
python
Copy code
from codern import client

client_instance = client(token="your_token")
upload_result = client_instance.Upload_file("path/to/your/file.txt")
print(upload_result)
ورودی‌ها
Path: مسیر فایل
خروجی
نتیجه آپلود فایل
کلاس api
این کلاس شامل متدهای مختلفی برای تعامل با API های سایت api-free.ir می‌باشد.

نمونه کد استفاده
جستجوی موسیقی
python
Copy code
from codern import api

music_results = api.search_music(text="نام موسیقی")
print(music_results)
ورودی‌ها
text: متن جستجو
result_count: تعداد نتایج (پیش‌فرض: 5)
خروجی
لیستی از لینک‌های موسیقی و عنوان‌ها
ایجاد صدا
python
Copy code
from codern import api

voice_result = api.create_voice(text="متن مورد نظر برای تبدیل به صدا")
print(voice_result)
ورودی‌ها
text: متن مورد نظر برای تبدیل به صدا
mod: مدل صدای مورد نظر (مقادیر مجاز: 'FaridNeural', 'DilaraNeural')
خروجی
لینک فایل صوتی ایجاد شده
ایجاد تصویر
python
Copy code
from codern import api

image_result = api.create_image(text="توضیحات تصویر")
print(image_result)
ورودی‌ها
text: توضیحات تصویر
version: نسخه مدل تولید تصویر (مقادیر مجاز: '3.5', '2.5', '1.5', '4')
choice: انتخاب تصادفی یک تصویر (پیش‌فرض: False)
خروجی
لینک یا لیست لینک‌های تصاویر ایجاد شده
دانلود پست روبیکا
python
Copy code
from codern import api

post_result = api.download_post_rubika(share_url="لینک پست روبیکا")
print(post_result)
ورودی‌ها
share_url: لینک پست روبیکا
خروجی
لینک یا لیست لینک‌های دانلود پست
دانلود استوری روبیکا
python
Copy code
from codern import api

story_result = api.download_story_rubika(username="نام کاربری")
print(story_result)
ورودی‌ها
username: نام کاربری
خروجی
لینک یا لیست لینک‌های دانلود استوری
جستجوی صفحه روبینو
python
Copy code
from codern import api

page_result = api.search_page_rubino(text="نام کاربری یا متن جستجو")
print(page_result)
ورودی‌ها
text: نام کاربری یا متن جستجو
خروجی
اطلاعات صفحه
دریافت IP خود
python
Copy code
from codern import api

ip_result = api.get_ip_me()
print(ip_result)
ورودی‌ها
ندارد
خروجی
آدرس IP شما
دریافت اطلاعات IP
python
Copy code
from codern import api

ip_info_result = api.get_info_ip(ip="آدرس IP")
print(ip_info_result)
ورودی‌ها
ip: آدرس IP
خروجی
اطلاعات مربوط به IP
دریافت اطلاعات صفحه اینستاگرام
python
Copy code
from codern import api

instagram_page_result = api.get_page_instagram(username="نام کاربری اینستاگرام")
print(instagram_page_result)
ورودی‌ها
username: نام کاربری اینستاگرام
خروجی
اطلاعات صفحه اینستاگرام
جستجوی ویکی‌پدیا
python
Copy code
from codern import api

wikipedia_result = api.search_wikipedia(text="متن جستجو", lang="fa")
print(wikipedia_result)
ورودی‌ها
text: متن جستجو
lang: زبان (پیش‌فرض: "fa")
خروجی
نتایج جستجو در ویکی‌پدیا
چت با GPT
python
Copy code
from codern import api

chat_result = api.Ai_chat_GPT(text="سوال شما")
print(chat_result)
ورودی‌ها
text: متن سوال
خروجی
پاسخ چت GPT
چت با Bard
python
Copy code
from codern import api

bard_result = api.Ai_bard_Chat(text="سوال شما", put_lang="fa")
print(bard_result)
ورودی‌ها
text: متن سوال
put_lang: زبان خروجی (مقادیر مجاز: 'fa', 'en')
خروجی
پاسخ چت Bard به زبان مورد نظر
جعبه سیاه (Black Box)
python
Copy code
from codern import api

black_box_result = api.Ai_black_box(text="متن ورودی")
print(black_box_result)
ورودی‌ها
text: متن ورودی
is_replace: رشته‌ای که باید در متن جایگزین شود (اختیاری)
خروجی
نتیجه پردازش جعبه سیاه