[app]
title = Arabic OCR App
package.name = arabicocr
package.domain = org.example

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,txt

version = 1.0
requirements = python3,kivy,pillow,huggingface_hub,rapidocr-onnxruntime,opencv-python,numpy

presplash.filename = assets/icon.png
icon.filename = assets/icon.png

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,CAMERA
android.api = 33
android.minapi = 21

[buildozer]
log_level = 2
