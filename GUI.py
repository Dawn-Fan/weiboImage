# 导入tkinter库
import asyncio
import tkinter
from spider_main import main
import threading
import tkinter.ttk
import time

from multiprocessing import Queue

process_num = Queue()

window = tkinter.Tk()
# 设置窗口title
window.title('my window')
# 设置窗口大小
window.geometry('500x100')


# 显示主窗口


# 启动新协程
def start_spider(url, peocess_num):
    asyncio.run(main(url, peocess_num))


# 启动新进程
def creat_thread_processing_spider():
    my_url = input_url.get()
    print(my_url)
    t = threading.Thread(target=start_spider, args=[my_url, process_num])
    t2 = threading.Thread(target=show_progress)
    t2.start()
    # t.setDaemon(True)
    t.start()
    # asyncio.get_event_loop().run_until_complete()


def show_progress():
    # 进度值最大值
    while process_num.empty():
        time.sleep(0.1)
    progressbarOne['maximum'] = process_num.get() - 1
    print("progressbarOne=======" + str(progressbarOne['maximum']))

    # 进度值初始值
    progressbarOne['value'] = 0
    while True:
        # print("===============数量为空========")
        time.sleep(0.1)
        progressbarOne['value'] = process_num.get()
        window.update()
        if progressbarOne['maximum'] == progressbarOne["value"]:
            break


tkinter.Label(window, text='请输入url').grid(row=1, column=0)
input_url = tkinter.Entry(window, width=50)
input_url.grid(row=1, column=1)

button1 = tkinter.Button(window,
                         text='启动',  # 按钮的文字
                         bg='pink',  # 背景颜色
                         width=15, height=1,  # 设置长宽
                         command=creat_thread_processing_spider
                         # 响应事件：关闭窗口
                         )
button1.grid(row=2, column=0)
progressbarOne = tkinter.ttk.Progressbar(window, length=200)
progressbarOne.grid(row=3, column=1)
window.mainloop()
