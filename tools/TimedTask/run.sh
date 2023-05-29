


path=log
if [ ! -d ${path}  ];then
    mkdir ${path}
else
    echo  dir exist: ${path}
fi
logfile=${path}/"main.log"


author_name="lianshuailong"
task_name="copy car_sales_hive data from hive to redis"

nohup python3  -u  main.py  --config_file "./data/config.json" --task_name "car_sales"  >${logfile} 2>&1 &       #     后台运行xxx.sh，并保存log


tail -f ${logfile}      #                实时打印log



