class NotifyRecipientError(Exception):
    """Exception raised when neither user nor group is defined for notification."""
    def __init__(self):
        super().__init__("At least a user or group must be defined for notification.")
