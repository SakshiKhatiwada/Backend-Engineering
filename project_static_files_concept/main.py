from fastapi import FastAPI
from fastapi import APIRouter

app = FastAPI()
router = APIRouter()

router.frontend("/", directory="static", fallback="404.html")
app.include_router(router, prefix="/app") # to show frontend page only for this route