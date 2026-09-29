[app]

title = Math Challenge
package.name = mathchallenge
package.domain = org.mathchallenge

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,json,txt

version = 1.0

requirements = python3,kivy

orientation = portrait
fullscreen = 0

android.api = 35
android.minapi = 21
android.arch = arm64-v8a

android.permissions = INTERNET

[buildozer]

log_level = 2
warn_on_root = 1
