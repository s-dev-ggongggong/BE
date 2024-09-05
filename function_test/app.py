import os
import secrets
from flask import Flask, request, jsonify, render_template
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

app = Flask(__name__)

# JWT 설정
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', secrets.token_urlsafe(32))
jwt = JWTManager(app)

# 유저 저장소 (임시, 실제로는 DB에서 관리)
users = {
    "testuser": {"password": "password123"}
}

# 루트 라우트 (홈페이지 또는 기본 경로)
@app.route('/')
def home():
    return jsonify({"msg": "Welcome to the API"}), 200

# 로그인 라우트 (GET: 로그인 페이지, POST: 로그인 처리)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        # 로그인 페이지 반환
        return render_template('login.html')
        return jsonify({"msg": "sucess create_login page"}), 200

    
    # POST 요청 처리 (로그인 로직) --> JSON 요청 처리, HTML 폼 데이터 처리
    username = request.json.get('username') if request.is_json else request.form.get('username')
    password = request.json.get('password') if request.is_json else request.form.get('password')
    
    if username not in users or users[username]['password'] != password:
        return jsonify({"msg": "Invalid username or password"}), 401
    
    # JWT 토큰 생성
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200

# Training 생성 라우트 (GET: 트레이닝 생성 페이지, POST: 트레이닝 생성)
@app.route('/training/create', methods=['GET', 'POST'])
@jwt_required()
def create_training():
    if request.method == 'GET':
        # 훈련 생성 페이지 반환
        #return render_template('create_training.html')
        return jsonify({"msg": "sucess create_training homepage"}), 200
    
    
    # POST 요청 처리 (훈련 생성 로직)
    data = request.json
    # 여기에 실제 트레이닝 데이터 생성 로직을 추가
    return jsonify({"msg": "Training created", "data": data}), 201

if __name__ == '__main__':
    # 현재 비밀 키 출력 (개발 중에는 확인 가능, 배포 시엔 비활성화하는 것이 좋음)
    #print(f"JWT Secret Key: {app.config['JWT_SECRET_KEY']}")
    app.run(debug=True)
