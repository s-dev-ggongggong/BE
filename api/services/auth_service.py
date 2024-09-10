# File: services/auth_service.py
from flask import jsonify, request
import jwt
from datetime import datetime, timedelta

SECRET_KEY = 'your_secret_key'

# 로그인 로직
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    # 고정된 비밀번호 확인
    if password != 'igloo1234':
        return jsonify({"error": "Invalid credentials"}), 401
    
    # JWT 생성
    token = jwt.encode({
        'email': email,
        'exp': datetime.utcnow() + timedelta(hours=24)  # 24시간 유효한 토큰
    }, SECRET_KEY)
    
    return jsonify({"token": token}), 200

# JWT 인증이 필요한 API 요청에 사용할 데코레이터
def token_required(f):
    from functools import wraps

    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"error": "Token is missing!"}), 401
        
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token!"}), 401
        
        return f(*args, **kwargs)
    
    return decorated_function
