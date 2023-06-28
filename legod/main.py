
import legod
import schedule
import time
import os

if __name__ == '__main__':
    time_sleep = int(os.environ.get('SLEEP', '600'))  # 检测时间(s)，值越小使用的内存越大
    time_stop = os.environ.get('TIME_STOP',"04:00") # 指定暂停时间
    # 创建定时任务
    legod = legod.legod()
    # 测试信息是否正确
    info = legod.get_account_info()
    print(info)
    if info[0]:
        print("登录信息有效，监听中...")
    else:
        raise Exception('请检查登录信息！')
    schedule.every().day.at(time_stop).do(legod.pause)
    # schedule.every(10).seconds.do(legod.pause) # 10s一次
    
    # 循环执行定时任务
    while True:
        schedule.run_pending()
        time.sleep(time_sleep)
