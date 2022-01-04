class GameInterruptedException(Exception):
    """Raised when pressing Q within a game"""
    pass


class ApplicationInterruptedException(Exception):
    """Raised when pressing Q in the main menu"""
    pass
