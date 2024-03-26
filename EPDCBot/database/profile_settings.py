def PROFILE_TABLE_TO_NEXT_LEVEL(level: int) -> int:
    """
    Returns the experience required to reach the next level.

    args:
        level: int - The current level of the profile.

    returns:
        int - The experience required to reach the next level.
    """
    return profile_table_to_next_level(level)

def profile_table_to_next_level(level: int) -> int:
    """
    Returns the experience required to reach the next level.

    args:
        level: int - The current level of the profile.

    returns:
        int - The experience required to reach the next level.
    """
    return round(2**(.9*level))

def profile_table_exp_per_message_by_level(level: int) -> int:
    """
    Returns the experience gained per message based on the level of the profile.

    args:
        level: int - The current level of the profile.

    returns:
        int - The experience gained per message.
    """
    return max(1, round(0.01*profile_table_to_next_level(level)))
