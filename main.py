from fastapi import FastAPI
import uvicorn

from myproject.admin.setup import setup_admin
from myproject.api import (profile, catalog, subcatalog, typecatalog, address, author, book, bookimage,
                           excerpt, order, orderitem, review, reviewlike, cart, cartitem,favorite, auth)
from myproject.admin.setup import setup_admin


chitay_app = FastAPI(title="Chitay API")
chitay_app.include_router(profile.user_router)
chitay_app.include_router(catalog.catalog_router)
chitay_app.include_router(subcatalog.subcatalog_router)
chitay_app.include_router(typecatalog.type_catalog_router)
chitay_app.include_router(address.address_router)
chitay_app.include_router(author.author_router)
chitay_app.include_router(bookimage.book_image_router)
chitay_app.include_router(excerpt.excerpt_router)
chitay_app.include_router(order.order_router)
chitay_app.include_router(orderitem.order_item_router)
chitay_app.include_router(review.review_router)
chitay_app.include_router(reviewlike.review_like_router)
chitay_app.include_router(cart.cart_router)
chitay_app.include_router(cartitem.cart_item_router)
chitay_app.include_router(favorite.favorite_router)
chitay_app.include_router(book.book_router)
chitay_app.include_router(auth.auth_router)
setup_admin(chitay_app)




if __name__ == "__main__":
    uvicorn.run(chitay_app, host="127.0.0.1", port=8000)
