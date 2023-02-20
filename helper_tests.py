

def simple_assert(gotten_val, expected_val):
    assert gotten_val == expected_val, f"Assertion failed, expected: {expected_val}, got: {gotten_val}"


def boolean_assert(value, message):
    assert value, message