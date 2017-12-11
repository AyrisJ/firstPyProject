# coding:utf-8

import time
from apscheduler.schedulers.blocking import BlockingScheduler


sched=BlockingScheduler()
# 多个定时器，只有一个生效，第一个
# sched2=BlockingScheduler()


def my_job1():
    print time.strftime('Job1:%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


#1. add_job设置执行触发时间
sched.add_job(my_job1,'interval',seconds=5,id='my_job1_id')


#2. 修饰器设置执行触发时间
@sched.scheduled_job('interval',seconds=4,id="my_job2_id")
def my_job2():
    print time.strftime('Job2:%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


# 根据id移除不需要的job
# sched.remove_job('my_job2_id')
starttime=time.time()
# 获取job列表
print sched.get_jobs()

# 暂停job,需要再job开始前设置，开始后可以启动
sched.pause_job('my_job1_id')

sched.start()

#再启动job
#sched.resume_job("my_job1_id")


# 任务作业调度三种模式
# 1. cron定时调度
# sched.add_job(my_job, 'cron', year=2017,month = 03,day = 22,hour = 17,minute = 19,second = 07)
# 2. interval 间隔调度
# sched.add_job(my_job, 'interval',days  = 03,hours = 17,minutes = 19,seconds = 07)
# 3. date 定时调度
# sched.add_job(my_job, 'date', run_date=date(2009, 11, 6), args=['text'])















