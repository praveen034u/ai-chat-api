"""
Repository for teacher_daily_content table using Supabase
"""
from typing import Optional, Dict, Any
from datetime import date, datetime
from app.db.supabase_client import get_supabase_client

TABLE = "teacher_daily_content"

class DailyContentRepository:
    def __init__(self):
        self.client = get_supabase_client()

    async def create_draft(self, payload: Dict[str, Any]) -> Dict:
        resp = self.client.table(TABLE).insert(payload).execute()
        if resp.error:
            raise Exception(f"Supabase error: {resp.error.message}")
        return resp.data[0]

    async def update_draft(self, draft_id: str, payload: Dict[str, Any]) -> Dict:
        resp = self.client.table(TABLE).update(payload).eq("id", draft_id).execute()
        if resp.error:
            raise Exception(f"Supabase error: {resp.error.message}")
        return resp.data[0]

    async def get_draft_by_id(self, draft_id: str) -> Optional[Dict]:
        resp = self.client.table(TABLE).select("*").eq("id", draft_id).single().execute()
        if resp.error:
            return None
        return resp.data

    async def get_existing_draft_by_class_and_date(self, class_id: str, content_date: date, teacher_id: str) -> Optional[Dict]:
        resp = self.client.table(TABLE).select("*") \
            .eq("class_id", class_id) \
            .eq("content_date", str(content_date)) \
            .eq("teacher_id", teacher_id) \
            .eq("status", "draft") \
            .single().execute()
        if resp.error:
            return None
        return resp.data

    async def get_published_by_class_and_date(self, class_id: str, content_date: date) -> Optional[Dict]:
        resp = self.client.table(TABLE).select("*") \
            .eq("class_id", class_id) \
            .eq("content_date", str(content_date)) \
            .eq("status", "published") \
            .single().execute()
        if resp.error:
            return None
        return resp.data

    async def publish_draft(self, draft_id: str, published_at: datetime) -> Dict:
        resp = self.client.table(TABLE).update({"status": "published", "published_at": published_at}).eq("id", draft_id).execute()
        if resp.error:
            raise Exception(f"Supabase error: {resp.error.message}")
        return resp.data[0]

    async def get_teacher_content_by_id(self, draft_id: str) -> Optional[Dict]:
        resp = self.client.table(TABLE).select("*").eq("id", draft_id).single().execute()
        if resp.error:
            return None
        return resp.data
