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

    def get_pitch_list(self, page=1):
        return self.repo.get_pitch_list(page)

    def get_message_type_counts(self):
        return self.repo.get_message_type_counts()

    def get_total_count(self):
        return self.repo.get_total_count()

    def create_pitch_list(self, records):
        result = self.repo.create_pitch_list(records)
        return result