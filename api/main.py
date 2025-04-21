from fastapi import FastAPI, Request
from api.router import router as data_router

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Initialize slowapi limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title="Credable Data Pipeline API")

# Register limiter with app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Include data routes
app.include_router(data_router, prefix="/data", tags=["Data"])