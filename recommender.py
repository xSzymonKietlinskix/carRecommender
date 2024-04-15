from sklearn.metrics import DistanceMetric
from sklearn.neighbors import NearestNeighbors

from user import User, DecodedUser
from car import  Car
import pandas as pd
def recommend(user):
    dec_user = user.decode()
    cars_db = Car.find_cars_segments("car database.csv")
    cars_db = cars_db[(cars_db['Price'] >= dec_user.min_price) & (cars_db['Price'] <= dec_user.max_price)]
    cars_db_selected = cars_db[cars_db['Segment'].isin(dec_user.purpose)]
    if not cars_db_selected.empty:
        cars_db = cars_db_selected
    matching_users = find_similar_users(dec_user)
    cars_selected = filter_cars(matching_users, cars_db)
    car_frame = cars_db.sample()
    selected_columns = ['Brand', 'Generation', 'Model', 'Version', 'Id']
    car_frame_str = car_frame[selected_columns].astype(str)
    car_list = car_frame_str.values.tolist()[0]
    car = Car(brand=car_list[0], generation=car_list[1], model=car_list[2], version=car_list[3], id=int(car_list[4]))
    return car



def find_similar_users(dec_user):
    przeznaczenie_dict = {
        'Rodzinny': 1,
        'Miejski': 2,
        'Uniwersalny': 3,
        'Trasy': 4,
        'Sportowy': 5
    }
    user_list = list(dec_user.values())
    user_list[0] = przeznaczenie_dict.get(user_list[0], None)

    users = pd.read_csv("users.csv", sep=';')
    users['przeznaczenie'] = users['przeznaczenie'].map(przeznaczenie_dict)
    features = ['przeznaczenie', 'ekonomia', 'komfort', 'styl', 'min_price', 'max_price']

    # Wybór k najbliższych sąsiadów (użytkowników)
    rows, _ = users.shape
    k = 3
    knn = NearestNeighbors(n_neighbors=k, metric='manhattan')
    knn.fit(users[features])

    distances, indices = knn.kneighbors([user_list])

    # Wyświetlenie wyników
    nearest_neighbors = users.iloc[indices[0]]
    matching_users = check_ratings(nearest_neighbors)
    return matching_users

def check_ratings(users):
    users_ratings = pd.read_csv('users_ratings.csv', sep=';')
    matching_users = users_ratings[users_ratings['user_id'].isin(users['id'])]
    return matching_users

def filter_cars(matching_users, cars_db):
    cars_db['accuracy'] = 3
    rating_map = dict(zip(matching_users['car_id'], matching_users['rating']))
    cars_db['accuracy'] = cars_db['Id'].map(rating_map).fillna(cars_db['accuracy'])
    print(cars_db)

