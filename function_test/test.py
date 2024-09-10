import os
import secrets
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from extensions import db  # SQLAlchemy 세션을 불러옵니다
from models import Employee, Training  # Employee와 Training 모델을 불러옵니다

app = Flask(__name__)

# JWT 설정
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', secrets.token_urlsafe(32))
jwt = JWTManager(app)

# 루트 라우트 (홈페이지 또는 기본 경로)
@app.route('/')
def home():
    return jsonify({"msg": "Welcome to the API"}), 200

# 로그인 라우트 (POST: 로그인 처리, 관리자용)
@app.route('/login', methods=['POST'])
def login():
    # 로그인 시 username과 password를 JSON 또는 form 데이터로 받음
    username = request.json.get('username') if request.is_json else request.form.get('username')
    password = request.json.get('password') if request.is_json else request.form.get('password')
    
    if not username or not password:
        return jsonify({"msg": "Username and password required"}), 400

    # DB에서 사용자 조회
    user = db.session.query(Employee).filter_by(username=username).first()
    
    if not user or user.password != password:
        return jsonify({"msg": "Invalid username or password"}), 401
    
    # 관리자인지 확인
    if not user.is_admin:
        return jsonify({"msg": "You are not authorized to access this resource"}), 403

    # JWT 토큰 생성
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200

# Training 생성 라우트 (POST: 트레이닝 생성, 관리자 인증 필수)
@app.route('/training/create', methods=['POST'])
@jwt_required()  # JWT 인증 필수
def create_training():
    # 현재 사용자 정보 가져오기 (JWT 토큰에서)
    current_user = get_jwt_identity()

    # DB에서 사용자 정보 조회
    user = db.session.query(Employee).filter_by(username=current_user).first()

    # 사용자 권한 확인 (관리자 여부)
    if not user or not user.is_admin:
        return jsonify({"msg": "You are not authorized to create training"}), 403

    # 요청에서 입력 데이터를 가져옴
    data = request.json
    if not data:
        return jsonify({"message": "No input data provided"}), 400

    # 훈련 데이터 생성 (Training 모델에 맞게 데이터를 입력)
    try:
        new_training = Training(**data)
        db.session.add(new_training)  # 새로운 트레이닝 데이터를 DB에 추가
        db.session.commit()  # 트랜잭션 커밋 (DB에 실제 반영)
    except Exception as e:
        db.session.rollback()  # 오류 발생 시 롤백
        return jsonify({"msg": f"Error creating training: {str(e)}"}), 500

    return jsonify({"msg": "Training created", "data": data}), 201

if __name__ == '__main__':
    app.run(debug=True)
