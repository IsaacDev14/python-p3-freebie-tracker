from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Company, Dev, Freebie

if __name__ == '__main__':
    engine = create_engine('sqlite:///freebies.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    # Example: Print all developers and their freebies
    devs = session.query(Dev).all()
    for dev in devs:
        print(f"{dev.name} received:")
        for freebie in dev.freebies:
            print(f"  - {freebie.item_name} (${freebie.value}) from {freebie.company.name}")
