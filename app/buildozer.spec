
[app]
title = Arabic OCR App
package.name = arabicocr
package.domain = org.example

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt

version = 1.0
requirements = python3,kivy,pillow

presplash.filename = assets/icon.png
icon.filename = assets/icon.png

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25.1.8937393
android.sdk = 33

[buildozer]
log_level = 2
