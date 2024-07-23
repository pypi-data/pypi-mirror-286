"""
数据库工具
"""

from .tools import now
from .tools import logger
from .tools import to_excel

__all__ = [
    "redisdb",
    "mongodb",
    "mongo_distinct",
    "mongo_insert",
    "mongo_sample",
    "mongo_tongji",
    "mongo_to_csv",
    "mongo_to_jsonl",
]


def redisdb(host="localhost", port=6379, db=0, password=None):
    """
    连接 redis 数据库
    """
    import redis

    return redis.Redis(host=host, port=port, db=db, password=password)


def mongodb(host, database, port: int | None = None, **kwargs):
    """
    连接 MongoDB

    host: mongo 链接
    database: 数据库名称
    port: mongo 端口

    host 有密码格式: "mongodb://username:password@192.168.0.1:27017/"
    host 无密码格式: "mongodb://192.168.0.1:27017/"
    """
    from pymongo import MongoClient

    try:
        client = MongoClient(host, port, **kwargs)
        db = client[database]
        db.list_collection_names()
        logger.success(f"MongoDB 成功连接到 {database}")
        return db
    except Exception as e:
        logger.error("MongoDB 连接失败:", str(e))
        return None


def mongo_sample(
    table,
    match: dict = {},
    *,
    size: int = 1000,
    excel: bool = True,
) -> list:
    """
    mongodb 随机样本抽样

    table: mongo 表(集合), Collection 对象
    match: 匹配条件，默认不筛选
    size: 随机样本数量
    to_excel_func: 用于导出到Excel的函数，默认为to_excel
    """
    results = list(
        table.aggregate(
            [
                {"$match": match},
                {"$sample": {"size": size}},
            ]
        )
    )
    if excel:
        import pandas as pd

        filename = f"{now(7)}_{table}_sample_{size}.xlsx"
        df = pd.DataFrame(results)
        to_excel(df, filename)

    return results


def mongo_tongji(
    mongodb,
    prefix: str = "",
    tongji_table: str = "tongji",
) -> dict:
    """
    统计 mongodb 每个集合的`文档数量`

    mongodb: mongo 库
    prefix: mongo 表(集合)前缀, 默认空字符串可以获取所有表, 字段名称例如 `统计_20240101`。
    tongji_table: 统计表名称，默认为 tongji
    """

    tongji = mongodb[tongji_table]
    key = prefix if prefix else f"统计_{now(7)}"
    collection_count_dict = {
        **(
            tongji.find_one({"key": key}).get("count")
            if tongji.find_one({"key": key})
            else {}
        ),
        **(
            {
                i: mongodb[i].estimated_document_count()
                for i in mongodb.list_collection_names()
                if i.startswith(prefix)
            }
        ),
    }
    tongji.update_one(
        {"key": prefix if prefix else f"统计_{now(7)}"},
        {"$set": {"count": collection_count_dict}},
        upsert=True,
    )
    return dict(sorted(collection_count_dict.items()))


def mongo_distinct(table, *fields):
    """
    mongo distinct 去重

    table: mongo 表(集合), Collection 对象
    fields: 字段名称，支持多个字段
    """
    pipeline = [{"$group": {"_id": {i: f"${i}" for i in fields}}}]
    agg_results = table.aggregate(pipeline)
    results = [i["_id"] for i in agg_results]
    return results


def mongo_to_csv(table, output_file: str, batch_size: int = 1000):
    """
    从MongoDB集合中导出数据到CSV文件

    table: MongoDB的集合名称或Collection对象
    output_file: 导出的CSV文件路径
    batch_size: 批处理大小，默认为1000
    """
    import pymongo
    import csv

    if not isinstance(table, pymongo.collection.Collection):
        raise ValueError("table 必须是 MongoDB Collection对象")

    try:
        with open(output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, quoting=1)
            cursor = table.find().batch_size(batch_size)
            header = table.find_one().keys() if table.find_one() else []
            writer.writerow(header)
            for doc in cursor:
                record = []
                for key in header:
                    if key not in doc:
                        record.append("")
                    else:
                        record.append(str(doc[key]))
                writer.writerow(record)
    except Exception as e:
        logger.error(f"mongo_to_csv 发生错误: {e}")


def mongo_to_jsonl(table, output_file: str, batch_size: int = 1000):
    """
    mongo 导出 jsonl

    table: mongo 表(集合), Collection 对象
    output_file: 导出的 jsonl 文件名
    batch_size: 批处理大小，默认为1000
    """
    import pymongo
    import json

    if not isinstance(table, pymongo.collection.Collection):
        raise ValueError("table 必须是 MongoDB Collection对象")

    try:
        with open(output_file, "w", encoding="utf-8") as f:
            cursor = table.find().batch_size(batch_size)
            for doc in cursor:
                doc["_id"] = str(doc["_id"])
                f.write(json.dumps(doc, ensure_ascii=False) + "\n")
    except Exception as e:
        logger.error(f"发生错误: {e}")


def mongo_insert(table, data: list[dict] | dict):
    """
    mongo 批量插入

    table: mongo 表(集合), Collection 对象
    data: 数据列表，每个元素为一个字典
    """
    try:
        if isinstance(data, dict):
            data = [data]
        table.insert_many(data, ordered=False)
    except Exception:
        pass
