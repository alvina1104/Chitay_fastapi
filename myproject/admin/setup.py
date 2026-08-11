from fastapi import FastAPI
from sqladmin import Admin
from myproject.database.db import engine
from .views import (UserProfileAdmin, CatalogAdmin, SubCatalogAdmin, TypeCatalogAdmin,
                    AddressAdmin, AuthorAdmin, BookAdmin, BookImageAdmin, ExcerptAdmin,
                    OrderAdmin, OrderItemAdmin, ReviewAdmin, ReviewLikeAdmin,
                    CartAdmin, CartItemAdmin, FavoriteItemAdmin)


def setup_admin(myproject: FastAPI):
    admin = Admin(myproject, engine)
    admin.add_view(UserProfileAdmin)
    admin.add_view(CatalogAdmin)
    admin.add_view(SubCatalogAdmin)
    admin.add_view(TypeCatalogAdmin)
    admin.add_view(AddressAdmin)
    admin.add_view(AuthorAdmin)
    admin.add_view(BookAdmin)
    admin.add_view(BookImageAdmin)
    admin.add_view(ExcerptAdmin)
    admin.add_view(OrderAdmin)
    admin.add_view(OrderItemAdmin)
    admin.add_view(ReviewAdmin)
    admin.add_view(ReviewLikeAdmin)
    admin.add_view(CartAdmin)
    admin.add_view(CartItemAdmin)
    admin.add_view(FavoriteItemAdmin)