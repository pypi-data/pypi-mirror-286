import hashlib
import urllib.request

from django.core.exceptions import ValidationError


class HaveIBeenPwnedValidator:
    def validate(self, password, user=None):
        """
        Check whether a password is known to Have I Been Pwned.

        Responses from the service are raw text of the form (as per
        the
        [API docs.](https://haveibeenpwned.com/API/v3#SearchingPwnedPasswordsByRange)):

        ```txt
        04A37A676E312CC7C4D236C93FBD992AA3C:10
        04AE045B134BDC43043B216AEF66100EE00:3
        ```

        :param password: to be checked
        :param user: unused in this context
        :raises ValidationError: if returned in the API response
        """
        sha1 = hashlib.sha1()  # nosec:required by service.
        sha1.update(password.encode())
        digest = sha1.hexdigest().upper()
        prefix = digest[:5]
        url = f"https://api.pwnedpasswords.com/range/{prefix}"
        request = urllib.request.Request(url, headers={"User-Agent": "django-pwny"})
        response = urllib.request.urlopen(request)  # nosec:URL required as above.
        for suffix_count in response.read().decode().splitlines():
            suffix, count = suffix_count.split(":")
            if digest == f"{prefix}{suffix}":
                raise ValidationError(
                    f"Your password has been pwned {int(count):,} times!"
                )
                break

    def get_help_text(self):
        return "Your password should not appear in a list of compromised passwords."
