# Let's import the tools we need, like getting ingredients before baking a cake!
from fastapi import FastAPI, HTTPException  # FastAPI = a tool to build a web server (like a restaurant)
from fastapi.middleware.cors import CORSMiddleware  # This helps different websites talk to each other safely
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float  # SQLAlchemy = tool for storing data in a filing cabinet
from sqlalchemy.ext.declarative import declarative_base  # This helps us describe what our data looks like
from sqlalchemy.orm import sessionmaker  # This helps us talk to the database (the filing cabinet)
from pydantic import BaseModel  # This checks that we get the right type of information
from datetime import datetime  # This helps us work with dates and times
import os  # This helps us work with the computer's files and folders

# Where do we want to store our data? Like choosing a filing cabinet!
DATABASE_URL = "sqlite:///./inventory.db"

# Open the filing cabinet and get ready to use it
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# This describes what each inventory item should look like
# Think of it like a template or form that everyone fills out the same way!
class Item(Base):
    __tablename__ = "items"  # The name of our filing cabinet drawer
    id = Column(Integer, primary_key=True, index=True)  # Each item gets a special number (like a receipt)
    name = Column(String, index=True)  # Name of the item
    description = Column(String)  # Description of the item
    quantity = Column(Float)  # Current quantity
    category = Column(String)  # Category (e.g., surgical instruments, medications)
    location = Column(String, default="Quirófano Ceye")  # Location in the operating room
    last_updated = Column(DateTime, default=datetime.utcnow)  # When was this item last updated?
    updated_by = Column(String)  # Who updated it (shift or user)

# Actually create the filing cabinet drawer in our computer
Base.metadata.create_all(bind=engine)

# Add some sample data if the database is empty
def create_sample_data():
    db = SessionLocal()
    if db.query(Item).count() == 0:
        sample_items = [
            Item(name="Guantes quirúrgicos", description="Guantes estériles tamaño M", quantity=50.0, category="Materiales desechables", location="Quirófano Ceye", updated_by="Sistema"),
            Item(name="Bisturí", description="Bisturí desechable #10", quantity=20.0, category="Instrumentos quirúrgicos", location="Quirófano Ceye", updated_by="Sistema"),
            Item(name="Anestesia local", description="Lidocaína 2% - 10ml", quantity=15.0, category="Medicamentos", location="Quirófano Ceye", updated_by="Sistema"),
            Item(name="Máscara quirúrgica", description="Máscaras N95", quantity=100.0, category="Materiales desechables", location="Quirófano Ceye", updated_by="Sistema"),
            Item(name="Sutura", description="Sutura absorbible 3-0", quantity=25.0, category="Instrumentos quirúrgicos", location="Quirófano Ceye", updated_by="Sistema"),
        ]
        for item in sample_items:
            db.add(item)
        db.commit()
    db.close()

create_sample_data()

# Create the web server (like opening a restaurant)
app = FastAPI()

# CORS = "Cross-Origin Resource Sharing" = Allow other websites to order from our restaurant
# This is like saying: "Anyone can call us and we'll serve them!"
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # * means "everyone is allowed"
    allow_credentials=True,  # Allow them to send cookies
    allow_methods=["*"],  # Allow all types of requests (GET, POST, etc.)
    allow_headers=["*"],  # Allow any information in the request
)

# This describes what information we need to CREATE a new item
# Like a recipe that shows what ingredients you must add
class ItemCreate(BaseModel):
    name: str  # Name of the item
    description: str  # Description
    quantity: float  # Initial quantity
    category: str  # Category
    location: str = "Quirófano Ceye"  # Location
    updated_by: str = "Sistema"  # Who is adding it

# This describes what information we need to UPDATE an item
class ItemUpdate(BaseModel):
    quantity: float  # New quantity
    updated_by: str  # Who is updating it

# This describes what information we SEND BACK when you ask for an item
# Like describing what a finished cake looks like when you ask for it
class ItemResponse(BaseModel):
    id: int  # The receipt number
    name: str  # Name
    description: str  # Description
    quantity: float  # Quantity
    category: str  # Category
    location: str  # Location
    last_updated: datetime  # Last updated
    updated_by: str  # Updated by

    class Config:
        from_attributes = True  # This lets us convert database stuff to this format

# ========== RESTAURANT MENU (ENDPOINTS) ==========
# These are like the menu items you can order from our restaurant!

# ENDPOINT 1: Get all inventory items
@app.get("/items", response_model=list[ItemResponse])
def get_items():
    """
    GET /items = Get all items from the inventory
    The server sends back: a list of all items
    """
    db = SessionLocal()  # Open the filing cabinet
    items = db.query(Item).order_by(Item.name).all()  # Get all items ordered by name
    db.close()  # Close the filing cabinet
    return items  # Send the list back

# ENDPOINT 2: Create a new inventory item
@app.post("/items", response_model=ItemResponse)
def create_item(item: ItemCreate):
    """
    POST /items = Create a new item in the inventory
    The client sends: item details
    The server sends back: the created item
    """
    db = SessionLocal()  # Open the filing cabinet
    db_item = Item(
        name=item.name,
        description=item.description,
        quantity=item.quantity,
        category=item.category,
        location=item.location,
        updated_by=item.updated_by
    )  # Create a new item
    db.add(db_item)  # Put it in the filing cabinet
    db.commit()  # Save it permanently
    db.refresh(db_item)  # Get the fresh copy with the id
    db.close()  # Close the filing cabinet
    return db_item  # Send it back

# ENDPOINT 3: Update an item's quantity
@app.put("/items/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, update: ItemUpdate):
    """
    PUT /items/{item_id} = Update an item's quantity
    The client sends: new quantity and who is updating
    The server sends back: the updated item
    """
    db = SessionLocal()  # Open the filing cabinet
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        db.close()
        raise HTTPException(status_code=404, detail="Item not found")
    
    db_item.quantity = update.quantity
    db_item.last_updated = datetime.utcnow()
    db_item.updated_by = update.updated_by
    db.commit()  # Save the changes
    db.refresh(db_item)
    db.close()  # Close the filing cabinet
    return db_item  # Send it back

# ENDPOINT 4: Delete an item
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    """
    DELETE /items/{item_id} = Remove an item from inventory
    """
    db = SessionLocal()
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        db.close()
        raise HTTPException(status_code=404, detail="Item not found")
    
    db.delete(db_item)
    db.commit()
    db.close()
    return {"message": "Item deleted"}

# ENDPOINT 5: Check if the server is alive (like a heartbeat check)
@app.get("/health")
def health():
    """
    GET /health = Is the server working?
    The server sends back: {"status": "ok"} = "Yes, I'm alive and ready to help!"
    """
    return {"status": "ok"}
