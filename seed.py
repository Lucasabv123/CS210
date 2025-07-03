from faker import Faker
from datetime import timedelta
from models import Contact, Subscription, init_db, Session

def seed(n=100):
    fake = Faker()
    init_db()
    session = Session()

    contacts = []
    for _ in range(n):
        signup = fake.date_time_between('-90d', 'now')
        plan   = fake.random_element(['basic','pro','trial'])
        c = Contact(
            name=fake.name(),
            email=fake.unique.email(),
            signup_date=signup,
            current_plan=plan
        )
        contacts.append(c)
    session.bulk_save_objects(contacts)
    session.commit()

    subs = []
    for c in session.query(Contact).all():
        end = c.signup_date + timedelta(days=30) if c.current_plan=='trial' else None
        subs.append(Subscription(
            contact_id=c.user_id,
            plan_tier=c.current_plan,
            start_date=c.signup_date.date(),
            end_date=end
        ))
    session.bulk_save_objects(subs)
    session.commit()
    session.close()
    print(f"Seeded {n} contacts and subscriptions.")

if __name__ == '__main__':
    seed(100)
