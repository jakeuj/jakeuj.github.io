# Azure Machine Learning Studio 操作筆記

<web-summary>2023 年跟著 Azure Machine Learning 教學操作的補充筆記：v1 與 v2 資料類型差異、Serverless Spark、Notebook 與 Designer 部署。</web-summary>

> 首次發表：2023-07-17

這是 2023 年跟著 iT 邦幫忙系列文操作的補充筆記。原文使用 v1 API，這裡記下和當時新版介面不同的地方；操作畫面可能和現在不同。

![此篇為補充方式呈現](dotblogs-ad68d565-1689927481.jpg)

DAY03 建立 Datastore 和 Dataset （上） - 10 上傳資料檔

<https://github.com/dsindy/kaggle-titanic/blob/master/data/train.csv>

DAY04 建立 Datastore 和 Dataset （下）

## Data types vs. dataset types

### **Data asset types**

The Azure Machine Learning CLI v2 and Python SDK v2 now include the following data types:

- uri\_file (display name: File)
- uri\_folder (display name: Folder)
- mltable (display name: Table)

[Learn more about data asset types **](https://go.microsoft.com/fwlink/?linkid=2194922)

### **Dataset types**

Dataset types from Azure Machine Learning CLI v1 and Python SDK v1 can still be used, but will be mapped to the appropriate data type in the v2 systems:

- file dataset type: maps to Folder type
- tabular dataset type: maps to Table type

[Learn more about dataset types **](https://go.microsoft.com/fwlink/?linkid=2208157)

![Learn more about dataset types ](dotblogs-ad68d565-1689925912.jpg)

Compute

- NV6 (M60) 將於 2023/7/31 棄用

![NV6 (M60) 將於 2023/7/31 棄用](dotblogs-ad68d565-1689583668.jpg)

還有 serverless 可以選，但第一次按了要等三到五分鐘

![還有 serverless 可以選，但第一次按了要等三到五分鐘](dotblogs-ad68d565-1689585407.jpg)

看起來是閒置 20 min 釋放

![Expandable diagram that shows scenarios for Apache Spark session inactivity period and cluster teardown.](https://learn.microsoft.com/en-us/azure/machine-learning/media/apache-spark-azure-ml-concepts/spark-session-timeout-teardown.png?view=azureml-api-2#lightbox)

Lib 是用 pyspark，懂 Spark 可以研究一下

[在 Azure Machine Learning 中使用 Apache Spark 進行互動式資料整頓 - Azure Machine Learning | Microsoft Learn](https://learn.microsoft.com/zh-tw/azure/machine-learning/interactive-data-wrangling-with-apache-spark-azure-ml?view=azureml-api-2#import-and-wrangle-data-from-azure-machine-learning-datastore)

NoteBook Sample

```
import pandas as pd

df = pd.read_csv("azureml://subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourcegroups/MLRG/workspaces/TestWorkSpace/datastores/testdata/paths/test.csv")
df.head()
```

![NoteBook Sample](dotblogs-ad68d565-1689668278.jpg)

`azureml` 可以從設定好的 DataSet 中取得

Designer

1. select columns: Survived, Pclass, Sex, Age, SibSp, Parch, Ticket, Fare, Cabin, Embarked

2. 在右邊 asset library 輸入 train model，拖曳到 Canvas 中，用 filter based feature selection 左邊的點點連接到它。 Train model 的右邊方框，在 Label Column 選擇 Survived。(原文為  Survivde)

![在右邊 asset library 輸入 train model，拖曳到 Canvas 中，用 filter based feature selection 左](dotblogs-ad68d565-1689738324.jpg)

DAY08 部署用 Designer 做好的 Pipeline 到 Web API

![DAY08 部署用 Designer 做好的 Pipeline 到 Web API](dotblogs-ad68d565-1689923164.jpg)

`Create inference pipeline` 在 Job 結果裡面

SDK

azureml-sdk: This package has been tested with Python 3.7, 3.8, 3.9 and 3.10.

參照

[[DAY06] 開始用 Notebook 在 Azure Machine Learing 上寫程式 - iT 邦幫忙::一起幫忙解決難題，拯救 IT 人的一天 (ithome.com.tw)](https://ithelp.ithome.com.tw/articles/10269106)

[什麼是 Azure OpenAI 服務？ - Azure AI services | Microsoft Learn](https://learn.microsoft.com/zh-tw/azure/ai-services/openai/overview)
