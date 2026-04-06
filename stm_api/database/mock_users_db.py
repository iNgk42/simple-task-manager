from typing import List
from stm_api.users.models import UserInDb

users_db: List[UserInDb] = [
    UserInDb(
        id = 1, 
        name = "Rick", 
        email = "rick@example.com", 
        passwordhash = "8d2f3db7b78917dfa579396265d931aece30d695413e5787c387f1c0d6cfafac", 
        created_at = "2026-04-03T12:00:00"
    ),
    UserInDb(
        id = 2, 
        name = "Morty", 
        email = "morty@example.com", 
        passwordhash = "6df8a65b771b62fceb0404fdde83c15c7d73ce96080dd514aee0fa28d09b5a3d", 
        created_at = "2026-04-03T12:45:00"
    )
]