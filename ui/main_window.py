
from PySide6.QtGui import QFontDatabase
import os

from PySide6.QtCore import Qt
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


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        font_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "assets",
            "fonts",
            "Cairo-Regular.ttf"
        )

        QFontDatabase.addApplicationFont(
            font_path
        )
        self.setWindowTitle("JOURNAL DESIGNER APP")

        self.resize(560, 720)

        self.setMinimumSize(520, 680)

        self.setLayoutDirection(
            Qt.RightToLeft
        )

        self.research_file = ""

        self.setup_ui()

        self.apply_style()

    # =========================
    # UI
    # =========================

    def setup_ui(self):

        # MAIN LAYOUT
        self.main_layout = QVBoxLayout(self)

        self.main_layout.setContentsMargins(
            25, 25, 25, 25
        )

        self.main_layout.setSpacing(20)

        self.main_layout.setAlignment(
            Qt.AlignTop
        )
        self.main_layout.setDirection(
            QVBoxLayout.TopToBottom
        )
        # =========================
        # CONTAINER
        # =========================

        self.container = QWidget()

        self.container.setObjectName(
            "container"
        )

        self.container_layout = QVBoxLayout(
            self.container
        )

        self.container_layout.setContentsMargins(
            25, 25, 25, 25
        )

        self.container_layout.setSpacing(12)

        self.main_layout.addWidget(
            self.container,
            alignment=Qt.AlignCenter
        )

        # =========================
        # TITLE
        # =========================

        title = QLabel(
            "JOURNAL DESIGNER APP"
        )

        title.setObjectName("title")

        subtitle = QLabel(
            "تصميم أبحاث المجلات العلمية"
        )

        subtitle.setObjectName(
            "subtitle"
        )

        self.container_layout.addWidget(
            title
        )

        self.container_layout.addWidget(
            subtitle
        )

        # =========================
        # JOURNAL
        # =========================

        journal_label = QLabel(
            "المجلة"
        )

        journal_label.setObjectName(
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

        self.container_layout.addWidget(
            journal_label
        )

        self.container_layout.addWidget(
            self.journal_combo
        )

        # =========================
        # LANGUAGE
        # =========================

        lang_label = QLabel(
            "اللغة"
        )

        lang_label.setObjectName(
            "sectionLabel"
        )

        lang_layout = QHBoxLayout()

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

        lang_layout.addWidget(
            self.ar_radio
        )

        lang_layout.addWidget(
            self.en_radio
        )

        lang_layout.addStretch()

        self.container_layout.addWidget(
            lang_label
        )

        self.container_layout.addLayout(
            lang_layout
        )

        # =========================
        # ISSUE
        # =========================

        issue_label = QLabel(
            "العدد"
        )

        issue_label.setObjectName(
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

        self.container_layout.addWidget(
            issue_label
        )

        self.container_layout.addWidget(
            self.issue_combo
        )

        # =========================
        # YEAR
        # =========================

        year_label = QLabel(
            "السنة"
        )

        year_label.setObjectName(
            "sectionLabel"
        )

        self.year_input = QLineEdit()

        self.year_input.setText("2026")

        self.container_layout.addWidget(
            year_label
        )

        self.container_layout.addWidget(
            self.year_input
        )

        # =========================
        # FILE
        # =========================

        file_label = QLabel(
            "ملف البحث"
        )

        file_label.setObjectName(
            "sectionLabel"
        )

        self.file_name = QLabel(
            "لم يتم اختيار ملف"
        )

        self.file_name.setObjectName(
            "fileLabel"
        )

        self.file_name.setWordWrap(True)

        self.file_name.setMinimumHeight(90)

        self.file_name.setAlignment(
            Qt.AlignCenter
        )

        self.file_btn = QPushButton(
            "اختيار ملف DOCX"
        )

        self.file_btn.setObjectName(
            "fileBtn"
        )

        self.file_btn.clicked.connect(
            self.choose_file
        )

        self.container_layout.addWidget(
            file_label
        )

        self.container_layout.addWidget(
            self.file_name
        )

        self.container_layout.addSpacing(8)

        self.container_layout.addWidget(
            self.file_btn
        )

        # =========================
        # PROGRESS
        # =========================

        self.progress = QProgressBar()

        self.progress.setValue(0)

        self.container_layout.addWidget(
            self.progress
        )

        # =========================
        # GENERATE BUTTON
        # =========================

        self.generate_btn = QPushButton(
            "إنشاء العدد"
        )

        self.generate_btn.setObjectName(
            "generateBtn"
        )

        self.generate_btn.clicked.connect(
            self.generate_document
        )

        self.container_layout.addWidget(
            self.generate_btn
        )

        # =========================
        # STATUS
        # =========================

        self.status_label = QLabel(
            "جاهز"
        )

        self.status_label.setObjectName(
            "status"
        )

        self.container_layout.addWidget(
            self.status_label
        )

    # =========================
    # STYLE
    # =========================

    def apply_style(self):

        self.setStyleSheet("""

            QWidget {

                background-color: #0d0d0d;

                color: white;

                font-size: 14px;

                font-family: Cairo;
            }

            #container {

                background-color: #151515;

                border: 1px solid #2a2a2a;

                border-radius: 22px;
            }

            QLabel {
                font-size: 14px;
            }

            #title {

                font-size: 22px;

                font-weight: bold;

                color: white;
            }

            #subtitle {

                font-size: 13px;

                color: #888888;

                margin-bottom: 18px;
            }

            .sectionLabel {

                color: #d0d0d0;

                font-size: 13px;

                font-weight: bold;

                margin-top: 6px;

                margin-bottom: 3px;
            }

            QComboBox,
            QLineEdit {

                background-color: #1f1f1f;

                border: 1px solid #333333;

                border-radius: 12px;

                padding: 12px;

                min-height: 22px;
            }

            QComboBox::drop-down {

                border: none;

                width: 30px;
            }

            QPushButton {

                background-color: #262626;

                border: none;

                border-radius: 14px;

                padding: 10px;

                font-weight: bold;

                min-height: 20px;
            }

            QPushButton:hover {
                background-color: #333333;
            }

            #fileBtn {

                background-color: #252525;

                border-radius: 14px;

                padding: 10px;

                font-size: 14px;

                font-weight: bold;
            }

            #fileBtn:hover {

                background-color: #333333;
            }

            #generateBtn {

                background-color: #c8a46b;

                color: black;

                font-size: 15px;
            }

            #generateBtn:hover {
                background-color: #ddb77a;
            }

            #fileLabel {

                color: #f5f5f5;

                background-color: #181818;

                border: 2px dashed #4a4a4a;

                border-radius: 16px;

                padding: 14px;

                font-size: 13px;

                font-weight: bold;

                min-height: 50px;
            }

            #status {

                color: #aaaaaa;

                font-size: 13px;
            }

            QRadioButton {
                spacing: 8px;
            }

            QProgressBar {

                border: none;

                border-radius: 10px;

                background-color: #1f1f1f;

                text-align: center;

                height: 10px;
            }

            QProgressBar::chunk {

                background-color: #c8a46b;

                border-radius: 10px;
            }

        """)

    # =========================
    # FILE PICKER
    # =========================

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
                f"📄\n{filename}"
            )

    # =========================
    # GENERATE
    # =========================

    def generate_document(self):

        try:

            if not self.research_file:

                QMessageBox.warning(
                    self,
                    "تنبيه",
                    "اختر ملف البحث أولاً"
                )

                return

            self.progress.setValue(20)

            self.status_label.setText(
                "جارٍ تجهيز الملف..."
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

            year = self.year_input.text().strip()

            self.progress.setValue(50)

            QApplication.processEvents()

            output = process_job(
                journal_key=journal_key,
                lang=lang,
                issue_key=issue_key,
                year=year,
                research_file=self.research_file,
            )

            self.progress.setValue(100)

            self.status_label.setText(
                "تم إنشاء الملف بنجاح"
            )

            QMessageBox.information(
                self,
                "تم بنجاح",
                f"تم إنشاء الملف:\n\n{output}"
            )

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