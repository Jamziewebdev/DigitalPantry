from sqlalchemy.orm import sessionmaker
from models import Base, engine, Item, Category

# Initialize DB session
Session = sessionmaker(bind=engine)
session = Session()


def add_item(name, quantity, unit, categories):
    try:
        new_item = Item(name=name, quantity=quantity, unit=unit)
        for category_name in categories:
            category = session.query(Category).filter_by(name=category_name).first()
            if not category:
                category = Category(name=category_name)
                session.add(category)
            new_item.categories.append(category)

        session.add(new_item)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e


def get_items():
    return session.query(Item).all()


def update_item(item_id, name, quantity, unit, categories):
    try:
        item = session.query(Item).filter_by(id=item_id).first()
        if not item:
            raise ValueError(f"Item with ID {item_id} not found.")

        item.name = name
        item.quantity = quantity
        item.unit = unit
        item.categories.clear()

        for category_name in categories:
            category = session.query(Category).filter_by(name=category_name).first()
            if not category:
                category = Category(name=category_name)
                session.add(category)
            item.categories.append(category)

        session.commit()
    except Exception as e:
        session.rollback()
        raise e


def delete_item_from_db(item_id):
    try:
        item = session.query(Item).filter_by(id=item_id).first()
        if not item:
            raise ValueError(f"Item with ID {item_id} not found.")
        session.delete(item)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
