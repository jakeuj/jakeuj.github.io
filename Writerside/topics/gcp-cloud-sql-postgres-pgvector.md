# Cloud SQL for PostgreSQL 使用 pgvector 向量搜尋

<web-summary>在 Cloud SQL for PostgreSQL 啟用 pgvector，用餘弦距離查相似向量，並以文字陣列欄位做出類似 Vertex AI namespace 的篩選。</web-summary>

> 首次發表：2024-01-24

在 Cloud SQL 的 PostgreSQL 啟用 `vector` 擴充就能做向量搜尋；再加一個 `namespace` 文字陣列欄位，可以做到類似 Vertex AI Vector Search 的命名空間篩選。

![並加入 namespace 字串陣列以達到原本 Vertext AI 向量搜尋中的篩選限制命名空間](dotblogs-bee17aac-1706066202.jpg)

## 結論

```
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE embeddings(
      id INTEGER,
      embedding vector(3)
);

INSERT INTO embeddings
           VALUES
                   (1, '[1, 0, -1]'),
                   (2, '[1, 1, 1]'),
                   (3, '[1, 1, 50]');

SELECT id,1 - (embedding <=> '[1, 0, -1]') AS similarity
FROM embeddings
WHERE 1 - (embedding <=> '[1, 0, -1]') > 0.5
ORDER BY similarity DESC
LIMIT 1
```

## 說明

使用 GCP Cloud SQL Postgres 向量搜尋

## 補充

參考 [Filter vector matches  |  Vertex AI  |  Google Cloud](https://cloud.google.com/vertex-ai/docs/vector-search/filtering) 加入限制條件

1. 於向量表加入新文字陣列欄位 namespace

![於向量表加入新文字陣列欄位 namespace](dotblogs-bee17aac-1706069069.jpg)

    2. 更新 namespace 資料 1, {val1,val2}

    3. 新增資料 4, [1.0.-1.5], {val3,val2}

    4 搜尋向量 [1, 0.5. -0.5]

```
SELECT id,1 - (embedding <=> '[1, 0.5, -0.5]') AS similarity, namespace
FROM embeddings
WHERE 1 - (embedding <=> '[1, 0.5, -0.5]') > 0.5
ORDER BY similarity DESC
LIMIT 2;
```

可以看到會找到符合的資料 1 與 4

![可以看到會找到符合的資料 1 與 4](dotblogs-bee17aac-1706069540.jpg)

    5. 加入 where 條件 `AND 'val1' =  ANY (namespace)`

```
SELECT id,1 - (embedding <=> '[1, 0.5, -0.5]') AS similarity, namespace
FROM embeddings
WHERE 1 - (embedding <=> '[1, 0.5, -0.5]') > 0.5
AND 'val1' =  ANY (namespace)
ORDER BY similarity DESC
LIMIT 2;
```

![5. 加入 where 條件 AND 'val1' = ANY (namespace)](dotblogs-bee17aac-1706069157.jpg)

可以看到資料 4 的 namespace 因為不包含 `val1` 所以不會出現在搜尋結果

[8.15. 陣列 - PostgreSQL 正體中文使用手冊](https://docs.postgresql.tw/the-sql-language/data-types/arrays#id-8.15.5.-searching-in-arrays)

## 參照

[將 pgvector、LLM 和 LangChain 與 Google Cloud 資料庫結合使用 |Google Cloud 博客](https://cloud.google.com/blog/products/databases/using-pgvector-llms-and-langchain-with-google-cloud-databases)

## 延伸閱讀

[GCP Cloud SQL Proxy 本地連線不開白名單](GCP-Cloud-SQL-Proxy-本地連線不開白名單.md)
