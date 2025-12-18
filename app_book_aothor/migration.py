# app_book_author/migration.py
from sqlalchemy import text
from app_book_author.dbs import engine


async def create_materialized_view():   # به‌روزرسانی بدون توقف
    view_sql = """
    CREATE MATERIALIZED VIEW IF NOT EXISTS author_book_counts AS
    SELECT 
        a.id AS author_id,
        a.name AS author_name,
        COUNT(b.id) AS book_count
    FROM authors a
    LEFT JOIN books b ON a.id = b.author_id
    GROUP BY a.id, a.name;
    """

    index_sql = "CREATE UNIQUE INDEX IF NOT EXISTS idx_author_id_view ON author_book_counts(author_id);"

    async with engine.begin() as conn:
        await conn.execute(text(view_sql))
        await conn.execute(text(index_sql))
    print("Materialized View created successfully!")


# 1- CREATE MATERIALIZED VIEW: برخلاف View معمولی که فقط یک «فرمول» است
# ، این دستور یک «جدول واقعی» روی دیسک می‌سازد.
# یعنی دیتابیس یک بار Join و Count را انجام می‌دهد و نتیجه را ذخیره می‌کند.
# وقتی کاربر آمار را می‌خواهد، دیتابیس محاسبه نمی‌کند، فقط عدد ذخیره شده را می‌خواند

# -----------------------------------------------------------------------------------

# 2- CREATE UNIQUE INDEX: این مهم‌ترین بخش برای «به‌روزرسانی بدون توقف» است.
# چرا؟ در PostgreSQL،
# اگر بخواهی ویو را آپدیت کنی (Refresh)، جدول قفل می‌شود.
# اما اگر این ایندکس یکتا (Unique Index) وجود داشته باشد،
# می‌توانی از دستور CONCURRENTLY استفاده کنی.
# این یعنی دیتابیس در حالی که دارد نسخه جدید را می‌سازد
# ، نسخه قدیمی را هم به کاربران نشان می‌دهد و هیچ‌کس منتظر نمی‌ماند.