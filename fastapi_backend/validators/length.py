def length_str_four_validator(string: str) -> str:
    """Проверяем, что строка состоит из 4 элементов."""
    assert len(string) >= 4, "The line length must be more than 4 characters."
    return string


def length_str_eight_validator(string: str) -> str:
    """Проверяем, что строка состоит из 8 элементов."""
    assert len(string) >= 8, "The line length must be more than 8 characters."
    return string
