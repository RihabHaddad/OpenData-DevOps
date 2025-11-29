from etl.fetch_data import fetch_data
from etl.load_db import create_table, insert_data
import sys
import logging


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

def main():
    try:
        logger.info(" Starting ETL process...")
        
        create_table()
        
        total_records = []
        batch_size = 100
        offset = 0
        max_records = 1000 
        
        while len(total_records) < max_records:
            logger.info(f"Fetching batch (offset: {offset})...")
            batch = fetch_data(limit=batch_size, offset=offset)
            
            if not batch:
                logger.info("No more records to fetch")
                break
            
            total_records.extend(batch)
            offset += len(batch)
            logger.info(f" Batch fetched: {len(batch)} records")
            
            if len(batch) < batch_size:
                logger.info("🏁 Reached last page")
                break
        
        logger.info(f"Total records fetched: {len(total_records)}")
        
        if total_records:
            insert_data(total_records)
            logger.info("ETL completed successfully!")
        else:
            logger.warning("⚠️ No records to process")
            
    except Exception as e:
        logger.error(f" ETL failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()