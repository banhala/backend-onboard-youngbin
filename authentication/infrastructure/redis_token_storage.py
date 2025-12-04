from __future__ import annotations

from django.core.cache import cache


class RedisTokenStorage:

    TOKEN_PREFIX = "jwt:token:"
    USER_TOKENS_PREFIX = "jwt:user:"

    @classmethod
    def save_token(cls, user_id: int, token: str, expire_seconds: int) -> None:
        token_key = f"{cls.TOKEN_PREFIX}{token}"
        user_tokens_key = f"{cls.USER_TOKENS_PREFIX}{user_id}"

        cache.set(token_key, user_id, timeout=expire_seconds)

        user_tokens = cache.get(user_tokens_key, set())
        if not isinstance(user_tokens, set):
            user_tokens = set()
        user_tokens.add(token)
        cache.set(user_tokens_key, user_tokens, timeout=expire_seconds)

    @classmethod
    def get_user_id(cls, token: str) -> int | None:
        token_key = f"{cls.TOKEN_PREFIX}{token}"
        return cache.get(token_key)

    @classmethod
    def is_valid_token(cls, token: str) -> bool:
        return cls.get_user_id(token) is not None

    @classmethod
    def delete_token(cls, user_id: int, token: str) -> None:
        token_key = f"{cls.TOKEN_PREFIX}{token}"
        user_tokens_key = f"{cls.USER_TOKENS_PREFIX}{user_id}"

        cache.delete(token_key)

        user_tokens = cache.get(user_tokens_key, set())
        if isinstance(user_tokens, set) and token in user_tokens:
            user_tokens.remove(token)
            if user_tokens:
                cache.set(user_tokens_key, user_tokens)
            else:
                cache.delete(user_tokens_key)

    @classmethod
    def delete_all_user_tokens(cls, user_id: int) -> None:

        user_tokens_key = f"{cls.USER_TOKENS_PREFIX}{user_id}"
        user_tokens = cache.get(user_tokens_key, set())

        if isinstance(user_tokens, set):
            for token in user_tokens:
                token_key = f"{cls.TOKEN_PREFIX}{token}"
                cache.delete(token_key)

        cache.delete(user_tokens_key)
