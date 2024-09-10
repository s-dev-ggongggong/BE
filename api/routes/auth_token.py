# File: api/routes/auth_token.py
from flask import Blueprint, request
from api.services.auth_token_service import (
    create_auth_token,
    get_all_auth_tokens,
    get_auth_token,
    update_auth_token,
    delete_auth_token
)

auth_token_bp = Blueprint('auth_token_bp', __name__)

@auth_token_bp.route('/', methods=['POST'])
def create_token():
    return create_auth_token(request.json)

@auth_token_bp.route('/', methods=['GET'])
def get_tokens():
    return get_all_auth_tokens()

@auth_token_bp.route('/<int:id>', methods=['GET'])
def get_token(id):
    return get_auth_token(id)

@auth_token_bp.route('/<int:id>', methods=['PUT'])
def update_token(id):
    return update_auth_token(id, request.json)

@auth_token_bp.route('/<int:id>', methods=['DELETE'])
def delete_token(id):
    return delete_auth_token(id)