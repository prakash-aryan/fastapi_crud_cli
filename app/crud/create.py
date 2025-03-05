from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.item import Item
from app.schemas.item import ItemCreate

def create_item(db: Session, item: ItemCreate):
    """
    Create a new item in the database using MySQL syntax.
    
    Args:
        db (Session): Database session
        item (ItemCreate): Item data to create
        
    Returns:
        Item: The created item
    """
    # Using raw SQL
    query = text("""
    INSERT INTO items (title, description, completed) 
    VALUES (:title, :description, :completed)
    """)
    
    result = db.execute(
        query, 
        {
            "title": item.title,
            "description": item.description,
            "completed": item.completed
        }
    )
    db.commit()
    
    # Get the last inserted ID
    last_id = db.execute(text("SELECT LAST_INSERT_ID()")).scalar()
    
    # Get the created item
    created_item = db.query(Item).filter(Item.id == last_id).first()
    
    return created_item