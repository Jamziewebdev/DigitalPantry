from sqlalchemy.orm import sessionmaker
from models import Base, engine, Item, Category

# Initialize DB session
Session = sessionmaker(bind=engine)
session = Session()


def add_item(name, quantity, unit, categories):
    try:
        existing_item = session.query(Item).filter_by(name=name).first()
        if existing_item:
            # If user inputs dupicate, amount is added to original item
            existing_item.quantity += quantity
            session.commit()
            return

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

def get_items_by_category(category_name):
    return session.query(Item).join(Item.categories).filter(Category.name == category_name).all()


def get_all_categories():
    return session.query(Category).all()


def get_item_by_id(item_id):
    return session.query(Item).filter_by(id=item_id).first()


def update_item(item_id, name, quantity, unit, categories):
    try:
        item = session.query(Item).filter_by(id=item_id).first()
        if not item:
            raise ValueError("Item not found")

        item.name = name
        item.quantity = quantity
        item.unit = unit
        item.categories = []

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
        if item:
            session.delete(item)
            session.commit()
    except Exception as e:
        session.rollback()
        raise e
