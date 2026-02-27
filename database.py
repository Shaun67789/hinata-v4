import os
import json
import logging
from supabase import create_client, Client
from datetime import datetime

# Setup Logger
logger = logging.getLogger("hinata.database")

# Supabase Configuration
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY =os.environ.get("SUPABASE_KEY")

supabase: Client = None

if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        logger.info("Supabase Neural Connection Established.")
    except Exception as e:
        logger.error("Failed to connect to Supabase: %s", e)
else:
    logger.warning("SUPABASE_URL or SUPABASE_KEY missing. Database operations will fail.")

# --- User Operations ---

def add_user(user_id: int, full_name: str, username: str):
    if not supabase: return False
    
    try:
        data = {
            "id": user_id,
            "full_name": full_name,
            "username": username,
            "last_active_at": datetime.now().isoformat()
        }
        
        # Upsert logic in Supabase (PostgreSQL)
        supabase.table("users").upsert(data, on_conflict="id").execute()
        return True
    except Exception as e:
        logger.error(f"DB Error (add_user): {e}")
        return False

def get_all_users():
    if not supabase: return []
    try:
        res = supabase.table("users").select("*").order("joined_at", desc=True).execute()
        return res.data
    except Exception as e:
        logger.error(f"DB Error (get_all_users): {e}")
        return []

def get_user(user_id: int):
    if not supabase: return None
    try:
        res = supabase.table("users").select("*").eq("id", user_id).execute()
        return res.data[0] if res.data else None
    except Exception as e:
        logger.error(f"DB Error (get_user): {e}")
        return None

def update_user(user_id: int, updates: dict):
    if not supabase: return False
    try:
        supabase.table("users").update(updates).eq("id", user_id).execute()
        return True
    except Exception as e:
        logger.error(f"DB Error (update_user): {e}")
        return False

def add_user_warn(user_id: int):
    if not supabase: return 0
    try:
        user = get_user(user_id)
        new_warns = (user.get("warn_count") or 0) + 1 if user else 1
        supabase.table("users").update({"warn_count": new_warns}).eq("id", user_id).execute()
        return new_warns
    except Exception as e:
        logger.error(f"DB Error (add_user_warn): {e}")
        return 0

def add_user_points(user_id: int, points: int):
    if not supabase: return 0
    try:
        user = get_user(user_id)
        new_points = (user.get("points") or 0) + points if user else points
        supabase.table("users").update({"points": new_points}).eq("id", user_id).execute()
        return new_points
    except Exception as e:
        logger.error(f"DB Error (add_user_points): {e}")
        return 0

# --- Group Operations ---

def add_group(chat_id: int, title: str, chat_type: str):
    if not supabase: return False
    try:
        data = {
            "id": chat_id,
            "title": title,
            "type": chat_type,
            "last_active_at": datetime.now().isoformat()
        }
        supabase.table("groups").upsert(data, on_conflict="id").execute()
        return True
    except Exception as e:
        logger.error(f"DB Error (add_group): {e}")
        return False

def update_group(chat_id: int, updates: dict):
    if not supabase: return False
    try:
        supabase.table("groups").update(updates).eq("id", chat_id).execute()
        return True
    except Exception as e:
        logger.error(f"DB Error (update_group): {e}")
        return False

def get_all_groups():
    if not supabase: return []
    try:
        res = supabase.table("groups").select("*").order("added_at", desc=True).execute()
        return res.data
    except Exception as e:
        logger.error(f"DB Error (get_all_groups): {e}")
        return []

def get_group(chat_id: int):
    if not supabase: return None
    try:
        res = supabase.table("groups").select("*").eq("id", chat_id).execute()
        return res.data[0] if res.data else None
    except Exception as e:
        logger.error(f"DB Error (get_group): {e}")
        return None

# --- Broadcast Operations ---

def add_broadcast(text: str, target: str, sent: int, failed: int, message_ids_map: dict):
    if not supabase: return False
    try:
        data = {
            "text": text,
            "target": target,
            "sent_count": sent,
            "failed_count": failed,
            "message_ids": message_ids_map
        }
        supabase.table("broadcasts").insert(data).execute()
        return True
    except Exception as e:
        logger.error(f"DB Error (add_broadcast): {e}")
        return False

def get_all_broadcasts():
    if not supabase: return []
    try:
        res = supabase.table("broadcasts").select("*").order("timestamp", desc=True).execute()
        return res.data
    except Exception as e:
        logger.error(f"DB Error (get_all_broadcasts): {e}")
        return []

def get_broadcast(b_id: int):
    if not supabase: return None
    try:
        res = supabase.table("broadcasts").select("*").eq("id", b_id).execute()
        return res.data[0] if res.data else None
    except Exception as e:
        logger.error(f"DB Error (get_broadcast): {e}")
        return None

def delete_broadcast_record(b_id: int):
    if not supabase: return False
    try:
        supabase.table("broadcasts").delete().eq("id", b_id).execute()
        return True
    except Exception as e:
        logger.error(f"DB Error (delete_broadcast_record): {e}")
        return False

# --- Chat History Operations ---

def save_chat_history(chat_id: int, user_id: int, role: str, message: str):
    if not supabase: return False
    try:
        data = {
            "chat_id": chat_id,
            "user_id": user_id,
            "role": role,
            "message": message
        }
        supabase.table("chat_history").insert(data).execute()
        return True
    except Exception as e:
        logger.error(f"DB Error (save_chat_history): {e}")
        return False

def get_chat_history(chat_id: int, limit: int = 10):
    if not supabase: return []
    try:
        res = supabase.table("chat_history") \
            .select("role, message") \
            .eq("chat_id", chat_id) \
            .order("timestamp", desc=True) \
            .limit(limit) \
            .execute()
        # Return in chronological order
        return [{"role": row["role"], "message": row["message"]} for row in reversed(res.data)]
    except Exception as e:
        logger.error(f"DB Error (get_chat_history): {e}")
        return []

def clear_chat_history(chat_id: int):
    if not supabase: return False
    try:
        supabase.table("chat_history").delete().eq("chat_id", chat_id).execute()
        return True
    except Exception as e:
        logger.error(f"DB Error (clear_chat_history): {e}")
        return False
