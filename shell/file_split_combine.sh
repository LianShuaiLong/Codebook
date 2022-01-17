#将文件夹下面的csv文件拆分成多个文件
#将文件夹下面多个csv文件合并成一个文件
#用于分析特征取值分布
func=$1
filefolder=$2

function split(){
    filename=$1
    columns=$(cat $filename|awk -F',' 'END {print NF}')
    echo 'filename:'$filename 'columns:'$columns
    for i in $(seq 1 $columns)
    do
        cat $filename|awk -F',' '{print $'$i'}'>$filename'_'$i
        f_name=$filename'_'$i
        if [ -f $f_name ];then
            echo $f_name'创建成功'
        else
            echo $f_name'创建失败'
        fi
    done
}
function combine(){
    filefolder=$1
    filelist=$(find $filefolder -name "*.csv_*")
    echo $filelist
    paste -d',' $filelist>$filefolder'/demo.csv'
    if [ ! -f $filefolder'/demo.csv' ];then
        echo 'demo.csv创建失败'
    else
        echo 'demo.csv创建成功'
    fi
    time rm -rf $filelist
    for file in $filelist
    do 
        if [ ! -f $file ];then
            echo $file'删除成功'
        else
            echo $file'删除失败'
        fi
    done
}

if [ $func = "0" ];then #注意这里的空格不能少！
    echo 'split func'
    for filename in `ls $filefolder`
    do
        filepath=$filefolder'/'$filename
        if [ "${filepath##*.}"x = "csv"x ]
        then 
            split $filepath
        fi
    done
else
    echo 'combine func'
    combine $filefolder
fi        