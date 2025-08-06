# ClickHouse 系列：與 Kafka 整合打造即時 Data Streaming Pipeline

這個專案整合了 **Kafka 和 ClickHouse** 整合環境，用於建立即時 Data Streaming Pipeline。專案包含資料 Produce、Consume、Store和Query的完整流程。

此專案為最小可行性方案，只有簡單設定服務。

## 🚀 Quick Start

> 需具備 [Make](https://ftp.gnu.org/gnu/make/)、Python 3.10+，我們的快速指令會由 makefile 驅動。

### 1. 環境設定

```bash
# 建立 Python 虛擬環境並安裝 Dependencies
make setup

# 啟動所有服務
make up

# 初始化 ClickHouse Tables
make init
```

### 2. 測試 Data Streaming

```bash
# 生產測試資料到 Kafka
make produce

# 查詢 ClickHouse 中的資料
make query
```

## Port

| Service | Port | Description | URL |
|------|------|------|------|
| Zookeeper | 2181 | 協調服務 | - |
| Kafka | 9092 | 外部連接 | `localhost:9092` |
| Kafka | 9093 | 內部連接 | `kafka:9093` |
| ClickHouse HTTP | 8123 | HTTP 介面 | `localhost:8123` |
| ClickHouse Native | 9000 | 原生協議 | `localhost:9000` |
| Kafka UI | 7777 | 管理介面 | `http://localhost:7777` |

## 📁 專案結構

```
kafka-clickhouse-data-streaming-pipeline/
├── docker-compose.yml          # Docker 服務配置
├── create_tables.sql           # ClickHouse 表格初始化
├── kafka_producer.py           # Kafka 資料生產者
├── clickhouse_query.py         # ClickHouse 資料查詢工具
├── requirements.txt            # Python 依賴套件
├── makefile                   # 專案管理腳本
├── .gitignore                 # Git 忽略檔案
└── README.md                  # 專案說明文件
```

## 核心功能

### 1. Kafka 資料生產

`kafka_producer.py` 會持續產生隨機事件資料並發送到 Kafka：

```python
# 產生的事件格式
{
    "UserID": 1234,
    "Action": "click",
    "EventDate": "2024-01-01 12:00:00",
}
```

### 2. ClickHouse 資料儲存

使用 Kafka Engine 和 Materialized View 實現即時資料流：

- **user_events**: 主要事件表格
- **kafka_user_events**: Kafka Engine 表格
- **kafka_to_events_mv**: Materialized View，自動同步資料

### 3. 資料查詢

`clickhouse_query.py` 提供資料查詢功能：

- 檢查表格狀態
- 統計記錄數量
- 查詢最近記錄
- 按動作分組統計

## 監控和管理

### Kafka UI

前往 `http://localhost:7777` 來管理 Kafka：

- 查看 Topics 和 Partitions
- 監控 Consumer Groups
- 瀏覽訊息內容
- 管理 Topic 設定

### ClickHouse UI

前往 `http://localhost:7777` 來查看 ClickHouse：
- 帳號密碼為：default
- 查詢 `kafka_user_events` 請在最後加上 `SETTINGS stream_like_engine_allow_direct_select = 1` (ClickHouse 預設不支援直接讀取)

## 授權

本專案採用 MIT 授權條款。

## 貢獻

歡迎提交 Issue 和 Pull Request 來改善這個專案！
