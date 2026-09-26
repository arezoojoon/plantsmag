# 🔧 تعمیرات و نگهداری — PlantsMag Infrastructure
**آخرین به‌روزرسانی:** ۲ مهر ۱۴۰۵ (September 24, 2026)

---

## ✅ کارهایی که انجام شد (بر اساس ۳ استراتژی اصلی)

| # | کار | وضعیت |
|---|-----|--------|
| 1 | راه‌اندازی **Native Technical Meta Engine** برای بهینه‌سازی SEO | ✅ |
| 2 | پیاده‌سازی **Mega-Content Hydration Script** (تولید محتوای +2500 کلمه) | ✅ |
| 3 | فعال‌سازی سیستم **Auto-Wiki Interlinking** در تمامی مقالات | ✅ |
| 4 | یکپارچه‌سازی وب‌هوک‌های **Stripe** و سیستم پرداخت | ✅ |
| 5 | تنظیم و اجرای **Next.js** روی سرور VPS با PM2 (محیط Staging و Production) | ✅ |
| 6 | تنظیم متغیرهای محیطی برای مدل‌های **Gemini** (Vision & Text) | ✅ |
| 7 | کانفیگ سیستم کشینگ **LiteSpeed** در سمت وردپرس | ✅ |

---

## 🖥️ اطلاعات سرور

> *نکته امنیتی: آدرس‌های IP و مشخصات ورود به سرور (مانند کاربر Root) از این مستند حذف شده‌اند. برای اتصال SSH به مستندات داخلی / Password Manager مراجعه کنید.*

```yaml
Next.js VPS (Staging & Production):
  IP:   [در Password Manager موجود است]
  Production App:
    PM2:  plantsmag-nextjs
    Port: 3000
    DB:   plantsmag_prod (User: plantsmag_prod_user)
  Staging App:
    PM2:  plantsmag-nextjs-staging
    Port: 3001
    DB:   plantsmag_staging (User: plantsmag_staging_user)
  Worker:   Production و Staging Workerهای مجزا
  Database: PostgreSQL (نصب روی همین VPS ترجیحاً با Docker)
  Queue:    pg-boss

WordPress Server (Hostinger):
  WP Path: [مسیر public_html_path پروژه]
  Cache:   LiteSpeed
```

---

## 🏗️ معماری Staging و Production (قوانین حیاتی)

1. **استقلال کامل دیتابیس:** محیط Staging **به هیچ وجه** نباید به دیتابیس Production وصل شود.
2. **تست و بررسی اولیه:** اولین Prisma Migration، تست‌های Stripe Test Mode، وب‌هوک‌ها و صف‌های pg-boss ابتدا باید **فقط روی Staging** (پورت 3001 و دیتابیس `plantsmag_staging`) انجام شوند.
3. **محیط Production:** محیط اصلی سایت دست‌نخورده باقی می‌ماند تا زمانی که Staging تمام مراحل Verification را با موفقیت پاس کند.
4. **عدم نیاز به سریس خارجی:** از آنجایی که VPS دائمی است، به جای سرویس‌های خارجی (مثل Supabase)، از PostgreSQL و `pg-boss` مستقیماً روی سرور فعلی استفاده می‌شود.

---

## 📁 فایل‌های مهم روی سرور / سورس‌کد

| فایل | کارکرد |
|------|---------|
| `ecosystem.config.js` | تنظیمات PM2 برای اجرای اپلیکیشن‌های Next.js |
| `.env` مرکزی | ذخیره `GEMINI_MODEL_TEXT`، `GEMINI_MODEL_VISION` و `STRIPE_WEBHOOK_SECRET` |
| `functions.php` | فایل تنظیمات قالب وردپرس (شامل سیستم اتوماتیک ۳۰۱ برای ریدایرکت‌های ۴۰۴) |
| `style.css` | هدر این فایل حاوی ورژن قالب است (برای Cache-Busting و آپدیت استایل‌ها) |

---

## 📊 چه چیزهایی خودکار انجام می‌شوند

```
تولید محتوای جامع (Mega-Content) 
    ↓
اسکریپت Hydration فعال شده و محتوای +۲۵۰۰ کلمه می‌سازد
    ↓
ارتباط با Gemini API از طریق متغیرهای محیطی (Config-Driven)
    ↓
سیستم Auto-Wiki مقالات مرتبط را به یکدیگر Interlink می‌کند
    ↓
پرداخت‌های کاربر (Stripe) از طریق Webhook با دیتابیس همگام می‌شوند (با امنیت Idempotency)
```

---

## 🔁 نگهداری دوره‌ای

### مانیتورینگ اپلیکیشن‌های Next.js روی VPS:
سرویس‌های پرداختی و درگاه‌ها روی سرور ابری (VPS) توسط PM2 مدیریت می‌شوند.
```bash
# بررسی وضعیت اپلیکیشن‌ها
pm2 status

# مشاهده لاگ‌های زنده
pm2 logs [app_name] --lines 50

# راه‌اندازی مجدد در صورت نیاز
pm2 restart [app_name]
```

### مدیریت کش (Caching) سایت وردپرس:
در صورتی که تغییراتی در قالب دادید و در سایت اعمال نشد:
```bash
# از طریق ترمینال سرور Hostinger:
wp litespeed-purge all --path=/public_html_path
```
**آپدیت استایل‌ها:** اگر CSS شکسته است، نسخه `Version` را در هدر فایل `style.css` یک عدد بالا ببرید (مثلاً از `3.0.1` به `3.0.2`) تا مکانیزم Cache-Busting فعال شود.

---

## 🛠️ رفع خطاهای رایج

### خطا: خطای 404 یا Deprecated شدن مدل‌های Gemini
**هشدار:** هرگز نام مدل‌های گوگل (مانند `gemini-3.1-flash-image` یا `gemini-2.5-flash`) را به صورت سخت‌افزاری (Hard-code) در داخل فایل‌های کد تغییر ندهید یا جستجو نکنید.
1. به داکیومنت‌های رسمی Google API مراجعه کرده و مدل جایگزین را پیدا کنید.
2. مدل‌های مورد استفاده باید از طریق یک فایل کانفیگ مرکزی (Central Config) یا متغیرهای محیطی (`.env`) خوانده شوند (مثلاً `GEMINI_MODEL_TEXT` و `GEMINI_MODEL_VISION`).
3. مقدار را در فایل `.env` سرور تغییر داده و اپلیکیشن را با `pm2 restart [app_name]` دوباره راه‌اندازی کنید.

### خطا: عدم هماهنگی وب‌هوک‌های Stripe
**مشکل:** پرداخت کاربر در پنل Stripe موفقیت‌آمیز است اما در دیتابیس ما `paid` ثبت نمی‌شود.
1. مطمئن شوید که `STRIPE_WEBHOOK_SECRET` دقیقاً با آنچه در پنل Stripe برای Endpoint سرور ثبت شده همخوانی دارد.
2. لاگ‌های ارور وب‌هوک را بررسی کنید: آیا Signature نامعتبر است یا دیتابیس خطای Timeout داده است؟
3. سیستم دارای جدول `stripe_events` برای بررسی Idempotency است؛ چک کنید آیا رویداد تکراری فرستاده شده است یا خیر.

### خطا: دریافت خطای 404 توسط کاربران در سایت اصلی وردپرس
اگر کاربران خطای 404 دریافت کردند (مثلا به خاطر لینک‌های قدیمی):
1. وارد فایل `functions.php` قالب وردپرس شوید.
2. آدرس قدیمی و جدید را در آرایه `$redirects` وارد کنید (سیستم 301 اتوماتیک).
3. فایل را روی سرور آپلود کنید.

---

## 🔒 امنیت دیتابیس

هیچ‌گاه به صورت خام روی جدول کاربران و لیدها کوئری نزنید. برای جلوگیری از SQL Injection همیشه از روش‌های زیر استفاده کنید:
- **در محیط وردپرس:** استفاده از دستور `$wpdb->prepare`
- **در محیط Node.js / Next.js:** استفاده از **Prisma ORM**

---

## 📝 کلیدهای مهم

```yaml
Gemini Models (Text):   [توسط .env سرور کنترل می‌شود]
Gemini Models (Vision): [توسط .env سرور کنترل می‌شود]
Stripe Webhook Secret:  [باید دقیقاً مطابق تنظیمات پنل دولوپر Stripe باشد]
Theme Version:          [جهت Cache-busting حتماً به‌روز نگه داشته شود]
```
