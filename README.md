# تطبيق التعرف على النص العربي

تطبيق Android للتعرف على النص العربي باستخدام Kivy.

## المميزات

- واجهة مستخدم باللغة العربية
- دعم التعرف على النص العربي
- بناء تلقائي باستخدام GitHub Actions

## البناء

يتم بناء التطبيق تلقائياً عند كل push إلى branch main عبر GitHub Actions.

## التنزيل

يمكن تحميل آخر نسخة من [صفحة Releases](https://github.com/username/arabic-ocr-app/releases).

## التشغيل

1. حمل ملف APK من آخر release
2. ثبته على جهاز Android
3. افتح التطبيق وابدأ باستخدام ميزة OCR

## التطوير

```bash
git clone https://github.com/username/arabic-ocr-app
cd arabic-ocr-app/app
buildozer android debug
```
