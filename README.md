## 代码树     
    .
    ├── configure.py  # 配置文件模块
    ├── data_reader.py  # 数据读取和预处理模块
    ├── dynamic_update.py # 事件实时更新模块
    ├── history_event.py  # 构建历史事件模块
    ├── load_history_event.py  # load历史事件代码
    ├── cluster  # 聚类模块
    │   ├── Kmeans  # kmeans聚类
    │   ├── LDA  # LDA主题
    │   └── singlePass  # singlepass聚类
    │       ├── singlePassCluster.py
    │       └── singlepassrun.py
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
        
## step 1 VSM训练
## step 2 singlePass聚类
## step 3 历史事件