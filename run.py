import os, sys
import click
from flask.cli import FlaskGroup
from flask import Flask
from extensions import init_extensions, db, jwt  # 필요한 확장 기능을 가져옴
from api.routes import routes  # 블루프린트 가져오기


# 애플리케이션 생성 함수
def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')  # 환경설정 파일 로드

    # 확장 기능 초기화
    init_extensions(app)

    # 블루프린트 등록
    app.register_blueprint(routes)
    
    return app


# CLI 명령어 그룹 설정
@click.group(cls=FlaskGroup, create_app=create_app)
def cli():
    pass


# 데이터베이스 초기화 명령어 추가
@cli.command('init_db')
def init_db_command():
    app = create_app()
    with app.app_context():
        db.create_all()  # 데이터베이스 테이블 생성
    click.echo("Database initialized")


# 개발 서버 실행 명령어 추가
@cli.command('dev')
@click.option('--port', default=8000, help='Port to run the server on')
def dev_cmd(port):
    click.echo(f"Running on port {port}")
    os.environ['FLASK_ENV'] = 'development'
    os.environ['FLASK_DEBUG'] = '1'
    app = create_app()
    app.run(port=port, debug=True)


# 메인 실행 코드
if __name__ == "__main__":
    cli()

