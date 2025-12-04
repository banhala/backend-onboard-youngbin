from __future__ import annotations

from django.contrib.auth import authenticate

from member.model.member import Member


class MemberRepository:

    def find_by_id(self, member_id: int) -> Member | None:
        try:
            return Member.objects.get(id=member_id)
        except Member.DoesNotExist:
            return None

    def find_by_email(self, email: str) -> Member | None:
        try:
            return Member.objects.get(email=email)
        except Member.DoesNotExist:
            return None

    def exists_by_email(self, email: str) -> bool:
        return Member.objects.filter(email=email).exists()

    def save(self, email: str, username: str, password: str) -> Member:
        return Member.objects.create_user(
            email=email,
            username=username,
            password=password,
        )

    def authenticate(self, email: str, password: str) -> Member | None:
        user = authenticate(username=email, password=password)
        if user and isinstance(user, Member):
            return user
        return None
