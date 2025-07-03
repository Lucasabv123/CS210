-- 0. Enable the TimescaleDB extension
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;

-- 1. Contacts table
CREATE TABLE IF NOT EXISTS contacts (
  user_id      SERIAL        PRIMARY KEY,
  name         TEXT          NOT NULL,
  email        TEXT          NOT NULL UNIQUE,
  signup_date  TIMESTAMPTZ   NOT NULL,
  current_plan TEXT          NOT NULL
);

-- 2. Subscriptions table
CREATE TABLE IF NOT EXISTS subscriptions (
  subscription_id SERIAL     PRIMARY KEY,
  contact_id      INTEGER    NOT NULL
    REFERENCES contacts(user_id)
    ON DELETE CASCADE,
  plan_tier       TEXT       NOT NULL,
  start_date      DATE       NOT NULL,
  end_date        DATE,
  CONSTRAINT chk_dates CHECK (end_date IS NULL OR end_date > start_date)
);

-- 3. Interactions table
CREATE TABLE IF NOT EXISTS interactions (
  interaction_id SERIAL        PRIMARY KEY,
  contact_id     INTEGER       NOT NULL
    REFERENCES contacts(user_id)
    ON DELETE CASCADE,
  type           TEXT          NOT NULL,
  timestamp      TIMESTAMPTZ   NOT NULL,
  notes          TEXT
);

-- 4. Notifications table
CREATE TABLE IF NOT EXISTS notifications (
  notification_id    SERIAL        PRIMARY KEY,
  contact_id         INTEGER       NOT NULL
    REFERENCES contacts(user_id)
    ON DELETE CASCADE,
  timestamp          TIMESTAMPTZ   NOT NULL DEFAULT now(),
  notification_type  TEXT          NOT NULL,
  nylas_message_id   TEXT,
  send_status        TEXT,
  ack_flag           BOOLEAN
);

-- 5. Convert interactions to a hypertable (migrating existing data)
-- 5. Convert interactions to a hypertable (migrating existing data),
--    but don’t auto-create any indexes
-- 0. Enable the TimescaleDB extension
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;

-- 1. Contacts table
CREATE TABLE IF NOT EXISTS contacts (
  user_id      SERIAL        PRIMARY KEY,
  name         TEXT          NOT NULL,
  email        TEXT          NOT NULL UNIQUE,
  signup_date  TIMESTAMPTZ   NOT NULL,
  current_plan TEXT          NOT NULL
);

-- 2. Subscriptions table
CREATE TABLE IF NOT EXISTS subscriptions (
  subscription_id SERIAL     PRIMARY KEY,
  contact_id      INTEGER    NOT NULL
    REFERENCES contacts(user_id)
    ON DELETE CASCADE,
  plan_tier       TEXT       NOT NULL,
  start_date      DATE       NOT NULL,
  end_date        DATE,
  CONSTRAINT chk_dates CHECK (end_date IS NULL OR end_date > start_date)
);

-- 3. Interactions table
CREATE TABLE IF NOT EXISTS interactions (
  interaction_id SERIAL        PRIMARY KEY,
  contact_id     INTEGER       NOT NULL
    REFERENCES contacts(user_id)
    ON DELETE CASCADE,
  type           TEXT          NOT NULL,
  timestamp      TIMESTAMPTZ   NOT NULL,
  notes          TEXT
);

-- 4. Notifications table
CREATE TABLE IF NOT EXISTS notifications (
  notification_id    SERIAL        PRIMARY KEY,
  contact_id         INTEGER       NOT NULL
    REFERENCES contacts(user_id)
    ON DELETE CASCADE,
  timestamp          TIMESTAMPTZ   NOT NULL DEFAULT now(),
  notification_type  TEXT          NOT NULL,
  nylas_message_id   TEXT,
  send_status        TEXT,
  ack_flag           BOOLEAN
);

-- 5. Convert interactions to a hypertable (migrating existing data)
SELECT create_hypertable(
  'interactions', 
  'timestamp',
  if_not_exists => TRUE,
  migrate_data  => TRUE
);

-- 6. Drop old continuous aggregate if present
DROP MATERIALIZED VIEW IF EXISTS interactions_7d_counts;

-- 7. Create 7-day continuous aggregate
CREATE MATERIALIZED VIEW IF NOT EXISTS interactions_7d_counts
  WITH (timescaledb.continuous) AS
SELECT
  contact_id,
  time_bucket('1 day', timestamp) AS day,
  COUNT(*)                   AS interaction_count
FROM interactions
GROUP BY contact_id, day;



