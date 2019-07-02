from database.ext import redis_client


#验证admin-token
def verify_token(token):
    if not token:
        return None
    uid = redis_client.get(token)
    return int(uid) if uid else None