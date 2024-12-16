from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from app.api.authors.routes import router as authors_router
from app.api.books.routes import router as books_router
from app.api.borrows.routes import router as borrows_router
from app.database.db import db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.create_tables()
    yield
    await db.dispose()


main_app = FastAPI(default_response_class=ORJSONResponse, lifespan=lifespan)

main_app.include_router(router=authors_router, prefix="/authors")
main_app.include_router(router=books_router, prefix="/books")
main_app.include_router(router=borrows_router, prefix="/borrows")
