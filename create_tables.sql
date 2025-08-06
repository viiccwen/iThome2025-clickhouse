-- ClickHouse Tables Setup
DROP TABLE IF EXISTS default.user_events;
DROP TABLE IF EXISTS default.kafka_user_events;
DROP TABLE IF EXISTS default.kafka_to_events_mv;

-- Main Events Table
CREATE TABLE IF NOT EXISTS default.user_events
(
    UserID UInt64,
    Action String,
    EventDate DateTime,
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(EventDate)
ORDER BY (UserID, EventDate);

-- Kafka Engine Table
CREATE TABLE IF NOT EXISTS default.kafka_user_events
(
    UserID UInt64,
    Action String,
    EventDate DateTime,
) ENGINE = Kafka()
SETTINGS
    kafka_broker_list = 'kafka:29092',
    kafka_topic_list = 'user_events_topic',
    kafka_group_name = 'clickhouse_consumer_v3',
    kafka_format = 'JSONEachRow',
    kafka_num_consumers = 1,
    kafka_thread_per_consumer = 1;

-- Materialized View to stream data from Kafka to main table
CREATE MATERIALIZED VIEW IF NOT EXISTS default.kafka_to_events_mv TO default.user_events AS
SELECT 
    UserID,
    Action,
    EventDate,
FROM default.kafka_user_events; 