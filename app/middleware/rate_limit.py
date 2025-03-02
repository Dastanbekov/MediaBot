from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from cachetools import TTLCache
from datetime import datetime

class RateLimiter(BaseMiddleware):
    def __init__(self, rate_limit: int = 5) -> None:
        self.rate_limit = rate_limit  
        self.cache = TTLCache(maxsize=10000, ttl=60.0) 
    
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        
        # Get current timestamp
        now = datetime.now().timestamp()
        
        # Initialize or get user's request count
        if user_id in self.cache:
            requests = self.cache[user_id]
            if len(requests) >= self.rate_limit:
                # Remove old requests
                requests = [ts for ts in requests if now - ts < 60]
                if len(requests) >= self.rate_limit:
                    if isinstance(event, Message):
                        await event.answer(
                            "⚠️ Rate limit exceeded. Please wait a minute before making more requests."
                        )
                    else:
                        await event.answer(
                            text="⚠️ Rate limit exceeded. Please wait a minute.",
                            show_alert=True
                        )
                    return
        else:
            requests = []
        
        # Add current request
        requests.append(now)
        self.cache[user_id] = requests
        
        return await handler(event, data) 