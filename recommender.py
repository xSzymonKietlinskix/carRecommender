from user import User, DecodedUser

def recommend(user):
    dec_user = user.decode()
    dec_user.save_user(1, 1)
