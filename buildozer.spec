[app]

title = Math Challenge
package.name = mathchallenge
package.domain = org.mathchallenge

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,txt

version = 1.0

requirements = python3,kivy

orientation = portrait

fullscreen = 0

android.permissions = INTERNET

[buildozer]

log_level = 2

warn_on_root = 1

[app:android]

android.api = 35
android.minapi = 21
android.ndk = 27c
android.archs = arm64-v8a
