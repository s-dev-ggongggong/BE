from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError
from functools import wraps
import time
from utils.logger import setup_logger

logger = setup_logger(__name__)

def handle_db_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        retries = 5
        while retries > 0:
            try:
                return func(*args, **kwargs)
            
            except IntegrityError as e:
                logger.error(f"IntegrityError: {str(e)}")
                from extensions import db
                db.session.rollback()
                break
            except OperationalError as e:
                if "database is locked" in str(e):
                    retries -= 1
                    logger.warning(f"Database locked, retrying... ({retries} retries left)")
                    time.sleep(0.5)
                    from extensions import db
                    db.session.rollback()
                else:
                    logger.error(f"OperationalError: {str(e)}")
                    raise
            except SQLAlchemyError as e:
                logger.error(f"Database error occurred: {str(e)}")
                from extensions import db
                db.session.rollback()
                break
            except Exception as e:
                logger.error(f"An unexpected error occurred: {str(e)}", exc_info=True)
                from extensions import db
                db.session.rollback()
                break
        return None
    return wrapper