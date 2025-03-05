from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Dict, Any, Optional
from app.models.item import Item
from app.schemas.item import ItemCreate

def update_item(db: Session, item_id: int, item: ItemCreate) -> Optional[Item]:
    """
    Update an existing item in the database using MySQL syntax.
    
    Args:
        db (Session): Database session
        item_id (int): ID of the item to update
        item (ItemCreate): New item data
        
    Returns:
        Optional[Item]: The updated item or None if not found
    """
    # Check if the item exists
    check_query = text("SELECT 1 FROM items WHERE id = :item_id")
    result = db.execute(check_query, {"item_id": item_id})
    if result.fetchone() is None:
        return None
    
    # Update the item
    query = text("""
    UPDATE items 
    SET title = :title, description = :description, completed = :completed 
    WHERE id = :item_id
    """)
    
    db.execute(
        query, 
        {
            "item_id": item_id,
            "title": item.title,
            "description": item.description,
            "completed": item.completed
        }
    )
    db.commit()
    
    # Get the updated item
    updated_query = text("""
    SELECT id, title, description, completed 
    FROM items 
    WHERE id = :item_id
    """)
    
    result = db.execute(updated_query, {"item_id": item_id}).fetchone()
    
    if result is None:
        return None
        
    # Convert row to Item model
    updated_item = Item()
    updated_item.id = result[0]
    updated_item.title = result[1]
    updated_item.description = result[2]
    updated_item.completed = result[3]
    
    return updated_item