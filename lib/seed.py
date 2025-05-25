#!/usr/bin/env python3

# Script goes here!
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Company, Dev, Freebie

engine = create_engine('sqlite:///freebies.db')
Session = sessionmaker(bind=engine)
session = Session()

# Clear existing data (optional during development)
session.query(Freebie).delete()
session.query(Dev).delete()
session.query(Company).delete()

# Seed data
google = Company(name="Google", founding_year=1998)
microsoft = Company(name="Microsoft", founding_year=1975)
alice = Dev(name="Alice")
bob = Dev(name="Bob")


f1 = Freebie(item_name="Sticker", value=1, company=google, dev=alice)
f2 = Freebie(item_name="T-shirt", value=10, company=microsoft, dev=alice)
f3 = Freebie(item_name="Mug", value=5, company=google, dev=bob)

session.add_all([google, microsoft, alice, bob, f1, f2, f3])
session.commit()

print("Seed data created.")