import sqlite3
import os
import sys
import json
from datetime import datetime

# Import the database module to use Supabase client
sys.path.append(os.getcwd())
import database

def migrate():
    summary = {
        "users": {"success": 0, "failed": 0},
        "groups": {"success": 0, "failed": 0},
        "broadcasts": {"success": 0, "failed": 0},
        "errors": []
    }

    if not database.supabase:
        err = "Supabase client not initialized. Check your environment variables (SUPABASE_URL, SUPABASE_KEY)."
        print(err)
        return {"success": False, "error": err}

    db_path = "bot.db"
    if not os.path.exists(db_path):
        err = "bot.db not found!"
        print(err)
        return {"success": False, "error": err}

    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        curr = conn.cursor()

        print("--- Starting Robust Migration ---")

        # 1. Migrate Users
        print("\nMigrating Users...")
        curr.execute("SELECT * FROM users")
        users = curr.fetchall()
        for user in users:
            try:
                joined_at = user["joined_at"]
                if joined_at and " " in joined_at:
                    joined_at = joined_at.replace(" ", "T") + "Z"
                
                last_active = user["last_active_at"]
                if last_active and " " in last_active:
                    last_active = last_active.replace(" ", "T") + "Z"
                elif not last_active:
                    last_active = datetime.now().isoformat()

                data = {
                    "id": user["id"],
                    "full_name": user["full_name"] or "Unknown",
                    "username": user["username"] or "unknown",
                    "joined_at": joined_at,
                    "last_active_at": last_active,
                    "message_count": user["message_count"] or 0,
                    "is_premium": bool(user["is_premium"]),
                    "language_code": user["language_code"] or "en"
                }
                database.supabase.table("users").upsert(data, on_conflict="id").execute()
                summary["users"]["success"] += 1
            except Exception as e:
                summary["users"]["failed"] += 1
                summary["errors"].append(f"User {user['id']}: {str(e)}")

        # 2. Migrate Groups
        print("\nMigrating Groups...")
        curr.execute("SELECT * FROM groups")
        groups = curr.fetchall()
        for group in groups:
            try:
                added_at = group["added_at"]
                if added_at and " " in added_at:
                    added_at = added_at.replace(" ", "T") + "Z"
                
                last_active = group["last_active_at"]
                if last_active and " " in last_active:
                    last_active = last_active.replace(" ", "T") + "Z"
                elif not last_active:
                    last_active = datetime.now().isoformat()

                data = {
                    "id": group["id"],
                    "title": group["title"] or "Legacy Group",
                    "type": group["type"] or "group",
                    "added_at": added_at,
                    "last_active_at": last_active,
                    "member_count": group["member_count"] or 0
                }
                database.supabase.table("groups").upsert(data, on_conflict="id").execute()
                summary["groups"]["success"] += 1
            except Exception as e:
                summary["groups"]["failed"] += 1
                summary["errors"].append(f"Group {group['id']}: {str(e)}")

        # 3. Migrate Broadcasts
        print("\nMigrating Broadcasts...")
        try:
            curr.execute("SELECT * FROM broadcasts")
            broadcasts = curr.fetchall()
            for b in broadcasts:
                try:
                    msg_ids = json.loads(b["message_ids"]) if b["message_ids"] else {}
                    t_val = b["timestamp"]
                    if t_val and " " in t_val:
                        t_val = t_val.replace(" ", "T") + "Z"
                    else:
                        t_val = datetime.now().isoformat()

                    data = {
                        "text": b["text"],
                        "target": b["target"],
                        "sent_count": b["sent_count"] or 0,
                        "failed_count": b["failed_count"] or 0,
                        "timestamp": t_val,
                        "message_ids": msg_ids
                    }
                    database.supabase.table("broadcasts").insert(data).execute()
                    summary["broadcasts"]["success"] += 1
                except Exception as e:
                    summary["broadcasts"]["failed"] += 1
                    summary["errors"].append(f"Broadcast Row Error: {str(e)}")
        except Exception:
            print("No broadcasts table found or error reading it.")

        conn.close()
        print("\n--- Migration Complete! ---")
        return {"success": True, "summary": summary}

    except Exception as e:
        print(f"Migration failed critically: {e}")
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    res = migrate()
    print(json.dumps(res, indent=2))
