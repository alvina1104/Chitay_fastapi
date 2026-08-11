from pydantic import BaseModel,EmailStr
from typing import Optional
from .models import RoleChoices,StatusChoices
from datetime import datetime,date


class UserProfileInputSchema(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    phone: str
    password: str
    age: Optional[int]
    user_image: Optional[str]
    role: RoleChoices
    date_register: date


class UserProfileOutSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    phone: str
    password: str
    age: Optional[int]
    user_image: Optional[str]
    role: RoleChoices
    date_register: date


class UserLoginSchema(BaseModel):
    username: str
    password: str


class CatalogInputSchema(BaseModel):
    catalog_image: str
    catalog_name: str


class CatalogOutSchema(BaseModel):
    id: int
    catalog_image: str
    catalog_name: str


class SubCatalogInputSchema(BaseModel):
    catalog_id: int
    subcatalog_name: str


class SubCatalogOutSchema(BaseModel):
    id: int
    catalog_id: int
    subcatalog_name: str


class TypeCatalogInputSchema(BaseModel):
    subcatalog_id: int
    typecatalog_name: str


class TypeCatalogOutSchema(BaseModel):
    id: int
    subcatalog_id: int
    typecatalog_name: str


class AddressInputSchema(BaseModel):
    title: str
    location: str


class AddressOutSchema(BaseModel):
    id: int
    title: str
    location: str


class AuthorInputSchema(BaseModel):
    author_name: str


class AuthorOutSchema(BaseModel):
    id: int
    author_name: str


class BookInputSchema(BaseModel):
    type_catalog_id: int
    author_id: int
    book_name: str
    stock_quantity: int
    price: int
    description: str
    cover_type: Optional[str]
    pages: Optional[int]
    size: str
    publisher: Optional[str]
    publisher_brand: str
    series: Optional[str]
    age_limit: Optional[str]
    isbn: Optional[int]
    tirage: Optional[int]
    id_product: int
    genre: Optional[str]
    theme: str
    textile: Optional[str]


class BookOutSchema(BaseModel):
    id: int
    type_catalog_id: int
    author_id: int
    book_name: str
    stock_quantity: int
    price: int
    description: str
    cover_type: Optional[str]
    pages: Optional[int]
    size: str
    publisher: Optional[str]
    publisher_brand: str
    series: Optional[str]
    age_limit: Optional[str]
    isbn: Optional[int]
    tirage: Optional[int]
    id_product: int
    genre: Optional[str]
    theme: str
    textile: Optional[str]


class BookImageInputSchema(BaseModel):
    book_id: int
    book_image: str


class BookImageOutSchema(BaseModel):
    id: int
    book_id: int
    book_image: str


class ExcerptInputSchema(BaseModel):
    book_id: int
    excerpt_name: str
    excerpt_file: str


class ExcerptOutSchema(BaseModel):
    id: int
    book_id: int
    excerpt_name: str
    excerpt_file: str


class OrderInputSchema(BaseModel):
    user_id: int
    created_at: datetime
    updated_at: datetime
    status: StatusChoices
    address: str
    total_price: int
    is_paid: bool


class OrderOutSchema(BaseModel):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    status: StatusChoices
    address: str
    total_price: int
    is_paid: bool


class OrderItemInputSchema(BaseModel):
    book_id: int
    order_id: int
    quantity: int
    price: int


class OrderItemOutSchema(BaseModel):
    id: int
    book_id: int
    order_id: int
    quantity: int
    price: int


class ReviewInputSchema(BaseModel):
    user_id: int
    book_id: int
    comment: str
    stars: int
    created_date: date


class ReviewOutSchema(BaseModel):
    user_id: int
    book_id: int
    comment: str
    stars: int
    created_date: date


class ReviewLikeInputSchema(BaseModel):
    user_id: int
    review_id: int
    like: bool


class ReviewLikeOutSchema(BaseModel):
    id: int
    user_id: int
    review_id: int
    like: bool


class CartInputSchema(BaseModel):
    user_id: int


class CartOutSchema(BaseModel):
    id: int
    user_id: int


class CartItemInputSchema(BaseModel):
    book_id: int
    cart_id: int
    quantity: int


class CartItemOutSchema(BaseModel):
    book_id: int
    cart_id: int
    quantity: int


class FavoriteItemInputSchema(BaseModel):
    book_id: int
    user_id: int
    added_at: datetime
    price_at_adding: int


class FavoriteItemOutSchema(BaseModel):
    id: int
    book_id: int
    user_id: int
    added_at: datetime
    price_at_adding: int

