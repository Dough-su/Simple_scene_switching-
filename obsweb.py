import threading
import obsws_python as obs
import time
import os
import win32api
import os
 
 

#录制时间
recording_time = 60
#切换时停顿时间(取决于机器速度)
stop_time = 8
#锁
lockx = "1"
#左建锁
leftlock=0
#右建锁
rightlock=0
threadx=1
# logging.basicConfig(level=logging.DEBUG)
from win10toast import ToastNotifier
toaster = ToastNotifier()
    
def get_video():
    #获取users文件夹路径
    path = os.path.expanduser('~') + "\\Videos\\"
    files = os.listdir(path)
    files.sort(key=lambda fn: os.path.getmtime(path + "\\" + fn) if not
os.path.isdir(path + "\\" + fn) else 0)
    #获取最新的视频文件名
    file_new = os.path.join(path, files[-1])
    #转换成/格式
    file_new = file_new.replace("\\", "/")
    return file_new
def switchnow():
    cl = obs.ReqClient(host='localhost', port=4455, password='123456')
    cl.set_current_program_scene('视频')
def main():
    global lockx
    if( lockx == "1"):
        lockx = "0"
        # Create an instance of the OBS Websocket
        cl = obs.ReqClient(host='localhost', port=4455, password='123456')
        # Connect to OBS Websocket
        cl.set_current_program_scene('视频')
        try:
         cl.start_record()
        except:
         print("已经开始录制") 
        time.sleep(recording_time)
        cl.stop_record()
        print(cl.send("GetInputKindList"))
        time.sleep(stop_time)
        cl.send("SetInputSettings", {"sceneName":"虚拟",
        "inputName": "test",  "inputSettings": 
        {"local_file": get_video()}})
        time.sleep(1)
        cl.set_current_program_scene('虚拟')
        lockx = "1"
def jj():
    global lockx
    global leftlock
    #启动安装的obs
    cl = obs.ReqClient(host='localhost', port=4455, password='123456')
    # Connect to OBS Websocket
    print(cl.get_current_program_scene())
    cl.set_current_program_scene('视频')
    print("已经切换到视频场景")
    try:
     cl.send("StartVirtualCam")
    except:
     print("已经启动虚拟摄像头")
    print("虚拟摄像机已启动")
    while True:
        #左键 
        if (win32api.GetAsyncKeyState(37)): 
            leftlock=1
            print("开始录制模式,不要再按了")
            toaster.show_toast("开始录制模式,不要再按了","开始录制模式,不要再按了",duration=3, icon_path = r'')
            main()
            leftlock=0
            toaster.show_toast("录制结束,可以动了","录制结束",duration=3, icon_path = r'')
        #右键
        if (win32api.GetAsyncKeyState(39)):
            print("切换到实时模式,不要再按了")
            switchnow()
            toaster.show_toast("切换到实时模式", "切换到实时模式", duration=3, icon_path = r'') 
        time.sleep(0.5)      
def start():
    #判断是否已经启动
    global threadx
    if(threadx == 1):
        threadx=0
        t = threading.Thread(target=jj)
        t.start()         
        print("开始监听")   
#修改录制时间
def set_record_time(timess): 
    #转换为int类型
    timess = int(timess)     
    global recording_time
    recording_time = timess
#修改停顿时间
def set_stop_time(timess): 
    timess = int(timess)     
    global stop_time
    stop_time = timess   
#创建tkinter窗口
import tkinter as tk  
window = tk.Tk()
window.title('OBS虚拟摄像头')
window.geometry('200x200')
e1 = tk.Entry(window, show=None)
e1.pack()
e2 = tk.Entry(window, show=None)
e2.pack()
#获取文本框的值
def get_time():
    if(e1.get() != ""):
        set_record_time(e1.get())
    if(e2.get() != ""):
        set_stop_time(e2.get())
b1 = tk.Button(window, text='修改录制时间', width=15, height=2, command=get_time)
b1.pack()
b2 = tk.Button(window, text='修改切换时间(不建议小于5)', width=20, height=2, command=get_time)
b2.pack()
b3 = tk.Button(window, text='开始', width=15, height=2, command=start)
b3.pack()
window.mainloop()


