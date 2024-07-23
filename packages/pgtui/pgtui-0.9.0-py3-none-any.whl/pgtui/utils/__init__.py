from uuid import uuid4


def random_id():
    return f"id_{uuid4().hex}"
