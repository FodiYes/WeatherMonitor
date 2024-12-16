#!/usr/bin/env python3
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QPushButton, QLabel, QLineEdit,
                            QScrollArea, QFrame, QGridLayout)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont

class WindowButtons(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(8)

        self.close_button = QPushButton()
        self.minimize_button = QPushButton()
        self.maximize_button = QPushButton()

        for button in [self.close_button, self.minimize_button, self.maximize_button]:
            button.setFixedSize(12, 12)
            button.setStyleSheet("""
                QPushButton {
                    border: none;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    opacity: 0.8;
                }
            """)

        self.close_button.setStyleSheet(self.close_button.styleSheet() + """
            QPushButton {
                background-color: #FF5F57;
            }
        """)
        self.minimize_button.setStyleSheet(self.minimize_button.styleSheet() + """
            QPushButton {
                background-color: #FFBD2E;
            }
        """)
        self.maximize_button.setStyleSheet(self.maximize_button.styleSheet() + """
            QPushButton {
                background-color: #28C940;
            }
        """)

        layout.addWidget(self.close_button)
        layout.addWidget(self.minimize_button)
        layout.addWidget(self.maximize_button)
        layout.addStretch()
        
        self.setLayout(layout)

class WeatherCard(QFrame):
    removed = pyqtSignal(str)
    
    def __init__(self, city_name, weather_data, parent=None):
        super().__init__(parent)
        self.city_name = city_name
        self.weather_data = weather_data
        self.forecast_data = None
        self.is_expanded = False
        self.forecast_widget = None
        self.setup_ui()
        
    def setup_ui(self):
        self.setObjectName("weatherCard")
        self.setStyleSheet("""
            QFrame#weatherCard {
                background-color: rgba(33, 37, 43, 0.95);
                border-radius: 15px;
                padding: 15px;
                margin: 5px;
            }
            QLabel { color: #c3ccdf; }
            QPushButton {
                background-color: rgba(255, 0, 0, 0.1);
                border: none;
                padding: 8px;
                border-radius: 5px;
                color: #ff6b6b;
            }
            QPushButton:hover {
                background-color: rgba(255, 0, 0, 0.2);
            }
            QPushButton#expandButton {
                background-color: transparent;
                font-size: 16px;
                color: #c3ccdf;
            }
            QPushButton#expandButton:hover {
                color: #bd93f9;
            }
        """)
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(10)
        
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        city_label = QLabel(self.city_name)
        city_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        header_layout.addWidget(city_label)
        
        expand_btn = QPushButton("▼")
        expand_btn.setObjectName("expandButton")
        expand_btn.setFixedSize(30, 30)
        expand_btn.clicked.connect(self.toggle_forecast)
        header_layout.addWidget(expand_btn)
        
        remove_btn = QPushButton("✕")
        remove_btn.setFixedSize(30, 30)
        remove_btn.clicked.connect(lambda: self.removed.emit(self.city_name))
        header_layout.addWidget(remove_btn)
        
        self.main_layout.addWidget(header)
        
        weather_widget = QWidget()
        weather_layout = QHBoxLayout(weather_widget)
        
        temp = self.weather_data.get('temperature', 'N/A')
        temp_label = QLabel(f"{temp}°C")
        temp_label.setFont(QFont("Segoe UI", 32))
        weather_layout.addWidget(temp_label)
        
        details_widget = QWidget()
        details_layout = QVBoxLayout(details_widget)
        details_layout.setSpacing(5)
        
        desc = self.weather_data.get('description', 'N/A')
        desc_label = QLabel(desc)
        desc_label.setFont(QFont("Segoe UI", 12))
        details_layout.addWidget(desc_label)
        
        metrics_widget = QWidget()
        metrics_layout = QHBoxLayout(metrics_widget)
        metrics_layout.setSpacing(20)
        
        humidity = self.weather_data.get('humidity', 'N/A')
        humidity_label = QLabel(f"💧 {humidity}%")
        metrics_layout.addWidget(humidity_label)
        
        wind = self.weather_data.get('wind_speed', 'N/A')
        wind_label = QLabel(f"💨 {wind} m/s")
        metrics_layout.addWidget(wind_label)
        
        details_layout.addWidget(metrics_widget)
        weather_layout.addWidget(details_widget)
        self.main_layout.addWidget(weather_widget)
        
        self.forecast_widget = QWidget()
        self.forecast_widget.hide()
        forecast_layout = QVBoxLayout(self.forecast_widget)
        
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("background-color: rgba(189, 147, 249, 0.3);")
        forecast_layout.addWidget(separator)
        
        forecast_title = QLabel("7-Day Forecast")
        forecast_title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        forecast_layout.addWidget(forecast_title)
        
        self.forecast_data = None
        self.forecast_layout = QVBoxLayout()
        forecast_layout.addLayout(self.forecast_layout)
        self.main_layout.addWidget(self.forecast_widget)
    
    def update_forecast(self, forecast_data):
        self.forecast_data = forecast_data
        
        for i in reversed(range(self.forecast_layout.count())): 
            widget = self.forecast_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        for day in forecast_data:
            day_widget = QWidget()
            day_layout = QHBoxLayout(day_widget)
            
            date = datetime.strptime(day['date'], "%Y-%m-%d").strftime("%a, %b %d")
            date_label = QLabel(date)
            date_label.setMinimumWidth(100)
            day_layout.addWidget(date_label)
            
            temp_label = QLabel(f"{day['temp_min']}°C - {day['temp_max']}°C")
            temp_label.setMinimumWidth(100)
            day_layout.addWidget(temp_label)
            
            desc_label = QLabel(day['description'])
            desc_label.setMinimumWidth(150)
            day_layout.addWidget(desc_label)
            
            prob_label = QLabel(f"🌧️ {day['precipitation_prob']}%")
            day_layout.addWidget(prob_label)
            
            wind_label = QLabel(f"💨 {day['wind_speed']} m/s")
            day_layout.addWidget(wind_label)
            
            day_layout.addStretch()
            self.forecast_layout.addWidget(day_widget)
    
    def toggle_forecast(self):
        self.is_expanded = not self.is_expanded
        self.forecast_widget.setVisible(self.is_expanded)
        
        button = self.findChild(QPushButton, "expandButton")
        if button:
            button.setText("▼" if not self.is_expanded else "▲")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.api = None
        self.data_manager = None
        self.weather_cards = {}
        self.dragging = False
        self.drag_position = None
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Weather Monitor")
        self.setMinimumSize(1000, 600)
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Add window buttons at the top
        title_bar = QWidget()
        title_bar_layout = QHBoxLayout(title_bar)
        title_bar_layout.setContentsMargins(0, 0, 0, 0)
        
        self.window_buttons = WindowButtons()
        self.window_buttons.close_button.clicked.connect(self.close)
        self.window_buttons.minimize_button.clicked.connect(self.showMinimized)
        self.window_buttons.maximize_button.clicked.connect(self.toggle_maximize)
        
        title_bar_layout.addWidget(self.window_buttons)
        title_bar_layout.addStretch()
        
        main_layout.addWidget(title_bar)
        
        # Main content
        content_layout = QHBoxLayout()
        content_layout.setSpacing(0)
        
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setStyleSheet("""
            QFrame#sidebar {
                background-color: rgb(33, 37, 43);
                border-right: 1px solid rgba(255, 255, 255, 0.1);
            }
            QLabel { color: #c3ccdf; }
            QLineEdit {
                padding: 10px;
                border-radius: 8px;
                background-color: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                color: #c3ccdf;
            }
            QLineEdit:focus {
                border: 1px solid #bd93f9;
                background-color: rgba(189, 147, 249, 0.1);
            }
            QPushButton {
                padding: 10px;
                border: none;
                border-radius: 8px;
                color: #c3ccdf;
                background-color: rgba(189, 147, 249, 0.2);
            }
            QPushButton:hover {
                background-color: rgba(189, 147, 249, 0.3);
                color: white;
            }
        """)
        sidebar.setFixedWidth(250)
        
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(20, 20, 20, 20)
        sidebar_layout.setSpacing(15)
        
        title = QLabel("Weather Monitor")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        sidebar_layout.addWidget(title)
        
        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText("Enter city name")
        self.city_input.returnPressed.connect(self.add_city)
        sidebar_layout.addWidget(self.city_input)
        
        add_btn = QPushButton("Add City")
        add_btn.clicked.connect(self.add_city)
        sidebar_layout.addWidget(add_btn)
        
        self.status_label = QLabel()
        self.status_label.setStyleSheet("color: #ff6b6b;")
        self.status_label.setWordWrap(True)
        sidebar_layout.addWidget(self.status_label)
        
        sidebar_layout.addStretch()
        
        self.update_time_label = QLabel("Last updated: Never")
        self.update_time_label.setStyleSheet("color: rgba(255, 255, 255, 0.5);")
        sidebar_layout.addWidget(self.update_time_label)
        
        content_layout.addWidget(sidebar)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
            }
            QWidget#scrollContent {
                background-color: rgb(40, 44, 52);
            }
            QScrollBar:vertical {
                border: none;
                background-color: rgb(33, 37, 43);
                width: 10px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background-color: rgba(189, 147, 249, 0.3);
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: rgba(189, 147, 249, 0.5);
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)
        
        scroll_content = QWidget()
        scroll_content.setObjectName("scrollContent")
        self.cards_layout = QVBoxLayout(scroll_content)
        self.cards_layout.setContentsMargins(20, 20, 20, 20)
        self.cards_layout.setSpacing(15)
        self.cards_layout.addStretch()
        
        scroll.setWidget(scroll_content)
        content_layout.addWidget(scroll)
        
        main_layout.addLayout(content_layout)
        
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_weather)
        self.update_timer.start(600000)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.dragging:
            self.move(event.globalPos() - self.drag_position)

    def mouseReleaseEvent(self, event):
        self.dragging = False

    def toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()
    
    def set_api(self, api):
        self.api = api
    
    def set_data_manager(self, data_manager):
        self.data_manager = data_manager
        for city in self.data_manager.load_cities():
            self.add_city(city)
    
    def add_city(self, city_name=None):
        if not city_name:
            city_name = self.city_input.text().strip()
            if not city_name:
                return
            self.city_input.clear()
        
        if city_name in self.weather_cards:
            self.status_label.setText(f"City '{city_name}' is already added!")
            return
        
        weather_data = self.api.get_current_weather(city_name)
        if not weather_data:
            self.status_label.setText(f"Could not find weather data for '{city_name}'")
            return
        
        forecast_data = self.api.get_forecast(city_name)
        self.status_label.setText("")
        
        card = WeatherCard(city_name, weather_data)
        if forecast_data:
            card.update_forecast(forecast_data)
        card.removed.connect(self.remove_city)
        self.weather_cards[city_name] = card
        self.cards_layout.insertWidget(self.cards_layout.count() - 1, card)
        
        self.data_manager.add_city(city_name)
        self.update_time_label.setText(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")
    
    def remove_city(self, city_name):
        if city_name in self.weather_cards:
            card = self.weather_cards.pop(city_name)
            self.cards_layout.removeWidget(card)
            card.deleteLater()
            self.data_manager.remove_city(city_name)
    
    def update_weather(self):
        for city_name in list(self.weather_cards.keys()):
            weather_data = self.api.get_current_weather(city_name)
            forecast_data = self.api.get_forecast(city_name)
            
            if weather_data:
                old_card = self.weather_cards.pop(city_name)
                self.cards_layout.removeWidget(old_card)
                old_card.deleteLater()
                
                card = WeatherCard(city_name, weather_data)
                if forecast_data:
                    card.update_forecast(forecast_data)
                card.removed.connect(self.remove_city)
                self.weather_cards[city_name] = card
                self.cards_layout.insertWidget(self.cards_layout.count() - 1, card)
        
        self.update_time_label.setText(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")
