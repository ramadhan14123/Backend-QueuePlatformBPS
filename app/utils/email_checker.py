import requests

DISPOSABLE_DOMAINS_URL = "https://raw.githubusercontent.com/disposable-email-domains/disposable-email-domains/main/disposable_email_blocklist.conf"

def load_disposable_domains():
    response = requests.get(DISPOSABLE_DOMAINS_URL)
    response.raise_for_status()
    return set(
        line.strip().lower()
        for line in response.text.splitlines()
        if line.strip() and not line.startswith("#")
    )

DISPOSABLE_EMAIL_DOMAINS = load_disposable_domains()

def is_disposable_email(email):
    domain = email.split('@')[-1].lower()
    return domain in DISPOSABLE_EMAIL_DOMAINS