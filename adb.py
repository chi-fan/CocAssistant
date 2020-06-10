import subprocess
 
class Screenshot():#截取手机屏幕并保存到电脑
    def __init__(self):
        #查看连接的手机
        connect=subprocess.Popen("adb devices",stderr=subprocess.PIPE,stdout=subprocess.PIPE,shell=True)
        stdout,stderr=connect.communicate()   #获取返回命令
        #输出执行命令结果结果
        # stdout=stdout.decode("utf-8")
        # stderr=stderr.decode("utf-8")
        # print(stdout)
        # print(stderr)
 
    def screen(self,cmd):#在手机上截图
        screenExecute=subprocess.Popen(str(cmd),stderr=subprocess.PIPE,stdout=subprocess.PIPE,shell=True)
        stdout, stderr = screenExecute.communicate()
        # 输出执行命令结果结果
        stdout = stdout
        stderr = stderr
        print(stdout)
        print(stderr)
 
    def saveComputer(self,cmd):#将截图保存到电脑
        screenExecute = subprocess.Popen(str(cmd), stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        stdout, stderr = screenExecute.communicate()
        stdout = stdout
        stderr = stderr
        # 输出执行命令结果结果
        stdout = stdout
        stderr = stderr
        print(stdout)
        print(stderr)
 

