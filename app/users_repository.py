from attrs import define


@define
class User:
    username: str
    full_name: str
    password: str
    id: int = 0


class UsersRepository:
    users: list[User]

    def __init__(self):
        self.users = []

    def save_user(self, user: User):
        user.id = len(self.users)+1
        self.users.append(user)

    def get_user_by_username(self, username: str) -> User:
        for user in self.users:
            if user.username == username:
                return user
        
        return None

    def get_user_by_id(self, id: int) -> User:
        for user in self.users:
            if user.id == id:
                return user

        return None
