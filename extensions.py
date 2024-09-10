# extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from contextlib import contextmanager

# 확장 기능 인스턴스 생성
jwt = JWTManager()
db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()

# 애플리케이션과 확장 기능 연결
def init_extensions(app):
    db.init_app(app)  # SQLAlchemy 초기화
    ma.init_app(app)  # Marshmallow 초기화
    jwt.init_app(app)  # JWTManager 초기화
    migrate.init_app(app, db)  # 데이터베이스 마이그레이션 초기화

# 데이터베이스 세션 관리 함수
@contextmanager
def session_scope():
    session = db.session
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()
