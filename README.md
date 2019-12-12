## 代码树     
    .
    ├── configure.py  # 配置文件模块
    ├── data_reader.py  # 数据读取和预处理模块
    ├── dynamic_update.py # 事件实时更新模块
    ├── history_event.py  # 构建历史事件模块
    ├── load_history_event.py  # load历史事件代码
    ├── algorithm
    │   └── cluster # 聚类模块
    │       ├── Kmeans # kmeans聚类
    │       │   └── k_means_cluster.py
    │       ├── LDA  # kmeans聚类
    │       │   └── lda_cluster.py
    │       └── singlePass   # singlepass聚类
    │           ├── singlePassCluster.py
    │           └── singlepassrun.py
    │
    ├── corpus
    ├── data  # 预处理的数据
    ├── log  # 分词,关键词提取等日志文件
    ├── model  # 存放各类模型文件,如聚类结果、事件结果、tfidf结果
    │   ├── event_model # 存放事件结果
    │   └── tfidf_model # 存放tfidf结果
    └── utils
        ├── Keywords.py  # 关键词提取代码
        ├── cluster.py
        ├── data_process.py # 数据预处理
        ├── data_source.py  # 数据读取
        ├── dicts.py  # 分词词典
        ├── event_util.py  # 事件类库
        ├── keywords_extractor.py  # 关键词提取
        ├── my_util.py  # 工具类
        ├── mysql_util.py  # sql类
        ├── news.py  # 新闻处理类库
        ├── test.py  # 测试代码
        ├── tfidf.py  # tfidf模型训练
        ├── time_util.py  # 时间工具类
        ├── tokenization.py  # 分词模块
        └── vector.py  # 空间向量模块
# 操作手册
## step、1 数据准备
- 涉及文件：data_reader.py
- 从数据库中读取指定日期前的所有新闻，然后整理成两部分数据。
- 第一部分数据新闻的标题，正文组合在一起，然后分词去停等预处理，保存为新闻ID，发布时间， 分词后的正文；[news_id, timestamp, contents]
- 第二部分提取新闻的标题，保存新闻的新闻ID， 发布时间， 新闻标题；[news_id, timestamp, title]

## step、2 VSM训练
- 涉及文件：/utils/tfidf.py
- 构建TFIDF空间向量模型，训练预料为step、1中第一部分保存的内容。
- 空间向量模型保存。

## step、3 singlePass聚类
- 涉及文件：singlepass_run.py
- 对step、1中第一部分生成的数据进行singlePass聚类

## step、4 历史事件准备
- 涉及文件：history_event.py
- 根据step3聚类的结果，构建事件库， 包括添加事件标题，筛选事件涉及的股票，提取事件关键词等，对事件的有效性进行判断。

## step、5 事件更新
- 涉及文件：dynamic_update.py
- 当数据库中出现新的新闻之后，将新的新闻和历史事件进行合并，若合并不成功生成新的事件。


## step、6 数据写入数据库
- 涉及文件：event2mysql.py
- 事件生成之后，根据项目需求整理成规定的格式，存入数据库，目前保存的是[事件ID，事件标题， 事件包含的股票， 事件包含的新闻], [股票, 股票涉及的事件]两张表

## step、7 雪球讨论历史数据统计
- 涉及文件： xueqiu_dicsuss_batch.py， xueqiu_dicsuss_batch.py
- 统计雪球讨论数据中涉及到的相关股票

## step、8 数据格式转换
- 涉及文件： format_transform.py
- 将step 7中统计得到的数据转换数据格式，转换成个股以及个股涉及的讨论数目， 股票代码形式修改了。