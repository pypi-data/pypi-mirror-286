import re
from typing import Union

from normalise.domains import (
    gmail_domains,
    icloud_domains,
    outlookdotcom_domains,
    yahoo_domains,
    yandex_domains,
)

re_single_dot = re.compile(r"(?<!\.)\.(?!\.)")


def normalise_email(
    email: str,
    all_lowercase: bool = True,
    gmail_lowercase: bool = True,
    gmail_remove_dots: bool = True,
    gmail_remove_subaddress: bool = True,
    gmail_convert_googlemaildotcom: bool = True,
    outlookdotcom_lowercase: bool = True,
    outlookdotcom_remove_subaddress: bool = True,
    yahoo_lowercase: bool = True,
    yahoo_remove_subaddress: bool = True,
    yandex_lowercase: bool = True,
    icloud_lowercase: bool = True,
    icloud_remove_subaddress: bool = True,
) -> Union[str, bool]:
    """
    Normalise an email address.

    Taken from:
    https://github.com/validatorjs/validator.js/blob/master/src/lib/normalizeEmail.js#L170

    :param email: email address
    :param all_lowercase: lower-case the local part of an email address
    :param gmail_lowercase: lower-case the local part of a Gmail address
    :param gmail_remove_dots: remove dots from the local part of a Gmail address
    :param gmail_remove_subaddress: remove subaddresses from a Gmail address
    :param gmail_convert_googlemaildotcom: change googlemail.com domain to gmail.com
    :param outlookdotcom_lowercase: lower-case the local part of an Outlook address
    :param outlookdotcom_remove_subaddress: remove subaddresses from an Outlook address
    :param yahoo_lowercase: lower-case the local part of a Yahoo address
    :param yahoo_remove_subaddress: remove subaddresses from a Yahoo address
    :param yandex_lowercase: lower-case the local part of a Yandex address
    :param icloud_lowercase: lower-case the local part of an iCloud address
    :param icloud_remove_subaddress: remove subaddresses from an iCloud address
    :return: normalised email address
    """
    # TODO: better-served as parts = email.rsplit("@", 1)?
    raw_parts = email.split("@")
    domain = raw_parts.pop()
    user = "@".join(raw_parts)
    parts = [user, domain]

    # The domain is always lowercased, as it's case-insensitive per RFC 1035
    parts[1] = parts[1].lower()

    if parts[1] in gmail_domains:

        if gmail_remove_subaddress:
            parts[0] = parts[0].split("+")[0]

        if gmail_remove_dots:
            # this does not replace consecutive dots like example..email@gmail.com
            parts[0] = re_single_dot.sub("", parts[0])

        if len(parts[0]) == 0:
            return False

        if all_lowercase or gmail_lowercase:
            parts[0] = parts[0].lower()

        if gmail_convert_googlemaildotcom:
            parts[1] = "gmail.com"

    elif parts[1] in icloud_domains:

        if icloud_remove_subaddress:
            parts[0] = parts[0].split("+")[0]

        if len(parts[0]) == 0:
            return False

        if all_lowercase or icloud_lowercase:
            parts[0] = parts[0].lower()

    elif parts[1] in outlookdotcom_domains:

        if outlookdotcom_remove_subaddress:
            parts[0] = parts[0].split("+")[0]

        if len(parts[0]) == 0:
            return False

        if all_lowercase or outlookdotcom_lowercase:
            parts[0] = parts[0].lower()

    elif parts[1] in yahoo_domains:

        if yahoo_remove_subaddress:
            parts[0] = parts[0].rsplit("-", 1)[0]

        if len(parts[0]) == 0:
            return False

        if all_lowercase or yahoo_lowercase:
            parts[0] = parts[0].lower()

    elif parts[1] in yandex_domains:

        if all_lowercase or yandex_lowercase:
            parts[0] = parts[0].lower()

        parts[1] = "yandex.ru"  # all yandex domains are equal, 1st preferred

    elif all_lowercase:
        parts[0] = parts[0].lower()

    return "@".join(parts)
