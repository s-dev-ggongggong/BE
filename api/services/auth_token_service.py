from extensions import db
from models.auth_token import AuthToken
from models.schemas import auth_token_schema, auth_tokens_schema
from utils.http_status_handler import handle_response, bad_request, server_error
from sqlalchemy.exc import SQLAlchemyError

# AuthToken 생성
def create_auth_token(data):
    try:
        if not data:
            return bad_request("요청 본문이 비어있습니다.")
        new_token = AuthToken(**data)
        db.session.add(new_token)
        db.session.commit()
        return handle_response(201, data=auth_token_schema.dump(new_token), message="AuthToken이 성공적으로 생성되었습니다.")
    except SQLAlchemyError as e:
        db.session.rollback()
        return server_error(f"AuthToken 생성 중 오류 발생: {str(e)}")

# 모든 AuthToken 조회
def get_all_auth_tokens():
    try:
        tokens = AuthToken.query.all()
        return handle_response(200, data=auth_tokens_schema.dump(tokens), message="모든 AuthToken을 성공적으로 조회했습니다.")
    except SQLAlchemyError as e:
        return server_error(f"AuthToken 조회 중 오류 발생: {str(e)}")

# 특정 AuthToken 조회
def get_auth_token(token_id):
    try:
        token = AuthToken.query.get_or_404(token_id)
        return handle_response(200, data=auth_token_schema.dump(token), message="AuthToken을 성공적으로 조회했습니다.")
    except SQLAlchemyError as e:
        return server_error(f"AuthToken 조회 중 오류 발생: {str(e)}")

# AuthToken 업데이트
def update_auth_token(token_id, data):
    try:
        token = AuthToken.query.get_or_404(token_id)
        for key, value in data.items():
            setattr(token, key, value)
        db.session.commit()
        return handle_response(200, data=auth_token_schema.dump(token), message="AuthToken이 성공적으로 업데이트되었습니다.")
    except SQLAlchemyError as e:
        db.session.rollback()
        return server_error(f"AuthToken 업데이트 중 오류 발생: {str(e)}")

# AuthToken 삭제
def delete_auth_token(token_id):
    try:
        token = AuthToken.query.get_or_404(token_id)
        db.session.delete(token)
        db.session.commit()
        return handle_response(200, data=True, message="AuthToken이 성공적으로 삭제되었습니다.")
    except SQLAlchemyError as e:
        db.session.rollback()
        return server_error(f"AuthToken 삭제 중 오류 발생: {str(e)}")
def load_auth_tokens(json_data):
    for token_data in json_data:
        new_token = AuthToken(
            token=token_data['token'],
            employee_id=token_data['employee_id'],
            created_at=token_data['created_at'],
            expires_at=token_data['expires_at']
        )
        db.session.add(new_token)
    db.session.commit()
