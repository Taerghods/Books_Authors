#app_book_author/Dockerfile.py
# استفاده از نسخه سبک پایتون
FROM python:3.11-slim

# تعیین پوشه کاری در کانتینر
WORKDIR /app

# کپی کردن پیش‌نیازها و نصب آن‌ها
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# کپی کردن تمام کدها به کانتینر
COPY . .

# باز کردن پورت ۸۰۰۰
EXPOSE 8000

# دستور اجرای برنامه
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]