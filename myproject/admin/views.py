from myproject.database.models import (UserProfile, Catalog, SubCatalog, TypeCatalog,Address,
                                       Author, Book, BookImage, Excerpt, Order, OrderItem,
                                       Review, ReviewLike, Cart, CartItem, FavoriteItem)
from sqladmin import ModelView

class UserProfileAdmin(ModelView, model= UserProfile):
    column_list = [UserProfile.id, UserProfile.first_name, UserProfile.last_name]


class CatalogAdmin(ModelView, model=Catalog):
    column_list = [Catalog.id,Catalog.catalog_name]


class SubCatalogAdmin(ModelView, model=SubCatalog):
    column_list = [SubCatalog.id,SubCatalog.subcatalog_name,SubCatalog.catalog_id,]



class TypeCatalogAdmin(ModelView, model=TypeCatalog):
    column_list = [TypeCatalog.id,TypeCatalog.typecatalog_name,TypeCatalog.subcatalog_id,]


class AddressAdmin(ModelView, model=Address):
    column_list = [Address.id,Address.title,]


class AuthorAdmin(ModelView, model=Author):
    column_list = [Author.id,Author.author_name,]



class BookAdmin(ModelView, model=Book):
    column_list = [Book.id, Book.book_name,]



class BookImageAdmin(ModelView, model=BookImage):
    column_list = [BookImage.id,BookImage.book_image,]



class ExcerptAdmin(ModelView, model=Excerpt):
    column_list = [Excerpt.id,Excerpt.excerpt_name,]



class OrderAdmin(ModelView, model=Order):
    column_list = [Order.id, Order.user_id,]


class OrderItemAdmin(ModelView, model=OrderItem):
    column_list = [OrderItem.id,
        OrderItem.order_id,]



class ReviewAdmin(ModelView, model=Review):
    column_list = [Review.id,Review.book_id,]


class ReviewLikeAdmin(ModelView, model=ReviewLike):
    column_list = [ReviewLike.id,ReviewLike.review_id,]



class CartAdmin(ModelView, model=Cart):
    column_list = [Cart.id,Cart.user_id,]



class CartItemAdmin(ModelView, model=CartItem):
    column_list = [CartItem.id,CartItem.cart_id,]



class FavoriteItemAdmin(ModelView, model=FavoriteItem):
    column_list = [FavoriteItem.id,FavoriteItem.book_id, ]
