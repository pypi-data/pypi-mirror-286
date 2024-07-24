__all__ = ("generate_password_grafana",)


def generate_password_grafana(input_string: str):
    """Generate password grafana."""
    # Let's make sure the string is not longer than the hash expects.
    input_string = input_string[:54]
    # Let's make sure the string is at least 5 characters long.
    if len(input_string) < 5:
        input_string += "0" * (5 - len(input_string))
    # Take the first 10 unique characters of the string.
    unique_chars = sorted(set(input_string))
    password = "".join(unique_chars[:10])
    # If the password is less than 10 characters, fill with zeros.
    password = password.ljust(10, "0")
    return password
