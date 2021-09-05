"""Binary string manipulation."""


def bin_to_string(string: str, *, sep: str = " ") -> str:
    """Convert a binary string, with the characters separated by `sep`."""
    if sep == "":
        raise ValueError("Separator cannot be empty.")
    if not isinstance(sep, str):
        raise TypeError(
            "Expected value of type str, got "
            f"{sep} of type {sep.__class__.__name__}"
        )
    if not isinstance(string, str):
        raise TypeError(
            "Expected value of type str, got "
            f"{string} of type {string.__class__.__name__}"
        )
    return "".join([chr(int(sub, base=2)) for sub in string.split(sep)])


def string_to_binary(string: str, sep: str = " ") -> str:
    """Convert a string to 8-digits binaries separated by `sep`."""
    encoded = []
    for char in string:
        binary = bin(ord(char))[2:]
        encoded.append("0" * (8 - len(binary)) + binary)
    return sep.join(encoded)
