import csv
import os
import random
import slicer
import qt
from .AnimatedProgressBar import AnimatedProgressBar

class HelpfulLoadingDialog(qt.QDialog):
    def __init__(self, parent=None, value=0, minimum=0,
                 maximum=100, windowTitle="Loading...",
                 progressText="Loading...",
                 can_cancel=True, hint_location=None,
                 progress_bar_kwargs={}):
        super().__init__()

        self.hints = []
        self.animation_timer = None

        if not hint_location:
            hint_location = slicer.modules.uiuxtoolkittester.widgetRepresentation().self().resourcePath("Hints.csv")
        self.loadHints(hint_location)
        self.setupUI(windowTitle, minimum, maximum, value, progressText, can_cancel, progress_bar_kwargs)
        self.ui = slicer.util.childWidgetVariables(self)
        self.progress_bar.animation_timer.singleShot(0, self.progress_bar.startAnimation)


    def setupUI(self, title, minimum, maximum, value, progressText, can_cancel, progress_bar_kwargs):
        self.windowTitle = title
        self.setWindowFlag(qt.Qt.WindowContextHelpButtonHint, False)

        main_layout = qt.QVBoxLayout()
        self.setLayout(main_layout)

        # Dialog Header
        header_widget = qt.QWidget()
        header_layout = qt.QHBoxLayout(header_widget)

        icon_label = qt.QLabel()
        icon_label.setObjectName("icon_label")
        icon_pixmap = qt.QPixmap(os.path.join(os.path.dirname(__file__), "../Resources/Icons/info_fill.svg"))
        icon_label.setPixmap(icon_pixmap)
        icon_label.setAlignment(qt.Qt.AlignCenter)
        icon_label.setSizePolicy(qt.QSizePolicy.Maximum, qt.QSizePolicy.Fixed)
        header_layout.addWidget(icon_label)

        hint_header_label = qt.QLabel("Hint")
        hint_header_label.setObjectName("hint_header_label")
        header_layout.addWidget(hint_header_label)
        main_layout.addWidget(header_widget)

        # Main Dialog Content
        hint_label = qt.QLabel(self.getRandomHint())
        hint_label.setObjectName("hint_label")
        main_layout.addWidget(hint_label)

        # Progress Bar and Label
        progress_bar = AnimatedProgressBar(**progress_bar_kwargs)
        progress_bar.value = value
        progress_bar.minimum = minimum
        progress_bar.maximum = maximum
        progress_bar.setObjectName("progress_bar")
        main_layout.addWidget(progress_bar)

        progress_label = qt.QLabel(progressText)
        progress_label.setObjectName("progress_label")
        progress_label.setAlignment(qt.Qt.AlignCenter)
        main_layout.addWidget(progress_label)

        # Cancel Button
        if can_cancel:
            button_widget = qt.QWidget()
            button_layout = qt.QHBoxLayout(button_widget)
            button_layout.insertStretch(0)
            main_layout.addWidget(button_widget)

            cancel_button = qt.QPushButton()
            cancel_button.setText("Cancel")
            cancel_button.setObjectName("cancel_button")
            cancel_button.setSizePolicy(qt.QSizePolicy.Maximum, qt.QSizePolicy.Preferred)
            cancel_button.clicked.connect(lambda: self.reject())
            button_layout.addWidget(cancel_button)

    def loadHints(self, file_path):
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.hints.append(row['HintText'])

    def getRandomHint(self):
        if self.hints:
            return random.choice(self.hints)
        else:
            return "Set up helpful hints."
