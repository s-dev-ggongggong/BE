import json
from .models.training import Training
from .extensions import db, session_scope
from run import  create_app
import requests


def load_trainings(file_path):
    with open(file_path, 'r') as file:
        trainings_data = json.load(file)

    trainings = [
        Training(
            trainingName=item['trainingName'],
            trainingDesc=item['trainingDesc'],
            trainingStart=item['trainingStart'],
            trainingEnd=item['trainingEnd'],  # 이 부분에서 오타가 수정되었습니다
            resourceUser=item['resourceUser'],
            maxPhishingMail=item['maxPhishingMail']  # 여기서도 오타가 수정되었습니다
        )
        for item in trainings_data
    ]

    with create_app().app_context():
        with session_scope() as session:
            session.bulk_save_objects(trainings)
            print(f"Inserted {len(trainings)} in to DB.")



    response = requests.post('http://localhost:8000/training/bulk', json=trainings_data)
    print(response.status_code)
    try:
        print(response.json())
    except json.JSONDecodeError as e :
        print("Failed to decode JSON")


if __name__ == '__main__':
    load_trainings('static/trainings.json')