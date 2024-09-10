from flask import Blueprint, request, jsonify
from extensions import db, session_scope
from marshmallow import ValidationError
import csv
from utils.utils import success_response, validate_training_data, create_training_record
from models import Employee, Training, EventLog, Form, AgentLog, Email, DashboardItem
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token

# 블루프린트 설정
routes = Blueprint('training', __name__)

# 홈 경로
@routes.route('/')
def home():
    return "Welcome to Email Test"

# 로그인 라우트
@routes.route('/login', methods=['POST'])
def login():
    username = request.json.get('username') if request.is_json else request.form.get('username')
    password = request.json.get('password') if request.is_json else request.form.get('password')

    if not username or not password:
        return jsonify({"msg": "Username and password required"}), 400

    user = db.session.query(Employee).filter_by(username=username).first()
    if not user or user.password != password:
        return jsonify({"msg": "Invalid username or password"}), 401
    if not user.is_admin:
        return jsonify({"msg": "You are not authorized to access this resource"}), 403

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200

# 권한 확인 함수
def get_admin_user():
    current_user = get_jwt_identity()
    user = db.session.query(Employee).filter_by(username=current_user).first()
    if not user or not user.is_admin:
        return None
    return user

# 필수 필드 확인 함수
def check_required_fields(data, required_fields):
    for field in required_fields:
        if field not in data:
            return f"Missing required field: {field}"
    return None

# 직원 관련 라우트
@routes.route('/employees', methods=['GET'])
def get_users():
    with session_scope() as session:
        users = session.query(Employee).all()
        return success_response(employees_schema.dump(users), status=200)

@routes.route('/employees/<int:id>', methods=['GET'])
def get_user(id):
    with session_scope() as session:
        user = session.query(Employee).get_or_404(id)
        return jsonify(employee_schema.dump(user))

@routes.route('/employees', methods=['POST'])
def add_user():
    try:
        user_data = employee_schema.load(request.json)
        with session_scope() as session:
            new_user = Employee(**user_data)
            session.add(new_user)
            session.flush()
            return jsonify(employee_schema.dump(new_user)), 201
    except ValidationError as err:
        return jsonify(err.messages), 400

@routes.route('/users/with-training', methods=['GET'])
def get_users_with_trainings():
    try:
        with session_scope() as session:
            all_users = session.query(Employee).all()
            result = users_with_trainings_schema.dump(all_users)
            return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e), "message": "An error occurred while retrieving users with trainings"}), 500

# 트레이닝 관련 라우트
@routes.route('/training/create', methods=['POST'])
@jwt_required()
def create_training():
    user = get_admin_user()
    if not user:
        return jsonify({"msg": "You are not authorized to create training"}), 403

    data = request.json
    if not data:
        return jsonify({"message": "No input data provided"}), 400

    required_fields = ['trainingName', 'trainingDesc', 'trainingStart', 'trainingEnd', 'resourceUser', 'maxPhishingMail', 'status', 'department']
    missing_field = check_required_fields(data, required_fields)
    if missing_field:
        return jsonify({"message": missing_field}), 400

    v_data, error = validate_training_data(data)
    if error:
        return jsonify(error), 400

    try:
        with session_scope() as session:
            new_training, initial_event_log = create_training_record(v_data)
            session.add(new_training)
            session.add(initial_event_log)
            session.commit()
            return jsonify(training_schema.dump(new_training)), 201
    except ValidationError as err:
        return jsonify({"message": "Validation error", "errors": err.messages}), 400    
    except Exception as e:
        return jsonify({"message": "An error occurred while creating the training", "error": str(e)}), 500

@routes.route('/training/read/<int:id>', methods=['GET'])
def get_training(id):
    try:
        training = db.session.query(Training).filter_by(id=id).first()
        if not training:
            return jsonify({"message": "Training not found"}), 404
        return jsonify(training_schema.dump(training)), 200
    except Exception as e:
        return jsonify({"error": str(e), "message": "An error occurred while retrieving training"}), 500

@routes.route('/training/bulk', methods=['POST'])
def bulk_training():
    data = request.json
    v_data, error = validate_training_data(data, many=True)
    try:
        with session_scope() as session:
            session.query(Training).delete()
            for item in v_data:
                new_training, initial_event_log = create_training_record(item)
                session.add(new_training)
                session.add(initial_event_log)
            session.commit()
            return jsonify({"message": f"{len(v_data)} trainings successfully added!"}), 201
    except ValidationError as ve:
        return jsonify({"error": "Validation error", "details": ve.messages}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@routes.route('/training/read', methods=['GET'])
def get_trainings():
    try:
        all_trainings = db.session.query(Training).all()
        result = trainings_schema.dump(all_trainings)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e), "message": "An error occurred while retrieving trainings"}), 500

# 기타 라우트
@routes.route('/forms', methods=['GET'])
def get_forms():
    with session_scope() as session:
        forms = session.query(Form).all()
        return jsonify(forms_schema.dump(forms))

@routes.route('/emails/read', methods=['GET'])
def get_emails():
    with session_scope() as session:
        emails = session.query(Email).all()
        return jsonify(emails_schema.dump(emails))

# 이벤트 로그
@routes.route('/training/view/<int:id>', methods=['GET'])
def view_training_event_logs(id):
    try:
        event_logs = db.session.query(EventLog).filter_by(training_id=id).all()
        if not event_logs:
            return jsonify({"message": "No event logs found for the specified training ID"}), 404
        result = event_logs_schema.dump(event_logs)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e), "message": "An error occurred while retrieving event logs"}), 500

# 대시보드
@routes.route('/dashboard/read', methods=["GET"])
def get_dashboard():
    try:
        with session_scope() as session:
            total_trainings = session.query(Training).count()
            avg_phishing_mails = session.query(db.func.avg(Training.maxPhishingMail)).scalar() or 0

            dashboard_items = [
                DashboardItem(title="Total Trainings", value=str(total_trainings), description="Total number of trainings"),
                DashboardItem(title="Avg Phishing Mails", value=f"{avg_phishing_mails:.2f}", description="Average number of phishing mails per training")
            ]
            result = dashboard_items_schema.dump(dashboard_items)
            return jsonify(result), 200
    except Exception as e:
        return jsonify({"message": "Error from Dashboard items", "error": str(e)}), 500

# 에이전트 로그
@routes.route('/agent/logs', methods=['POST'])
def receive_logs():
    try:
        logs = request.get_json()
        with session_scope() as session:
            for log_entry in logs:
                agent_log = AgentLog(**log_entry)
                session.add(agent_log)
        return jsonify({"message": "Logs successfully stored"}), 201
    except Exception as e:
        return jsonify({"error": "Failed to store logs", "details": str(e)}), 500

@routes.route('/agent/logs', methods=['GET'])
def get_logs():
    try:
        with session_scope() as session:
            logs = session.query(AgentLog).all()
            return jsonify(agent_logs_schema.dump(logs)), 200
    except Exception as e:
        return jsonify({"error": "Failed to retrieve logs", "details": str(e)}), 500

@routes.route('/agent/upload_csv', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and file.filename.endswith('.csv'):
        try:
            csv_reader = csv.DictReader(file.stream.read().decode('utf-8').splitlines())
            with session_scope() as session:
                for row in csv_reader:
                    agent_log = AgentLog(**row)
                    session.add(agent_log)
            return jsonify({"message": "CSV file successfully processed and data stored"}), 201
        except Exception as e:
            return jsonify({"error": "Failed to process CSV file", "details": str(e)}), 500
    else:
        return jsonify({"error": "Invalid file format"}), 400
