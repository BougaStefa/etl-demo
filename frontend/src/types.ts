export interface Launch {
  id: string;
  name: string;
  flight_number: number;
  date_utc: string;
  success: boolean;
  details: string | null;
  rocket_id: string;
  created_at: string;
  updated_at: string;
}
