from flask import Blueprint, request, jsonify
from api.services.phishing_service import PhishingEvent
from extensions import db

# Blueprint 설정
phishing_bp = Blueprint('phishing_bp', __name__)

# 피싱 링크 생성 엔드포인트
@phishing_bp.route('/generate_phishing_link', methods=['POST'])
def generate_phishing_link_route():
    try:
        # 요청에서 user_id와 training_id 추출
        data = request.get_json()
        user_id = data.get('user_id')
        training_id = data.get('training_id')

        if not user_id or not training_id:
            return jsonify({"error": "user_id and training_id are required"}), 400
        
        # PhishingEvent 클래스를 사용해 피싱 링크 생성
        phishing_event = PhishingEvent(db.session)
        link, status = phishing_event.generate_phishing_link(user_id, training_id)

        return jsonify({"phishing_link": link}), status

    except Exception as e:
        return jsonify({"error": str(e)}), 500
