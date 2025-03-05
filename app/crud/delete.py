from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional

def delete_item(db: Session, item_id: int) -> bool:
    """
    Delete an item from the database using MySQL syntax.
    
    Args:
        db (Session): Database session
        item_id (int): ID of the item to delete
        
    Returns:
        bool: True if the item was deleted, False if the item was not found
    """
    # Check if the item exists
    check_query = text("SELECT 1 FROM items WHERE id = :item_id")
    result = db.execute(check_query, {"item_id": item_id})
    if result.fetchone() is None:
        return False
    
    # Delete the item
    query = text("DELETE FROM items WHERE id = :item_id")
    db.execute(query, {"item_id": item_id})
    db.commit()
    
    return True