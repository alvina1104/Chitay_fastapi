

from .db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer,String, Enum, Date, Text, ForeignKey, DateTime, Boolean
from enum import Enum as PyEnum
from datetime import date, datetime
from typing import List, Optional

class RoleChoices(str, PyEnum):
    admin = "admin"
    user = "user"

class StatusChoices(str, PyEnum):
    pending = 'pending'
    processing = 'processing'
    shipped = 'shipped'
    delivered = 'delivered'
    cancelled = 'cancelled'


class UserProfile(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    username: Mapped[str] = mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    phone: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    age: Mapped[Optional[int]] = mapped_column(Integer,nullable=True)
    user_image: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    role: Mapped[RoleChoices] = mapped_column(Enum(RoleChoices), default=RoleChoices.user)
    date_register: Mapped[Date] = mapped_column(Date, default=date.today)

    orders: Mapped[List['Order']] = relationship(back_populates='user', cascade='all, delete-orphan')
    reviews: Mapped[List['Review']] = relationship(back_populates='users', cascade='all, delete-orphan')
    user_relike: Mapped[List['ReviewLike']] = relationship(back_populates='relike_u', cascade='all, delete-orphan')
    user_cart: Mapped[List['Cart']] = relationship(back_populates='user_c',cascade='all, delete-orphan')
    favorites: Mapped[List['FavoriteItem']] = relationship(back_populates='users_fav', cascade='all, delete-orphan')
    user_token: Mapped[List['RefreshToken']] = relationship(back_populates='token_user', cascade='all, delete-orphan')

    def __str__(self):
        return self.username


class RefreshToken(Base):
    __tablename__ = 'refresh_token'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    token_user: Mapped['UserProfile'] = relationship(UserProfile, back_populates='user_token')
    token: Mapped[str] = mapped_column(String)
    created_date: Mapped[DateTime] = mapped_column(DateTime, default=datetime.utcnow)


class Catalog(Base):
    __tablename__ = 'catalog'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    catalog_image: Mapped[str] = mapped_column(String)
    catalog_name: Mapped[str] = mapped_column(String)

    subcatalog: Mapped[List['SubCatalog']] = relationship(back_populates='catalog',cascade='all, delete-orphan')

    def __str__(self):
        return self.catalog_name


class SubCatalog(Base):
    __tablename__ = 'subcatalog'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    subcatalog_name: Mapped[str] = mapped_column(String)

    catalog_id: Mapped[int] = mapped_column(ForeignKey('catalog.id'))
    catalog: Mapped[Catalog] = relationship(back_populates='subcatalog')

    typecatalog: Mapped[List['TypeCatalog']] = relationship(back_populates='subcatalog', cascade='all, delete-orphan')

    def __str__(self):
        return self.subcatalog_name


class TypeCatalog(Base):
    __tablename__ = 'typecatalog'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    typecatalog_name: Mapped[str] = mapped_column(String)

    subcatalog_id: Mapped[int] = mapped_column(ForeignKey('subcatalog.id'))
    subcatalog: Mapped[SubCatalog] = relationship(back_populates='typecatalog')

    books: Mapped[List['Book']] = relationship(back_populates='type_catalog', cascade='all, delete-orphan')

    def __str__(self):
        return self.typecatalog_name


class Address(Base):
    __tablename__ = 'address'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(150))
    location: Mapped[str] = mapped_column(String)


class Author(Base):
    __tablename__ = 'author'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    author_name: Mapped[str] = mapped_column(String(100))

    books_auth: Mapped[List['Book']] = relationship(back_populates='author', cascade='all, delete-orphan')


class Book(Base):
    __tablename__ = 'book'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    book_name: Mapped[str] = mapped_column(String(100))
    stock_quantity: Mapped[int] = mapped_column(Integer)  # Кампадагы саны
    price: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(Text)
    cover_type: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    pages: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    size: Mapped[str] = mapped_column(String)
    publisher: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    publisher_brand: Mapped[str] = mapped_column(String)
    series: Mapped[Optional[str]] = mapped_column(String(100),nullable=True)
    age_limit: Mapped[Optional[str]] = mapped_column(String(5), nullable=True, default="18+")
    isbn: Mapped[str] = mapped_column(String(20))
    tirage: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    id_product: Mapped[int] = mapped_column(Integer)
    genre: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    theme: Mapped[str] = mapped_column(String(100))
    textile: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    type_catalog_id: Mapped[int] = mapped_column(ForeignKey('typecatalog.id'))
    author_id: Mapped[int] = mapped_column(ForeignKey('author.id'))

    author: Mapped[Author] = relationship(Author, back_populates='books_auth')
    type_catalog: Mapped[TypeCatalog] = relationship(back_populates='books')

    book_image: Mapped[List['BookImage']] = relationship(back_populates='book', cascade='all, delete-orphan')
    excerpts: Mapped[List['Excerpt']] = relationship(back_populates='book_field', cascade='all, delete-orphan')
    order_item: Mapped[List['OrderItem']] = relationship(back_populates='book_orit', cascade='all, delete-orphan')
    reviews_b: Mapped[List['Review']] = relationship(back_populates='books_r', cascade='all, delete-orphan')
    items: Mapped[List['CartItem']] = relationship(back_populates='item', cascade='all, delete-orphan')
    favorite: Mapped[List['FavoriteItem']] = relationship(back_populates='book_fav', cascade='all, delete-orphan')



class BookImage(Base):
    __tablename__ = 'book_image'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    book_image: Mapped[str] = mapped_column(String)

    book_id: Mapped[int] = mapped_column(ForeignKey('book.id'))
    book: Mapped[Book] = relationship(back_populates='book_image')



class Excerpt(Base):
    __tablename__ = 'excerpt'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    excerpt_name: Mapped[str] = mapped_column(String(100))
    excerpt_file: Mapped[str] = mapped_column(String)

    book_id: Mapped[int] = mapped_column(ForeignKey('book.id'))
    book_field: Mapped[Book] = relationship(Book, back_populates='excerpts')


class Order(Base):
    __tablename__ = 'order'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime)
    updated_at: Mapped[datetime] = mapped_column(DateTime)
    status: Mapped[StatusChoices] = mapped_column(Enum(StatusChoices), default=StatusChoices.pending)
    address: Mapped[str] = mapped_column(String)
    total_price: Mapped[int] = mapped_column(Integer)
    is_paid: Mapped[bool] = mapped_column(Boolean)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped[UserProfile] = relationship(back_populates='orders')

    order_items: Mapped[List['OrderItem']] = relationship(back_populates='order', cascade='all, delete-orphan')


class OrderItem(Base):
    __tablename__ = 'order_item'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    price: Mapped[int] = mapped_column(Integer)

    order_id: Mapped[int] = mapped_column(ForeignKey('order.id'))
    order: Mapped[Order] = relationship(Order, back_populates='order_items')

    book_id: Mapped[int] = mapped_column(ForeignKey('book.id'))
    book_orit: Mapped[Book] = relationship(Book, back_populates='order_item')



class Review(Base):
    __tablename__ = 'review'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    comment: Mapped[str] = mapped_column(Text)
    stars: Mapped[int] = mapped_column(Integer)
    created_date: Mapped[date] = mapped_column(Date)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    users: Mapped[UserProfile] = relationship(back_populates='reviews')

    book_id: Mapped[int] = mapped_column(ForeignKey('book.id'))
    books_r: Mapped[Book] = relationship(Book, back_populates='reviews_b')

    review_likes: Mapped[List['ReviewLike']] = relationship(back_populates='review', cascade='all, delete-orphan')


class ReviewLike(Base):
    __tablename__ = 'review_like'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    like: Mapped[bool] = mapped_column(Boolean, default=False)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    relike_u: Mapped[UserProfile] = relationship( back_populates='user_relike')

    review_id: Mapped[int] = mapped_column(ForeignKey('review.id'))
    review: Mapped[Review] = relationship(back_populates='review_likes')


class Cart(Base):
    __tablename__ = 'cart'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user_c: Mapped[UserProfile] = relationship(back_populates='user_cart')

    cart_items: Mapped[List['CartItem']] = relationship(back_populates='items', cascade='all, delete-orphan')




class CartItem(Base):
    __tablename__ = 'cart_item'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    quantity: Mapped[int] = mapped_column(Integer,default=1)

    cart_id: Mapped[int] = mapped_column(ForeignKey('cart.id'))
    items: Mapped[Cart] = relationship(back_populates='cart_items')

    book_id: Mapped[int] = mapped_column(ForeignKey('book.id'))
    item: Mapped[Book] = relationship(Book, back_populates='items')




class FavoriteItem(Base):
    __tablename__ = 'favorite_item'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    added_at: Mapped[datetime] = mapped_column(DateTime)
    price_at_adding: Mapped[int] = mapped_column(Integer)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    users_fav: Mapped[UserProfile] = relationship(back_populates='favorites')

    book_id: Mapped[int] = mapped_column(ForeignKey('book.id'))
    book_fav: Mapped[Book] = relationship(back_populates='favorite')




