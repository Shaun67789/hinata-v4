# 🚀 Hinata Bot - Render & Supabase Deployment Guide

Follow these steps to deploy your bot with Cloud Persistence.

## 1. Supabase Setup (Database)

1.  Go to [Supabase](https://supabase.com/) and create a new project.
2.  Open the **SQL Editor** in the left sidebar.
3.  Open the file `supabase_schema.sql` from this repository, copy the code, and paste it into the SQL Editor.
4.  Click **Run**. Your tables are now ready!
5.  Go to **Project Settings > API** and copy:
    - `URL` (Project URL)
    - `service_role` key (Secret Key) -- **DO NOT use the anon key for admin control.**

## 2. Render Deployment (Web & Bot)

1.  Create a new **Web Service** on Render.
2.  Connect your GitHub repository.
3.  **Runtime**: `Python 3`
4.  **Build Command**: `pip install -r requirements.txt`
5.  **Start Command**: `python main.py`

## 3. Environment Variables

In Render, go to **Environment** and add:

- `BOT_TOKEN`: Your Telegram Bot Token.
- `SUPABASE_URL`: Your Supabase Project URL.
- `SUPABASE_KEY`: Your Supabase `service_role` Secret Key.
- `PYTHON_VERSION`: `3.10.0` (Recommended for stability on Render).

## 4. Web Dashboard Control

Once deployed, visit your Render URL (e.g., `https://hinata-bot.onrender.com`).

- Use the dashboard to view live logs.
- Monitor your Supabase instance for real-time user data.
- Manage downloads and cleanup tasks automatically.

---

_Hinata is now powered by the Cloud. 🌸_
