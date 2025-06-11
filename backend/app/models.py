from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class ChatMessage(BaseModel):
    message: str
    max_tokens: Optional[int] = 1000
    session_id: Optional[str] = None
    current_page: Optional[str] = None
    current_product_id: Optional[int] = None
    context_data: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    response: str
    timestamp: datetime
    tokens_used: Optional[int] = None
    intent: Optional[str] = None
    entities: Optional[Dict[str, Any]] = {}
    products: Optional[List[Dict[str, Any]]] = []
    cart_total: Optional[float] = None
    cart_action: Optional[Dict[str, Any]] = None  # Para acciones del carrito

class ConversationHistory(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime

class HealthCheck(BaseModel):
    status: str
    timestamp: datetime
    version: str

# E-commerce Models
class UserBase(BaseModel):
    username: str
    email: str
    full_name: str
    phone: Optional[str] = None
    address: Optional[str] = None

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    original_price: Optional[float] = None
    sku: str
    stock_quantity: int
    brand: str
    model: str
    specifications: Optional[str] = None
    image_url: str
    category_id: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    rating: float
    review_count: int
    is_active: bool
    is_featured: bool
    is_new: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class CategoryBase(BaseModel):
    name: str
    description: str
    slug: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class CartItemBase(BaseModel):
    product_id: int
    quantity: int

class CartItem(CartItemBase):
    product: Product
    
    class Config:
        from_attributes = True

class Cart(BaseModel):
    id: int
    user_id: Optional[int] = None
    session_id: Optional[str] = None
    total_amount: float
    items: List[CartItem] = []
    updated_at: datetime
    
    class Config:
        from_attributes = True

class AddToCartRequest(BaseModel):
    product_id: int
    quantity: int = 1
    session_id: Optional[str] = None

class RemoveFromCartRequest(BaseModel):
    product_id: int
    session_id: Optional[str] = None

class OrderBase(BaseModel):
    shipping_address: str
    payment_method: str

class Order(OrderBase):
    id: int
    order_number: str
    user_id: int
    status: str
    total_amount: float
    payment_status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# Enhanced Chat Models
class ChatMessageWithContext(ChatMessage):
    session_id: Optional[str] = None
    user_id: Optional[int] = None
    intent: Optional[str] = None

class ChatResponseWithActions(ChatResponse):
    actions: Optional[List[dict]] = []  # Actions like add_to_cart, show_products, etc.
    products: Optional[List[Product]] = []  # Recommended products
    cart_updated: Optional[bool] = False

# Response Models para API
class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    original_price: Optional[float] = None
    sku: str
    stock_quantity: int
    brand: str
    model: str
    specifications: Optional[str] = None
    image_url: str
    category_id: int
    rating: float
    review_count: int
    is_active: bool
    is_featured: bool
    is_new: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class CategoryResponse(BaseModel):
    id: int
    name: str
    description: str
    slug: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class CartItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    product: ProductResponse
    
    class Config:
        from_attributes = True

class CartResponse(BaseModel):
    items: List[CartItemResponse]
    total: float
    item_count: int

class CartItemCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int = 1

class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: float
    total_price: float
    product: ProductResponse
    
    class Config:
        from_attributes = True

class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_amount: float
    status: str
    shipping_address: Optional[str]
    payment_method: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    order_items: List[OrderItemResponse]
    
    class Config:
        from_attributes = True

class OrderCreate(BaseModel):
    user_id: int
    shipping_address: str
    payment_method: str
