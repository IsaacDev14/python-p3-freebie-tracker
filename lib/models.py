from sqlalchemy import Column, Integer, String, ForeignKey, MetaData
from sqlalchemy.orm import declarative_base, relationship

# Naming convention for Alembic migrations
convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    founding_year = Column(Integer)

    freebies = relationship("Freebie", backref="company")

    @property
    def devs(self):
        # Return unique devs who got freebies from this company
        return list({freebie.dev for freebie in self.freebies})

    def give_freebie(self, dev, item_name, value):
        """Create a new freebie for a dev from this company"""
        new_freebie = Freebie(item_name=item_name, value=value, company=self, dev=dev)
        return new_freebie

    @classmethod
    def oldest_company(cls, session):
        """Return the company with the smallest founding_year"""
        return session.query(cls).order_by(cls.founding_year).first()

    def __repr__(self):
        return f"<Company {self.name}>"

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    freebies = relationship("Freebie", backref="dev")

    @property
    def companies(self):
        # Return unique companies who gave freebies to this dev
        return list({freebie.company for freebie in self.freebies})

    def received_one(self, item_name):
        """Return True if dev has received a freebie with this item_name"""
        return any(freebie.item_name == item_name for freebie in self.freebies)

    def give_away(self, new_dev, freebie):
        """
        Transfer ownership of a freebie to another dev.
        Returns True if successful, False if freebie does not belong to self.
        """
        if freebie in self.freebies:
            freebie.dev = new_dev
            return True
        return False

    def __repr__(self):
        return f"<Dev {self.name}>"

class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer, primary_key=True)
    item_name = Column(String)
    value = Column(Integer)

    dev_id = Column(Integer, ForeignKey('devs.id'))
    company_id = Column(Integer, ForeignKey('companies.id'))

    def print_details(self):
        return f"{self.dev.name} owns a {self.item_name} from {self.company.name}"

    def __repr__(self):
        return f"<Freebie {self.item_name} (${self.value})>"
