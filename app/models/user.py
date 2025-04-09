from flask_login import UserMixin

class User(UserMixin):
    """
    Args:
        user_data (Dict[str, Any]): User data from MongoDB
    Returns:

    Description:
        This class is used with Flask=Login to manage user login. 
        Can expand to include additional user-related methods.
    """
    def __init__(self, user_data):
        self.id = str(user_data["_id"])
        self.username = user_data.get("username")
        self.email = user_data.get("email", "")
        self.instance_name = user_data.get("instance_name", "Default Instance")

    def get_id(self):
        return self.id
