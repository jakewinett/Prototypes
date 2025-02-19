import sys
import os
from pathlib import Path  # Add this import
import PyQt6
from PyQt6.QtCore import Qt, QLibraryInfo
from PyQt6.QtGui import QIcon
import sqlite3
import datetime

from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QListWidget, QPushButton, QMessageBox, QCheckBox)
from osxphotos import PhotosDB  # Instead of from photos import Photos

class ImportApplePhotos(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Import Apple Photos")
        self.setMinimumSize(800, 600)
        self.photos_library = None
        self.db_conn = None
        self.init_ui()
        self.init_database()
        
    def init_database(self):
        try:
            self.db_conn = sqlite3.connect('photo_library.db')
            self.create_tables()
        except sqlite3.Error as e:
            self.show_error("Database Error", f"Failed to initialize database: {str(e)}")
            sys.exit(1)

    def create_tables(self):
        cursor = self.db_conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS albums (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                date_created DATETIME
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS photos (
                id TEXT PRIMARY KEY,
                album_id TEXT,
                path TEXT,
                thumbnail_path TEXT,
                date_taken DATETIME,
                latitude REAL,
                longitude REAL,
                people TEXT,
                FOREIGN KEY (album_id) REFERENCES albums (id)
            )
        ''')
        self.db_conn.commit()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Album list
        self.album_list = QListWidget()
        layout.addWidget(self.album_list)

        # Buttons
        self.refresh_button = QPushButton("Refresh Albums")
        self.import_button = QPushButton("Import Selected")
        self.update_button = QPushButton("Update Existing")
        
        layout.addWidget(self.refresh_button)
        layout.addWidget(self.import_button)
        layout.addWidget(self.update_button)

        # Connect signals
        self.refresh_button.clicked.connect(self.refresh_albums)
        self.import_button.clicked.connect(self.import_selected_albums)
        self.update_button.clicked.connect(self.update_albums)

    def request_photos_access(self):
        try:
            # Force Photos access prompt by attempting to access the library
            photos_path = os.path.expanduser("~/Pictures/Photos Library.photoslibrary")
            
            # Print debug info
            print(f"Attempting to access Photos library at: {photos_path}")
            print(f"Photos library exists: {os.path.exists(photos_path)}")
            
            self.photos_library = PhotosDB(photos_path)
            
            # Test access by trying to get albums
            albums = self.photos_library.albums
            if not albums:
                print("No albums found - this might indicate a permissions issue")
                raise Exception("No albums found or no access permission")
                
        except Exception as e:
            print(f"Photos access error: {str(e)}")
            self.show_error(
                "Photos Access Error", 
                "Please grant access to Photos in System Settings → Privacy & Security → Photos\n\n"
                "If Photos is not listed, try running the app bundle instead of the Python script directly."
            )
            sys.exit(1)

    def show_error(self, title, message):
        QMessageBox.critical(self, title, message)

    def refresh_albums(self):
        """Refresh the list of albums from Photos library"""
        if not self.photos_library:
            self.request_photos_access()
        
        try:
            self.album_list.clear()
            for album in self.photos_library.albums:
                self.album_list.addItem(album.title)
        except Exception as e:
            self.show_error("Refresh Error", f"Failed to refresh albums: {str(e)}")

    def import_selected_albums(self):
        """Import selected albums from Photos library"""
        selected_items = self.album_list.selectedItems()
        if not selected_items:
            self.show_error("Selection Error", "Please select at least one album to import")
            return
        
        # Implementation for importing selected albums
        pass

    def update_albums(self):
        """Update existing albums with any changes from Photos library"""
        # Implementation for updating albums
        pass

if __name__ == '__main__':
    try:
        # Get Qt library paths
        qt_library_path = QLibraryInfo.path(QLibraryInfo.LibraryPath.PluginsPath)
        
        possible_paths = [
            qt_library_path,
            '/opt/homebrew/opt/qt6/plugins',  # M1 Mac Homebrew path
            '/usr/local/opt/qt6/plugins',     # Intel Mac Homebrew path
            str(Path(PyQt6.__file__).parent / "Qt6" / "plugins"),  # PyQt6 package path
        ]
        
        # Debug: Print all potential paths
        for path in possible_paths:
            print(f"Checking path: {path}")
            if os.path.exists(path):
                print(f"Path exists: {path}")
                if os.path.exists(os.path.join(path, 'platforms')):
                    print(f"Platforms directory found at: {path}/platforms")
                    print(f"Contents: {os.listdir(os.path.join(path, 'platforms'))}")
        
        # Find first existing path
        qt_plugins_path = next((path for path in possible_paths if os.path.exists(path)), None)
        
        if not qt_plugins_path:
            raise RuntimeError("Could not find Qt plugins directory")
        
        # Set environment variables before QApplication
        os.environ['QT_QPA_PLATFORM'] = 'cocoa'
        os.environ['QT_PLUGIN_PATH'] = qt_plugins_path
        os.environ['QT_DEBUG_PLUGINS'] = '1'
        
        print(f"Using Qt plugins from: {qt_plugins_path}")
        
        app = QApplication(sys.argv)
        app.setApplicationName("Photo Import")
        app.setOrganizationName("Your Organization")
        app.setOrganizationDomain("your-domain.com")
        
        window = ImportApplePhotos()
        window.show()
        window.request_photos_access()
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"Error initializing application: {e}")
        sys.exit(1)