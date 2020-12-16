# -*- coding: utf-8 -*-
import os

ThisPath = os.path.dirname(os.path.realpath(__file__))
YosemiteApk = os.path.join(ThisPath, 'android' , "apks", "Yosemite.apk")
YosemitePackage = 'com.netease.nie.yosemite'
LogFile = os.path.join(ThisPath, './temp/cocAssistant.log')
DefaultAdbPath = {
    "Windows": os.path.join("adb.exe"),
    "Darwin": os.path.join(ThisPath, "adb", "mac", "adb"),
    "Linux": os.path.join(ThisPath, "adb", "linux", "adb"),
    "Linux-x86_64": os.path.join(ThisPath, "adb", "linux", "adb"),
    "Linux-armv7l": os.path.join(ThisPath, "adb", "linux_arm", "adb"),
}
AppWindowsName = 'CocAssistant -- 部落冲突辅助 by chifan and HoneyGump'
SerialNumber = '127.0.0.1:62001'
