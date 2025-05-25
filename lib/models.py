class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())

    freebies = relationship("Freebie", backref="company")

    @property
    def devs(self):
        return list({freebie.dev for freebie in self.freebies})

    def __repr__(self):
        return f'<Company {self.name}>'


class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name = Column(String())

    freebies = relationship("Freebie", backref="dev")

    @property
    def companies(self):
        return list({freebie.company for freebie in self.freebies})

    def __repr__(self):
        return f'<Dev {self.name}>'
