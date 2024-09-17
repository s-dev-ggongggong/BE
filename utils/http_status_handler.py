from flask import jsonify

HTTP_STATUS_CODES = {
    200: "성공: 요청이 성공적으로 처리되었습니다.",
    201: "생성됨: 새 리소스가 성공적으로 생성되었습니다.",
    204: "내용 없음: 요청이 성공적으로 처리되었지만 응답 본문이 없습니다.",
    400: "잘못된 요청: 서버가 요청을 이해할 수 없습니다.",
    401: "인증 실패: 인증이 필요합니다.",
    403: "접근 금지: 서버가 요청을 거부했습니다.",
    404: "찾을 수 없음: 요청한 리소스를 찾을 수 없습니다.",
    405: "허용되지 않는 메소드: 해당 엔드포인트에서 허용되지 않는 HTTP 메소드입니다.",
    409: "충돌: 요청이 서버의 현재 상태와 충돌합니다.",
    500: "서버 내부 오류: 서버에 예기치 않은 조건이 발생했습니다."
}

def handle_response(status_code, data=None, message=None):
    """
    HTTP 응답을 생성하는 함수
    :param status_code: HTTP 상태 코드
    :param data: 응답에 포함될 데이터 (선택사항)
    :param message: 사용자 정의 메시지 (선택사항)
    :return: JSON 응답
    """
    response = {
        "status": status_code,
        "data":data,
        "message": message or HTTP_STATUS_CODES.get(status_code, "알 수 없는 상태"),
    }
    
    if data is not None:
        response["data"] = data
    
    return jsonify(response), status_code

def bad_request(message=None):
    return handle_response(400, message=message)

def unauthorized(message=None):
    return handle_response(401, message=message)

def forbidden(message=None):
    return handle_response(403, message=message)

def not_found(message=None):
    return handle_response(404, message=message)

def method_not_allowed(message=None):
    return handle_response(405, message=message)

def conflict(message=None):
    return handle_response(409, message=message)

def server_error(message=None):
    return handle_response(500, message=message)