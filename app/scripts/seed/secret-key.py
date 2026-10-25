"""Generate a random secret for local API practice.

Run: python app/scripts/seed/secret-key.py
Each run prints a new URL-safe value. Store it outside source control.
"""

from secrets import token_urlsafe


def main() -> None:
    print(token_urlsafe(32))


if __name__ == "__main__":
    main()
