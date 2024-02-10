import pytest

from django.core.exceptions import ValidationError

from user.models import LockboxUser



@pytest.mark.django_db()
class TestUser:
    """
    Test util default creation functions are working.
    """