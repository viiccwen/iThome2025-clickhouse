import clickhouse_connect

# ClickHouse Config
CLICKHOUSE_HOST = 'localhost'
CLICKHOUSE_PORT = 8123

def connect_clickhouse():
    """connect to ClickHouse"""
    try:
        client = clickhouse_connect.get_client(
            host=CLICKHOUSE_HOST,
            port=CLICKHOUSE_PORT,
            username='default',
            password='default'
        )
        print("connected to ClickHouse!")
        return client
    except Exception as e:
        print(f"connect to ClickHouse failed: {e}")
        return None

def check_tables(client):
    """check tables"""
    try:
        result = client.query("SHOW TABLES")
        print("existing tables:")
        for row in result.result_rows:
            print(f"  - {row[0]}")
        return True
    except Exception as e:
        print(f"check tables failed: {e}")
        return False

def query_data(client):
    """query data"""
    try:
        # query total records
        count_result = client.query("SELECT COUNT(*) FROM default.user_events")
        total_count = count_result.result_rows[0][0]
        print(f"\ntotal records: {total_count}")
        
        if total_count > 0:
            # query recent 10 records
            recent_result = client.query("""
                SELECT EventDate, UserID, Action 
                FROM default.user_events 
                ORDER BY EventDate DESC 
                LIMIT 10
            """)
            
            print("\nrecent 10 records:")
            print("-" * 60)
            for row in recent_result.result_rows:
                print(f"  {row[0]} | UserID: {row[1]} | Action: {row[2]}")
        
        # group by Action
        action_stats = client.query("""
            SELECT Action, COUNT(*) as count 
            FROM default.user_events 
            GROUP BY Action 
            ORDER BY count DESC
        """)
        
        print("\ngroup by Action:")
        print("-" * 30)
        for row in action_stats.result_rows:
            print(f"  {row[0]}: {row[1]} records")
            
    except Exception as e:
        print(f"query data failed: {e}")

def main():
    print("ClickHouse data query tool")
    print("=" * 40)
    
    client = connect_clickhouse()
    if client:
        check_tables(client)
        query_data(client)
        client.close()

if __name__ == "__main__":
    main() 