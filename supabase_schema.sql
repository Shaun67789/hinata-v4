-- Hinata Bot - Supabase PostgreSQL Schema
-- Paste this into the Supabase SQL Editor to initialize your database.

-- 1. Users Table
CREATE TABLE IF NOT EXISTS users (
    id BIGINT PRIMARY KEY,
    full_name TEXT,
    username TEXT,
    joined_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_active_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    message_count INTEGER DEFAULT 0,
    is_premium BOOLEAN DEFAULT FALSE,
    is_banned BOOLEAN DEFAULT FALSE,
    is_admin BOOLEAN DEFAULT FALSE,
    warn_count INTEGER DEFAULT 0,
    points INTEGER DEFAULT 0,
    language_code TEXT,
    metadata JSONB DEFAULT '{}'::jsonb
);

-- 2. Groups Table
CREATE TABLE IF NOT EXISTS groups (
    id BIGINT PRIMARY KEY,
    title TEXT,
    type TEXT,
    added_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_active_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    member_count INTEGER DEFAULT 0,
    is_muted BOOLEAN DEFAULT FALSE,
    settings JSONB DEFAULT '{"welcome_enabled": true}'::jsonb
);

-- 3. Broadcasts Table
CREATE TABLE IF NOT EXISTS broadcasts (
    id BIGSERIAL PRIMARY KEY,
    text TEXT,
    target TEXT,
    sent_count INTEGER,
    failed_count INTEGER,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    message_ids JSONB
);

-- 4. Chat History Table
CREATE TABLE IF NOT EXISTS chat_history (
    id BIGSERIAL PRIMARY KEY,
    chat_id BIGINT,
    user_id BIGINT,
    role TEXT, -- 'user' or 'hinata'
    message TEXT,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 5. Performance Indexes
CREATE INDEX IF NOT EXISTS idx_chat_history_chat_id ON chat_history(chat_id);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_is_banned ON users(is_banned);
