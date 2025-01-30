from sqlalchemy import create_engine, Column, Integer, String, Float, Table, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# Association table to enable multiple category choice for items
item_category_association = Table(
    'item_category', Base.metadata,
    Column('item_id', Integer, ForeignKey('items.id')),
    Column('category_id', Integer, ForeignKey('categories.id'))
)


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    items = relationship('Item', secondary=item_category_association, back_populates='categories')


class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    quantity = Column(Float, nullable=False)
    unit = Column(String, nullable=False)
    categories = relationship('Category', secondary=item_category_association, back_populates='items')


# Create SQLite DB
DATABASE_URL = 'sqlite:///pantry.db'
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
