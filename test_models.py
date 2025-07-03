# test_models.py
from sqlalchemy import inspect
from models import init_db, engine, Session, Contact, Subscription, Interaction, Notification

def main():
    # 1. Create all tables (if they don’t exist)
    init_db()
    print("✅ Tables created (if not already present)")

    # 2. Introspect the database to list all tables
    inspector = inspect(engine)
    print("Tables in database:", inspector.get_table_names())

    # 3. Quick CRUD test
    session = Session()
    # 3a. Create a test user
    u = Contact(name="Test User", email="test@example.com",
             signup_date="2025-01-01 00:00:00", current_plan="basic")
    session.add(u)
    session.commit()
    print("✅ Inserted User:", u.user_id)

    # 3b. Create a related subscription
    sub = Subscription(contact_id=u.user_id,
                       plan_tier="basic",
                       start_date="2025-01-01",
                       end_date=None)
    session.add(sub)
    session.commit()
    print("✅ Inserted Subscription for user:", sub.subscription_id)

    # 3c. Query back
    fetched = session.query(Contact).filter_by(email="test@example.com").first()
    print("Fetched User:", fetched.name, "with subscriptions:", [s.subscription_id for s in fetched.subscriptions])

    # Cleanup
    session.delete(sub)
    session.delete(u)
    session.commit()
    session.close()
    print("✅ Smoke test passed.")

if __name__ == "__main__":
    main()
