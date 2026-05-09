# =========================================================
# JOURNAL DESIGNER APP
# Main Window UI
# =========================================================

import os

from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QFontDatabase,
    QIntValidator,
)

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QComboBox,
    QLineEdit,
    QRadioButton,
    QButtonGroup,
    QProgressBar,
    QApplication,
)

from core.processor import (
    JOURNALS,
    ISSUE_CODES,
    process_job,
)


# =========================================================
# MAIN WINDOW
# =========================================================

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.research_file = ""

        self.load_fonts()

        self.setup_window()

        self.setup_ui()

        self.apply_style()

    # =====================================================
    # WINDOW SETUP
    # =====================================================

    def setup_window(self):

        self.setWindowTitle(
            "JOURNAL DESIGNER APP"
        )

        self.resize(850, 650)

        self.setMinimumSize(800, 550)

        self.setLayoutDirection(
            Qt.RightToLeft
        )

    # =====================================================
    # LOAD FONTS
    # =====================================================

    def load_fonts(self):

        font_path = os.path.join(
            os.path.dirname(
                os.path.dirname(__file__)
            ),
            "assets",
            "fonts",
            "Cairo-Regular.ttf"
        )

        QFontDatabase.addApplicationFont(
            font_path
        )

    # =====================================================
    # UI
    # =====================================================

    def setup_ui(self):

        # MAIN LAYOUT
        self.main_layout = QVBoxLayout(self)

        self.main_layout.setContentsMargins(
            30, 30, 30, 30
        )

        self.main_layout.setAlignment(
            Qt.AlignCenter
        )

        # CONTAINER CARD
        self.container = QWidget()

        self.container.setObjectName(
            "container"
        )

        self.container.setFixedWidth(750)

        self.container_layout = QVBoxLayout(
            self.container
        )

        self.container_layout.setContentsMargins(
            35, 35, 35, 35
        )

        self.container_layout.setSpacing(20)

        self.main_layout.addWidget(
            self.container
        )

        # HEADER
        self.build_header()

        # JOURNAL + LANGUAGE
        self.build_row_one()

        # ISSUE + YEAR
        self.build_row_two()

        # FILE SECTION
        self.build_file_section()

        # ACTIONS
        self.build_actions_section()

    # =====================================================
    # HEADER
    # =====================================================

    def build_header(self):

        header_layout = QVBoxLayout()

        title = QLabel(
            "JOURNAL DESIGNER APP"
        )

        title.setObjectName("title")

        subtitle = QLabel(
            "تصميم أبحاث المجلات العلمية - لوحة التحكم"
        )

        subtitle.setObjectName(
            "subtitle"
        )

        header_layout.addWidget(title)

        header_layout.addWidget(subtitle)

        self.container_layout.addLayout(
            header_layout
        )

    # =====================================================
    # ROW 1
    # JOURNAL + LANGUAGE
    # =====================================================

    def build_row_one(self):

        row_layout = QHBoxLayout()

        row_layout.setSpacing(20)

        # =========================
        # JOURNAL
        # =========================

        journal_layout = QVBoxLayout()

        journal_label = QLabel("المجلة")

        journal_label.setProperty(
            "class",
            "sectionLabel"
        )

        self.journal_combo = QComboBox()

        for key, data in JOURNALS.items():

            name = (
                data.get("name_ar")
                or data.get("name_en")
                or key
            )

            self.journal_combo.addItem(
                name,
                key
            )

        journal_layout.addWidget(
            journal_label
        )

        journal_layout.addWidget(
            self.journal_combo
        )

        # =========================
        # LANGUAGE
        # =========================

        lang_layout = QVBoxLayout()

        lang_label = QLabel(
            "لغة البحث"
        )

        lang_label.setProperty(
            "class",
            "sectionLabel"
        )

        lang_buttons_layout = QHBoxLayout()

        self.ar_radio = QRadioButton(
            "العربية"
        )

        self.en_radio = QRadioButton(
            "English"
        )

        self.ar_radio.setChecked(True)

        self.lang_group = QButtonGroup(
            self
        )

        self.lang_group.addButton(
            self.ar_radio
        )

        self.lang_group.addButton(
            self.en_radio
        )

        lang_buttons_layout.addWidget(
            self.ar_radio
        )

        lang_buttons_layout.addWidget(
            self.en_radio
        )

        lang_layout.addWidget(
            lang_label
        )

        lang_layout.addLayout(
            lang_buttons_layout
        )

        # ADD TO ROW

        row_layout.addLayout(
            journal_layout,
            2
        )

        row_layout.addLayout(
            lang_layout,
            1
        )

        self.container_layout.addLayout(
            row_layout
        )

    # =====================================================
    # ROW 2
    # ISSUE + YEAR
    # =====================================================

    def build_row_two(self):

        row_layout = QHBoxLayout()

        row_layout.setSpacing(20)

        # =========================
        # ISSUE
        # =========================

        issue_layout = QVBoxLayout()

        issue_label = QLabel("العدد")

        issue_label.setProperty(
            "class",
            "sectionLabel"
        )

        self.issue_combo = QComboBox()

        for key in ISSUE_CODES:

            month_name = ISSUE_CODES[key][
                "month_ar"
            ]

            self.issue_combo.addItem(
                month_name,
                key
            )

        issue_layout.addWidget(
            issue_label
        )

        issue_layout.addWidget(
            self.issue_combo
        )

        # =========================
        # YEAR
        # =========================

        year_layout = QVBoxLayout()

        year_label = QLabel(
            "سنة النشر"
        )

        year_label.setProperty(
            "class",
            "sectionLabel"
        )

        self.year_input = QLineEdit()

        self.year_input.setText("2026")

        self.year_input.setValidator(
            QIntValidator(2000, 2100)
        )

        year_layout.addWidget(
            year_label
        )

        year_layout.addWidget(
            self.year_input
        )

        # ADD TO ROW

        row_layout.addLayout(
            issue_layout,
            2
        )

        row_layout.addLayout(
            year_layout,
            1
        )

        self.container_layout.addLayout(
            row_layout
        )

    # =====================================================
    # FILE SECTION
    # =====================================================

    def build_file_section(self):

        file_layout = QHBoxLayout()

        file_layout.setSpacing(15)

        self.file_name = QLabel(
            "لم يتم اختيار ملف"
        )

        self.file_name.setObjectName(
            "fileLabel"
        )

        self.file_name.setAlignment(
            Qt.AlignCenter
        )

        self.file_btn = QPushButton(
            "اختيار ملف DOCX"
        )

        self.file_btn.setObjectName(
            "fileBtn"
        )

        self.file_btn.setFixedWidth(180)

        self.file_btn.clicked.connect(
            self.choose_file
        )

        file_layout.addWidget(
            self.file_name,
            1
        )

        file_layout.addWidget(
            self.file_btn
        )

        self.container_layout.addLayout(
            file_layout
        )

    # =====================================================
    # ACTIONS SECTION
    # =====================================================

    def build_actions_section(self):

        self.progress = QProgressBar()

        self.progress.setValue(0)

        self.container_layout.addWidget(
            self.progress
        )

        self.generate_btn = QPushButton(
            "إنشاء وتنسيق البحث"
        )

        self.generate_btn.setObjectName(
            "generateBtn"
        )

        self.generate_btn.setMinimumHeight(
            50
        )

        self.generate_btn.clicked.connect(
            self.generate_document
        )

        self.container_layout.addWidget(
            self.generate_btn
        )

        self.status_label = QLabel(
            "جاهز للعمل"
        )

        self.status_label.setObjectName(
            "status"
        )

        self.container_layout.addWidget(
            self.status_label,
            alignment=Qt.AlignCenter
        )

    # =====================================================
    # STYLE
    # =====================================================

    def apply_style(self):

        self.setStyleSheet("""

            QWidget {
                background-color: #0d0d0d;
                color: white;
                font-family: Cairo, Segoe UI;
            }

            #container {
                background-color: #151515;
                border: 1px solid #2a2a2a;
                border-radius: 20px;
            }

            #title {
                font-size: 26px;
                font-weight: bold;
                color: #ffffff;
            }

            #subtitle {
                font-size: 14px;
                color: #888888;
                margin-bottom: 10px;
            }

            QLabel[class="sectionLabel"] {
                color: #c8a46b;
                font-size: 13px;
                font-weight: bold;
            }

            QComboBox,
            QLineEdit {
                background-color: #1f1f1f;
                border: 1px solid #333333;
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
                min-height: 22px;
            }

            QComboBox:focus,
            QLineEdit:focus {
                border: 1px solid #c8a46b;
                background-color: #252525;
            }

            QPushButton {
                background-color: #262626;
                border-radius: 10px;
                padding: 12px;
                font-weight: bold;
                font-size: 14px;
            }

            QPushButton:hover {
                background-color: #333333;
            }

            #fileBtn {
                background-color: #2a2a2a;
                border: 1px solid #3d3d3d;
            }

            #generateBtn {
                background-color: #c8a46b;
                color: black;
                font-size: 16px;
                margin-top: 10px;
            }

            #generateBtn:hover {
                background-color: #ddb77a;
            }

            #fileLabel {
                background-color: #111111;
                border: 2px dashed #333333;
                border-radius: 10px;
                padding: 10px;
                color: #aaaaaa;
                font-style: italic;
                min-height: 40px;
            }

            QProgressBar {
                border: none;
                border-radius: 4px;
                background-color: #1a1a1a;
                height: 8px;
                text-align: center;
                font-size: 0px;
            }

            QProgressBar::chunk {
                background-color: #c8a46b;
                border-radius: 4px;
            }

            QRadioButton {
                font-size: 13px;
                spacing: 6px;
            }

            #status {
                color: #666666;
                font-size: 12px;
            }

        """)

    # =====================================================
    # FILE PICKER
    # =====================================================

    def choose_file(self):

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "اختر ملف البحث",
            "",
            "Word Files (*.docx)"
        )

        if file_path:

            self.research_file = file_path

            filename = os.path.basename(
                file_path
            )

            self.file_name.setText(
                f"📄 {filename}"
            )

            self.file_name.setStyleSheet("""
                color: #c8a46b;
                font-style: normal;
                border-color: #c8a46b;
            """)

    # =====================================================
    # GENERATE DOCUMENT
    # =====================================================

    def generate_document(self):

        try:

            if not self.research_file:

                QMessageBox.warning(
                    self,
                    "تنبيه",
                    "برجاء اختيار ملف البحث أولاً"
                )

                return

            self.progress.setValue(20)

            self.status_label.setText(
                "جارٍ المعالجة..."
            )

            QApplication.processEvents()

            journal_key = (
                self.journal_combo.currentData()
            )

            lang = (
                "ar"
                if self.ar_radio.isChecked()
                else "en"
            )

            issue_key = (
                self.issue_combo.currentData()
            )

            year = (
                self.year_input.text().strip()
            )

            output = process_job(
                journal_key=journal_key,
                lang=lang,
                issue_key=issue_key,
                year=year,
                research_file=self.research_file,
            )

            self.progress.setValue(100)

            self.status_label.setText(
                "تمت العملية بنجاح"
            )

            QMessageBox.information(
                self,
                "تم بنجاح",
                f"تم إنشاء الملف بنجاح:\n{output}"
            )

            os.startfile(output)

        except Exception as e:

            self.progress.setValue(0)

            self.status_label.setText(
                "حدث خطأ"
            )

            QMessageBox.critical(
                self,
                "خطأ",
                str(e)
            )


# =========================================================
# TEST RUN
# =========================================================

if __name__ == "__main__":

    import sys

    app = QApplication(sys.argv)

    window = MainWindow()

    window.show()

    sys.exit(app.exec())