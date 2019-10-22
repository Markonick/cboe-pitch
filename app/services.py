import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s")
logger = logging.getLogger("REPO")


class PitchListService:
    """
    Service class responsible for handling pitch list
    """

    def __init__(self, repo):
        self.repo = repo

    def get_pitch_list(self):
        return self.repo.get_pitch_list()

    def create_pitch_list(self, message_type, timestamp):
        result = self.repo.create_pitch_list(message_type, timestamp)
        return result
