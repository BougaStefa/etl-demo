from datetime import datetime, UTC
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from database import LaunchData
from etl.spacex import SpaceXAPI

class ETLManager:
    def __init__(self, db: Session):
        self.db = db
        self.spacex_api = SpaceXAPI()
    
    def transform_launch(self, launch: Dict[Any, Any]) -> Dict[Any, Any]:
        now = datetime.now(UTC)
        return {
            "id": launch["id"],
            "name": launch["name"],
            "flight_number": launch["flight_number"],
            "date_utc": datetime.fromisoformat(launch["date_utc"].replace("Z", "+00:00")),
            "success": launch["success"],
            "details": launch["details"],
            "rocket_id": launch["rocket"],
            "created_at": now,
            "updated_at": now,
        }
    
    async def run_etl(self):
        try:
            launches = await self.spacex_api.fetch_launches()
            
            transformed_launches = [
                self.transform_launch(launch) for launch in launches
            ]
            
            for launch_data in transformed_launches:
                stmt = insert(LaunchData).values(**launch_data)

                # dont updated created_at
                update_data = launch_data.copy()
                del update_data['created_at']

                stmt = stmt.on_conflict_do_update(
                    index_elements=['id'],
                    set_=update_data
                )
                self.db.execute(stmt)
            
            self.db.commit()
            return len(transformed_launches)
            
        except Exception as e:
            self.db.rollback()
            raise
