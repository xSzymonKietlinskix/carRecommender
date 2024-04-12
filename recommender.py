from sklearn.metrics import DistanceMetric

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
    car_frame = cars_db.sample()
    selected_columns = ['Brand', 'Generation', 'Model', 'Version', 'Id']
    car_frame_str = car_frame[selected_columns].astype(str)
    car_list = car_frame_str.values.tolist()[0]
    car = Car(brand=car_list[0], generation=car_list[1], model=car_list[2], version=car_list[3], id=int(car_list[4]))
    # c_filtering(dec_user)
    return car



def c_filtering(dec_user):
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
    metric = DistanceMetric.get_metric('manhattan')
    distances = metric.pairwise(users[features], [user_list])
    distances_df = pd.DataFrame({'Id': users['Id'], 'Distance': distances.flatten()})
    sorted_users = distances_df.sort_values(by='Distance')

    # Wybór k najbliższych sąsiadów (użytkowników)
    k = 2
    nearest_neighbors = sorted_users.head(k)

    # Zwrócenie ID użytkowników jako rekomendacji
    recommendations = nearest_neighbors['Id'].tolist()
    print("Rekomendowane ID użytkowników:", recommendations)

