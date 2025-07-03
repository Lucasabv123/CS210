# load_features.py
import pandas as pd
from sqlalchemy import create_engine

# Configure your database URL (update host if needed)
DATABASE_URL = "postgresql://crm_user:crm_pass@localhost:5432/crm_db"


def load_rolling_window_features():
    # Create SQLAlchemy engine
    engine = create_engine(DATABASE_URL)

    # Query to fetch each contact's 7-day interaction count
    query = """
    SELECT
      c.user_id          AS contact_id,
      c.current_plan,
      COALESCE(f.interactions_last_7d, 0) AS interactions_last_7d
    FROM contacts c
    LEFT JOIN (
      SELECT
        contact_id,
        SUM(interaction_count) AS interactions_last_7d
      FROM interactions_7d_counts
      GROUP BY contact_id
    ) f ON c.user_id = f.contact_id;
    """

    # Load into a pandas DataFrame
    df = pd.read_sql(query, engine)
    print("Loaded rolling-window features for the first 5 contacts:")
    print(df.head())
    return df


if __name__ == '__main__':
    df = load_rolling_window_features()
    # Optionally, save to CSV for inspection
    df.to_csv('rolling_window_features.csv', index=False)
    print("Features saved to rolling_window_features.csv")
