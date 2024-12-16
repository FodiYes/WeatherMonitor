#!/usr/bin/env python3
import sys
import os
import logging
from PyQt5.QtWidgets import QApplication
from qt_material import apply_stylesheet
from ui.main_window import MainWindow
from api.weather_api import WeatherAPI
from data.data_manager import DataManager

def setup_logging():
    logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
    os.makedirs(logs_dir, exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(os.path.join(logs_dir, 'weather_app.log')),
            logging.StreamHandler()
        ]
    )

def main():
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting Weather Monitoring Application")
    
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_teal.xml')
    app.setStyle("Fusion")
    
    try:
        api = WeatherAPI()
        data_manager = DataManager()
        window = MainWindow()
        
        window.set_api(api)
        window.set_data_manager(data_manager)
        
        window.show()
        
        logger.info("Application started successfully")
        sys.exit(app.exec_())
        
    except Exception as e:
        logger.error(f"Error starting application: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
