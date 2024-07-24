class NoUpdatesMadeException(Exception):
    def __init__(self, response):
        self.response = response
        super().__init__(f"Failed to update the post. Response: {response}")


class FailedDeletePostException(Exception):
    def __init__(self, response):
        self.response = response
        super().__init__(f"Failed to delete the post. Response: {response}")