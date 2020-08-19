import subprocess
import time

class screenShot() :
    m_debug = None
    cmdScreenShot = None
    def __init__(self, filePath = "F:/cocAssistant/picture", isDebug = False):
        self.m_debug = isDebug
        self.cmdScreenShot = "adb.exe pull /sdcard/screenshort.png " + filePath
        if self.m_debug :
            connect=subprocess.Popen("adb.exe devices",stderr=subprocess.PIPE,stdout=subprocess.PIPE,shell=True)
            stdout,stderr=connect.communicate()
            stdout=stdout
            stderr=stderr
            print(stdout)
            print(stderr)

    def getImage(self) :
        self.executeCmd("adb.exe shell /system/bin/screencap -p /sdcard/screenshort.png")
        self.executeCmd(self.cmdScreenShot)

    def executeCmd(self, cmd):
        screenExecute=subprocess.Popen(str(cmd),stderr=subprocess.PIPE,stdout=subprocess.PIPE,shell=True)
        stdout, stderr = screenExecute.communicate()
        stdout = stdout
        stderr = stderr
        print(stdout)
        print(stderr)

start = time.time()
for x in range(1) :
    cmd1=r"adb.exe shell /system/bin/screencap -p /sdcard/screenshort.png"       #命令1：在手机上截图3.png为图片名
    cmd2=r"adb.exe pull /sdcard/screenshort.png F:/cocAssistant/picture"    #命令2：将图片保存到电脑 d:/3.png为要保存到电脑的路径
    screen = screenShot()
    screen.getImage()
end = time.time()
print(end - start)
