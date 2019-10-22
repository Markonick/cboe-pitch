from app.services import PitchListService
from app.repositories import PitchListRepo


def create_pitch_list_repo():
    return PitchListRepo()


def create_pitch_list_service():
    return PitchListService(create_pitch_list_repo())
