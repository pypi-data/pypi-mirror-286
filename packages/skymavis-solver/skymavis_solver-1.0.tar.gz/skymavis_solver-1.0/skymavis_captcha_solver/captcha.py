from .vision import is_correct_orientation
import logging

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('captcha_bypass.log')
    ]
)

logger = logging.getLogger(__name__)

def bypass_captcha(file_path):
    logger.info('Processing file: %s', file_path)
    
    if is_correct_orientation(file_path):
        logger.info('CAPTCHA is correctly oriented.')
        return True
    else:
        logger.warning('CAPTCHA is not correctly oriented.')
        return False
