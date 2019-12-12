
# 代码维护
## discuss_parser/xueqiu_discuss_daily.py
### 描述
实时统计每天新增讨论的中涉及股票， 并且转换成股票以及股票的讨论数。
###  运行方式
每天定时运行

### 保存格式
["stock", "xid_list",  "xid_count", "created_at"]


## focus_parser/xueqiu_focus_statistics.py
### 描述
每天定时统计大V关注的股票, 增量式计算每只股票的大V关注数。然后跟当天的时间一起入库

### 运行方式
每天定时运行

### 保存格式
["symbol",  "focus_total_count", "created_at"]


# 定时任务维护
## discuss_focus_statistic_daily.sh
使用crontab每天定时运行该脚本文件，运行之前注意配置python的虚拟环境。




# 存在的问题
将stock.csv中的股票代码需要重新转换， 将引号去掉，比如['300315']

