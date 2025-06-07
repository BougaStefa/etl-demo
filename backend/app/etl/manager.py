from datetime import datetime, UTC
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from database import LaunchData
from etl.spacex import SpaceXAPI
import logging

logger = logging.getLogger(__name__)

class ETLManager:
    def __init__(self, db: Session):
        self.db = db
        self.spacex_api = SpaceXAPI()
        self.run_timestamp = datetime.now(UTC)
    
    def transform_launch(self, launch: Dict[Any, Any]) -> Dict[Any, Any]:
        return {
            "id": launch["id"],
            "name": launch["name"],
            "flight_number": launch["flight_number"],
            "date_utc": datetime.fromisoformat(launch["date_utc"].replace("Z", "+00:00")),
            "success": launch["success"],
            "details": launch["details"],
            "rocket_id": launch["rocket"],
            "created_at": self.run_timestamp,
            "updated_at": self.run_timestamp,
        }
    
    async def execute_etl(self) -> int:
        """
        Main ETL execution with logging
        Returns: Number of records processed
        """
        start_time = datetime.now(UTC)
        logger.info(f"Starting ETL process at {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        try:
            # Extract
            launches = await self.spacex_api.fetch_launches()
            
            # Transform
            transformed_launches = [
                self.transform_launch(launch) for launch in launches
            ]
            
            # Load
            for launch_data in transformed_launches:
                stmt = insert(LaunchData).values(**launch_data)
                update_data = launch_data.copy()
                del update_data['created_at']
                stmt = stmt.on_conflict_do_update(
                    index_elements=['id'],
                    set_=update_data
                )
                self.db.execute(stmt)
            
            self.db.commit()
            records_count = len(transformed_launches)
            logger.info(f"Successfully processed {records_count} records")
            return records_count
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"ETL failed: {str(e)}")
            raise
        finally:
            end_time = datetime.now(UTC)
            duration = (end_time - start_time).total_seconds()
            logger.info(f"ETL process completed at {end_time.strftime('%Y-%m-%d %H:%M:%S')} (duration: {duration}s)")
