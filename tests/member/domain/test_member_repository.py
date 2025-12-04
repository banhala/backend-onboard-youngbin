import pytest

from member.domain.member_repository import MemberRepository


@pytest.fixture
def repository():
    return MemberRepository()


@pytest.mark.django_db
class TestMemberRepository:

    def test_save_member(self, repository):
        # Given
        email = "youngbin.seo@a-bly.com"
        username = "youngbin"
        password = "Password1234!"

        # When
        member = repository.save(email, username, password)

        # Then
        assert member is not None
        assert member.email == email
        assert member.username == username
        assert member.password != password

    def test_exists_by_email_true(self, repository):
        # Given
        email = "youngbin.seo@a-bly.com"
        repository.save(email, "youngbin", "Password1234!")

        # When
        exists = repository.exists_by_email(email)

        # Then
        assert exists is True

    def test_exists_by_email_false(self, repository):
        # Given
        email = "notexists@a-bly.com"

        # When
        exists = repository.exists_by_email(email)

        # Then
        assert exists is False

    def test_find_by_email_success(self, repository):
        # Given
        email = "find@a-bly.com"
        username = "finduser"
        repository.save(email, username, "Password1234!")

        # When
        member = repository.find_by_email(email)

        # Then
        assert member is not None
        assert member.email == email
        assert member.username == username

    def test_find_by_email_not_found(self, repository):
        # Given
        email = "notfound@a-bly.com"

        # When
        member = repository.find_by_email(email)

        # Then
        assert member is None

    def test_find_by_id_success(self, repository):
        # Given
        saved_member = repository.save(
            "youngbin.seo@a-bly.com", "youngbin", "Password1234!"
        )

        # When
        member = repository.find_by_id(saved_member.id)

        # Then
        assert member is not None
        assert member.id == saved_member.id
        assert member.email == saved_member.email

    def test_find_by_id_not_found(self, repository):
        # Given
        non_existent_id = 99999

        # When
        member = repository.find_by_id(non_existent_id)

        # Then
        assert member is None

    def test_authenticate_success(self, repository):
        # Given
        email = "youngbin.seo@a-bly.com"
        password = "Password1234!"
        repository.save(email, "youngbin", password)

        # When
        member = repository.authenticate(email, password)

        # Then
        assert member is not None
        assert member.email == email

    def test_authenticate_wrong_password(self, repository):
        # Given
        email = "youngbin.seo@a-bly.com"
        password = "Password1234!"
        username = "youngbin"
        repository.save(email, username, password)

        # When
        member = repository.authenticate(email, "wrongpassword")

        # Then
        assert member is None

    def test_authenticate_nonexistent_user(self, repository):
        # Given
        email = "nonexistent@a-bly.com"
        password = "Password1234!"

        # When
        member = repository.authenticate(email, password)

        # Then
        assert member is None
