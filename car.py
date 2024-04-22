import joblib
import pandas as pd



class Car:
    def __init__(self, id =0, brand = 0, model = 0, generation = 0, version = 0, length = 0, width = 0, height = 0, wheel_base = 0, petrol_min_cap = 0, petrol_max_cap = 0, petrol_min_hp = 0, petrol_max_hp = 0, avg_weight = 0, price = 0):
        self.price = price
        self.avg_weight = avg_weight
        self.petrol_max_hp = petrol_max_hp
        self.petrol_min_hp = petrol_min_hp
        self.petrol_max_cap = petrol_max_cap
        self.petrol_min_cap = petrol_min_cap
        self.wheel_base = wheel_base
        self.height = height
        self.width = width
        self.length = length
        self.version = version
        self.generation = generation
        self.model = model
        self.brand = brand
        self.id = id



    def find_cars_segments(file_name):
        knn = joblib.load('models/knn1.pkl')
        cars_db = pd.read_csv(file_name, sep=';')
        cars_to_pred = cars_db.copy()
        cars_to_pred = cars_to_pred.drop(['Id', 'Model', 'Generation', 'Version', 'Height', 'Brand', 'Price'], axis = 1)
        scaler = joblib.load('models/knn1_scaler.pkl')
        cars_to_pred = scaler.transform(cars_to_pred)
        prediction = knn.predict(cars_to_pred)
        cars_db = cars_db.assign(Segment=prediction)
        return cars_db


