class User:
    def __init__(self, username: str, role: str):
        self.username = username
        self.role = role
        
    def to_dict(self):
        return {
            'username': self.username,
            'role': self.role
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            username=data['username'],
            role=data['role']
        )