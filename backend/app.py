# Let's import the tools we need, like getting ingredients before baking a cake!
from fastapi import FastAPI, HTTPException  # FastAPI = a tool to build a web server (like a restaurant)
from fastapi.middleware.cors import CORSMiddleware  # This helps different websites talk to each other safely
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, ForeignKey  # SQLAlchemy = tool for storing data in a filing cabinet
from sqlalchemy.ext.declarative import declarative_base  # This helps us describe what our data looks like
from sqlalchemy.orm import sessionmaker, relationship  # This helps us talk to the database (the filing cabinet)
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
    
    # Relationship to counts and audits
    counts = relationship("Count", back_populates="item")
    audits = relationship("AuditLog", back_populates="item")

# User model for tracking who does what
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    full_name = Column(String)
    role = Column(String, default="enfermera")  # enfermera, supervisor, admin
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Integer, default=1)
    
    # Relationships
    counts = relationship("Count", back_populates="user")
    audits = relationship("AuditLog", back_populates="user")

# Count model to track inventory counts
class Count(Base):
    __tablename__ = "counts"
    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    quantity_on_hand = Column(Float)  # Actual quantity found during count
    expected_quantity = Column(Float)  # Expected quantity before count
    discrepancy = Column(Float)  # quantity_on_hand - expected_quantity
    count_type = Column(String, default="gas")  # "gas" o "vapor"
    count_date = Column(DateTime, default=datetime.utcnow)
    notes = Column(String, nullable=True)
    
    # Relationships
    item = relationship("Item", back_populates="counts")
    user = relationship("User", back_populates="counts")

# Audit log for tracking all changes
class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String)  # "created", "updated", "counted", "deleted"
    old_quantity = Column(Float, nullable=True)
    new_quantity = Column(Float, nullable=True)
    action_date = Column(DateTime, default=datetime.utcnow)
    notes = Column(String, nullable=True)
    
    # Relationships
    item = relationship("Item", back_populates="audits")
    user = relationship("User", back_populates="audits")

# Actually create the filing cabinet drawer in our computer
Base.metadata.create_all(bind=engine)

# Add some sample data if the database is empty
def create_sample_data():
    db = SessionLocal()
    
    # Create sample users if they don't exist
    if db.query(User).count() == 0:
        sample_users = [
            User(username="maria", full_name="María García", role="enfermera"),
            User(username="carlos", full_name="Carlos López", role="enfermera"),
            User(username="ana", full_name="Ana Martínez", role="supervisor"),
            User(username="admin", full_name="Administrador", role="admin"),
        ]
        for user in sample_users:
            db.add(user)
        db.commit()
    
    # Create sample items if they don't exist
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

# ===== USER MODELS =====
class UserCreate(BaseModel):
    username: str
    full_name: str
    role: str = "enfermera"

class UserResponse(BaseModel):
    id: int
    username: str
    full_name: str
    role: str
    created_at: datetime
    is_active: int

    class Config:
        from_attributes = True

# ===== COUNT MODELS =====
class CountCreate(BaseModel):
    item_id: int
    user_id: int
    quantity_on_hand: float
    expected_quantity: float
    count_type: str = "gas"
    notes: str = None

class CountResponse(BaseModel):
    id: int
    item_id: int
    user_id: int
    quantity_on_hand: float
    expected_quantity: float
    discrepancy: float
    count_type: str
    count_date: datetime
    notes: str
    item: ItemResponse
    user: UserResponse

    class Config:
        from_attributes = True

# ===== AUDIT LOG MODELS =====
class AuditLogResponse(BaseModel):
    id: int
    item_id: int
    user_id: int
    action: str
    old_quantity: float
    new_quantity: float
    action_date: datetime
    notes: str
    item: ItemResponse
    user: UserResponse

    class Config:
        from_attributes = True

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
    
    # Create audit log for the new item
    audit = AuditLog(
        item_id=db_item.id,
        action="created",
        new_quantity=item.quantity,
        notes=f"New item '{item.name}' added to inventory"
    )
    db.add(audit)
    db.commit()
    
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
    
    old_quantity = db_item.quantity
    db_item.quantity = update.quantity
    db_item.last_updated = datetime.utcnow()
    db_item.updated_by = update.updated_by
    db.commit()  # Save the changes
    
    # Create audit log for this update
    audit = AuditLog(
        item_id=item_id,
        action="updated",
        old_quantity=old_quantity,
        new_quantity=update.quantity,
        notes=f"Quantity updated from {old_quantity} to {update.quantity}"
    )
    db.add(audit)
    db.commit()
    
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
    
    # Create audit log before deleting
    audit = AuditLog(
        item_id=item_id,
        action="deleted",
        old_quantity=db_item.quantity,
        notes=f"Item '{db_item.name}' deleted from inventory"
    )
    db.add(audit)
    
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

# ========== USER ENDPOINTS ==========

# ENDPOINT 6: Get all users
@app.get("/users", response_model=list[UserResponse])
def get_users():
    """
    GET /users = Get all users in the system
    """
    db = SessionLocal()
    users = db.query(User).filter(User.is_active == 1).order_by(User.full_name).all()
    db.close()
    return users

# ENDPOINT 7: Create a new user
@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate):
    """
    POST /users = Create a new user
    """
    db = SessionLocal()
    db_user = User(
        username=user.username,
        full_name=user.full_name,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db.close()
    return db_user

# ENDPOINT 8: Get user by ID
@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    """
    GET /users/{user_id} = Get a specific user
    """
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    db.close()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# ========== COUNT ENDPOINTS ==========

# ENDPOINT 9: Create a count record
@app.post("/counts", response_model=CountResponse)
def create_count(count: CountCreate):
    """
    POST /counts = Record an inventory count
    Calculates discrepancy automatically
    """
    db = SessionLocal()
    
    # Get the item to verify it exists
    item = db.query(Item).filter(Item.id == count.item_id).first()
    if not item:
        db.close()
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Calculate discrepancy
    discrepancy = count.quantity_on_hand - count.expected_quantity
    
    # Create the count record
    db_count = Count(
        item_id=count.item_id,
        user_id=count.user_id,
        quantity_on_hand=count.quantity_on_hand,
        expected_quantity=count.expected_quantity,
        discrepancy=discrepancy,
        count_type=count.count_type,
        notes=count.notes
    )
    
    db.add(db_count)
    db.commit()
    db.refresh(db_count)
    
    # Also create an audit log entry
    audit = AuditLog(
        item_id=count.item_id,
        user_id=count.user_id,
        action="counted",
        old_quantity=count.expected_quantity,
        new_quantity=count.quantity_on_hand,
        notes=f"Count discrepancy: {discrepancy}"
    )
    db.add(audit)
    db.commit()
    
    db.close()
    return db_count

# ENDPOINT 10: Get all counts
@app.get("/counts", response_model=list[CountResponse])
def get_counts(item_id: int = None, user_id: int = None):
    """
    GET /counts = Get all count records
    Optional filters: item_id, user_id
    """
    db = SessionLocal()
    query = db.query(Count)
    
    if item_id:
        query = query.filter(Count.item_id == item_id)
    if user_id:
        query = query.filter(Count.user_id == user_id)
    
    counts = query.order_by(Count.count_date.desc()).all()
    db.close()
    return counts

# ENDPOINT 11: Get counts for a specific item
@app.get("/items/{item_id}/counts", response_model=list[CountResponse])
def get_item_counts(item_id: int):
    """
    GET /items/{item_id}/counts = Get all count records for an item
    """
    db = SessionLocal()
    counts = db.query(Count).filter(Count.item_id == item_id).order_by(Count.count_date.desc()).all()
    db.close()
    return counts

# ========== AUDIT LOG ENDPOINTS ==========

# ENDPOINT 12: Get audit logs
@app.get("/audit-logs", response_model=list[AuditLogResponse])
def get_audit_logs(item_id: int = None, user_id: int = None, action: str = None):
    """
    GET /audit-logs = Get audit log records
    Optional filters: item_id, user_id, action
    """
    db = SessionLocal()
    query = db.query(AuditLog)
    
    if item_id:
        query = query.filter(AuditLog.item_id == item_id)
    if user_id:
        query = query.filter(AuditLog.user_id == user_id)
    if action:
        query = query.filter(AuditLog.action == action)
    
    logs = query.order_by(AuditLog.action_date.desc()).all()
    db.close()
    return logs

# ENDPOINT 13: Get audit logs for a specific item
@app.get("/items/{item_id}/audit-logs", response_model=list[AuditLogResponse])
def get_item_audit_logs(item_id: int):
    """
    GET /items/{item_id}/audit-logs = Get audit history for an item
    """
    db = SessionLocal()
    logs = db.query(AuditLog).filter(AuditLog.item_id == item_id).order_by(AuditLog.action_date.desc()).all()
    db.close()
    return logs
