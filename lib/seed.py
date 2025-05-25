from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Company, Dev, Freebie

# Setup database connection and session
engine = create_engine('sqlite:///freebies.db')
Session = sessionmaker(bind=engine)
session = Session()

# 1. Clear existing data (reset tables)
session.query(Freebie).delete()
session.query(Dev).delete()
session.query(Company).delete()
session.commit()  # Commit after deletions

print("Cleared old data.")  # For your reference

# 2. Create companies and devs
google = Company(name="Google", founding_year=1998)
microsoft = Company(name="Microsoft", founding_year=1975)
alice = Dev(name="Alice")
bob = Dev(name="Bob")

session.add_all([google, microsoft, alice, bob])
session.commit()  # Commit after initial data insertion

print("Added companies and developers.")

# 3. Create freebies
f1 = Freebie(item_name="Sticker", value=1, company=google, dev=alice)
f2 = Freebie(item_name="T-shirt", value=10, company=microsoft, dev=alice)
f3 = Freebie(item_name="Mug", value=5, company=google, dev=bob)

session.add_all([f1, f2, f3])
session.commit()

print("Added freebies.")

# 4. Use Company method: give_freebie
keychain = google.give_freebie(alice, "Keychain", 3)
session.add(keychain)
session.commit()
print(f"Company gave a freebie: {keychain}")

# 5. Use class method: oldest_company
oldest = Company.oldest_company(session)
print(f"Oldest company: {oldest}")

# 6. Use Dev method: received_one
print(f"Alice received Sticker? {alice.received_one('Sticker')}")
print(f"Bob received T-shirt? {bob.received_one('T-shirt')}")

# 7. Use Dev method: give_away
first_freebie = alice.freebies[0]
print(f"Before giveaway: {first_freebie.print_details()}")
success = alice.give_away(bob, first_freebie)
if success:
    session.commit()
    print(f"Freebie given away successfully.")
else:
    print("Giveaway failed.")
print(f"After giveaway: {first_freebie.print_details()}")
