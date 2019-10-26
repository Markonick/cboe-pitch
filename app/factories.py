import os
from app.services import PitchListService
from app.repositories import PitchListRepo

per_page = int(os.environ.get('PER_PAGE'))

def create_pitch_list_repo():
    return PitchListRepo(per_page)


def create_pitch_list_service():
    return PitchListService(create_pitch_list_repo())
