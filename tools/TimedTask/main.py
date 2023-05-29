# coding:utf-8
import sys
import json
import argparse
import time

from schedule_utils.timed_task import TimedTask
from redis_utils.update_redis import task_func




def parse_parser():
	
    parser = argparse.ArgumentParser()

    parser.add_argument("--author_name", default="xxx", type=str,
                        help=" task name ")
    parser.add_argument("--task_name", default="copy xxx data from hive to redis", type=str,
                        help=" task name ")
    parser.add_argument("--config_file", default="./data/config.json", type=str,
                        help=" config file")

    args= parser.parse_args()

    return args



def process():

    # ==== config   
    args = parse_parser()
    print(' ############## start ###############')
    print(' #### args: ', args)
    
    task_name = args.task_name 
    config = json.loads(open(args.config_file,'r').read())
     
    task_input ={
        'data_cmd': config['data_cmd'],
        'redis_config':config['redis_config'],
		'video_themes':config['video_themes']
       }



    # ==== trigger
    # ==== 兼容linux的crontab
    trigger_type = 'cron'  
    trigger_time = {
                    'hour': 14,
                    'minute': 32,
                    'second': 0,
                   }


    # ==== TimedTask
    timedtasker = TimedTask(task_name, task_func, task_input,trigger_type=trigger_type, trigger_time=trigger_time)
    timedtasker.run_task()

    while 1:
        time.sleep(1)



if __name__ == '__main__':

    process()    





