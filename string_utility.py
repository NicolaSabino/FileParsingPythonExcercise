"""String utility modile"""

from logger import logger

VALID_STR_LEN = 16
VALID_STR_BEGIN = "#G4"
VALID_STR_END = "\r\n"


def compute_checksum(input_str: str) -> int:
    """Compute string checksum

    Checksum is calculated by adding the ASCII values corresponding to
    the hex digits from the # included to the last character before the checksum itself.
    The addition is 8 bit, so it overflows each time the sum exceeds 255.

    If invalid string is passed checksum return -1

    Args:
        input_str (str): input string

    Returns:
        int: The computed checksum value
    """
    try:

        checksum = 0
        for digit in input_str[:-4]:
            checksum += ord(digit)
            checksum = checksum % 256

        return checksum

    except TypeError:
        logger.error("Invalid string for checksum computation")
        return -1


def is_checksum_valid(input_str: str) -> bool:
    """I checksum in string valid

    Args:
        input_str (str): The input string

    Returns:
        bool: True if checksum embedded in string correspond to computed checksum
    """
    str_checksum = input_str[-4:-2]
    computed_checksum = compute_checksum(input_str)
    if int(str_checksum, base=16) == computed_checksum:
        logger.debug("Chesum valid for %s", repr(input_str))
        return True
    else:
        logger.warning("Checksum not valid for %s", repr(input_str))
        return False


def is_string_valid(input_str: str) -> bool:
    """Is accelerometer string valid

    A valid accelerometer string always begins with the identifier #G4
    and ends with \\r\\n.

    The message is fixed length. The two hex digits, CC, represent a checksum
    for the message.

    CC is calculated by adding the ASCII values corresponding to the hex digits
    from the # to the last character before the checksum itself. The addition
    is 8 bit, so it overflows each time the sum exceeds 255.

    If input string is none it return false.

    Args:
        input_str (str): The string to be processed

    Returns:
        bool: True if string fits requirements
    """

    if input_str is None:
        logger.debug("Invalid message - Input string is None")
        return False

    if input_str == "":
        logger.debug("Invalid message - Input string is empty")
        return False

    if len(input_str) != VALID_STR_LEN:
        logger.debug("Invalid message - Invalid string lenght for %s", repr(input_str))
        return False

    if not input_str.startswith(VALID_STR_BEGIN):
        logger.debug(
            "Invalid message - Invalid string beginning for %s", repr(input_str)
        )
        return False

    if not input_str.endswith(VALID_STR_END):
        logger.debug("Invalid message - Invalid string end for %s", repr(input_str))
        return False

    return True


def main():
    """Main function"""
    is_string_valid(None)
    is_string_valid("")
    is_string_valid("#G4001FFF03DA8\r\n")

    inpt = "#G4001FFF03DA8\r\n"
    assert compute_checksum(inpt) == 168, compute_checksum(inpt)
    assert is_checksum_valid(inpt)


if __name__ == "__main__":
    main()
