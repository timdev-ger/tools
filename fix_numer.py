import re

country_patterns = [
    ("49", r"^0(1[5-7]\d{8}|[2-9]\d{3,})$"),
    ("43", r"^0(6\d{7,8}|1\d{7})$"),
    ("41", r"^0(7\d{8}|[2-4]\d{7})$"),
    ("33", r"^0[1-9]\d{8}$"),
    ("44", r"^0\d{9,10}$"),
    ("1",  r"^[2-9]\d{9}$"),
]

def normalize(phone):
    return re.sub(r"[^\d+]", "", phone)

def to_e164(phone):
    phone = normalize(phone)

    # 0049... → +49...
    if phone.startswith("00"):
        phone = "+" + phone[2:]

    # already E.164-Format?
    if phone.startswith("+") and re.fullmatch(r"\+\d{6,15}", phone):
        return phone

    if not phone.startswith("0") and re.fullmatch(r"\d{10}", phone):
        return "+1" + phone

    for country_code, pattern in country_patterns:
        if re.fullmatch(pattern, phone):
            national_number = phone.lstrip("0")
            return f"+{country_code}{national_number}"

    return ""  # Nothing found

# Zapier Input
raw_number = input_data.get("phone", "")

# Output
output = {"formatted_number": to_e164(raw_number)}
