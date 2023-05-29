# coding:utf-8
import os
import sys
import copy
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED, EVENT_JOB_ADDED
import threading


import time



path_file = os.path.realpath(__file__)
sys_path = '/'.join(path_file.split('/')[:-2])
sys.path.append(sys_path)


# from script.task_func import task_func



class TimedTask(object):
    def __init__(self, task_name, task, task_input, trigger_type, trigger_time):
        '''
        trigger_type = 'date':     固定时间点触发
                       'interval': 固定时间间隔触发
                       'cron':     在特定时间点周期性触发
        '''
        self.task_name = task_name
        self.task = task
        self.task_input = task_input
        self.trigger_type = trigger_type
        self.trigger_time = trigger_time
        self.output = {'data':None, 'state':False}  # state = False   表示无效数据， data 数据被取出后置为Fasle
        self.count_trigger = 0      
 
        print(' TimedTask init finished') 

    def listener(self, event):
        error_code = 0
        if event.code == EVENT_JOB_EXECUTED:
            self.output['data'] = copy.deepcopy(event.retval)
            self.output['state'] = True
            self.count_trigger += 1
            print(' TimedTask, job execute success , count_trigger:{}'.format(self.count_trigger))
        
        if event.code == EVENT_JOB_ADDED:
            print(' TimedTask, job add success ')
        if event.code == EVENT_JOB_ERROR:
            error_code = 113211
            print(' ERROR_{}: TimedTask, job execute error '.format(error_code))

    def init_task(self, input_data):
        scheduler = BlockingScheduler()
        scheduler.add_listener(self.listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR | EVENT_JOB_ADDED)
    
        if self.trigger_type == 'interval':
            scheduler.add_job(self.task,         # 每隔1分30秒， 运行一次 job 方法
                              self.trigger_type,
                              hours = self.trigger_time['hours'],
                              minutes = self.trigger_time['minutes'],
                              args = (input_data,))

        elif self.trigger_type == 'cron':
            scheduler.add_job(self.task,         # 每天固定时间点， 运行一次 job 方法
                              self.trigger_type,
                              hour = self.trigger_time['hour'],
                              minute = self.trigger_time['minute'],
                              second = self.trigger_time['second'],
                              args = (input_data,))
        scheduler.start()
        print(' TimedTask, init task finished ')

    def run_task(self):
        thread1 = threading.Thread(target = self.init_task, args=(self.task_input,))
        thread1.setDaemon(True)
        thread1.start()
        print(' TimedTask, init threading finished')

        #thread1.join()   # Join的作用是阻塞进程，直到线程执行完毕


if __name__ == '__main__':
    # ==== task_input 
    task_input ={ 
        'path_cmd': '../data/cmd.sh',
       }
    
    # ==== trigger 
    '''
    trigger_type = 'cron'
    trigger_time = {
                    'hour': 10,
                    'minute': 45,
                    'second': 0,
                   }
    '''
    trigger_type = 'interval'
    trigger_time = {
                    'hours': 0,
                    'minutes': 2,
                   }


    task_name = 'xxx'

    # ==== TimedTask
    timedtasker = TimedTask(task_name, task_func, task_input, trigger_type=trigger_type, trigger_time=trigger_time)
    timedtasker.run_task()

    while 1:
        time.sleep(1)         




