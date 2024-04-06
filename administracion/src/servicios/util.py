from uuid import UUID

def is_valid_id(uuid: str, version: int = 4) -> bool:
    try:
        uuid_obj = UUID(uuid, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid