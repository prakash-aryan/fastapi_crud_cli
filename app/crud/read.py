from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional
from app.models.item import Item

def get_item(db: Session, item_id: int) -> Optional[Item]:
    """
    Get a single item by ID using MySQL syntax.
    
    Args:
        db (Session): Database session
        item_id (int): ID of the item to retrieve
        
    Returns:
        Optional[Item]: The found item or None if not found
    """
    query = text("""
    SELECT id, title, description, completed 
    FROM items 
    WHERE id = :item_id
    """)
    
    result = db.execute(query, {"item_id": item_id}).fetchone()
    
    if result is None:
        return None
    
    # Convert row to Item model
    item = Item()
    item.id = result[0]
    item.title = result[1]
    item.description = result[2]
    item.completed = result[3]
    
    return item

def get_items(db: Session, skip: int = 0, limit: int = 100) -> List[Item]:
    """
    Get multiple items with pagination using MySQL syntax.
    
    Args:
        db (Session): Database session
        skip (int): Number of records to skip (for pagination)
        limit (int): Maximum number of records to return
        
    Returns:
        List[Item]: List of found items
    """
    query = text("""
    SELECT id, title, description, completed 
    FROM items 
    LIMIT :limit OFFSET :skip
    """)
    
    result = db.execute(query, {"skip": skip, "limit": limit})
    
    items = []
    for row in result:
        item = Item()
        item.id = row[0]
        item.title = row[1]
        item.description = row[2]
        item.completed = row[3]
        items.append(item)
    
    return items