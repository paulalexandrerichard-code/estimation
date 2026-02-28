from __future__ import annotations

import sys

from PySide6.QtWidgets import (
    QApplication,
    QFormLayout,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from plumbing_takeoff.extractor import DEFAULT_MODEL
from plumbing_takeoff.doctor import run_doctor


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Plumbing Takeoff MVP")
        self.api_key = QLineEdit()
        self.api_key.setEchoMode(QLineEdit.Password)
        self.model_name = QLineEdit(DEFAULT_MODEL)
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.doctor_btn = QPushButton("Run doctor")
        self.doctor_btn.clicked.connect(self._on_doctor)

        form = QFormLayout()
        form.addRow("OpenRouter API key", self.api_key)
        form.addRow("Model", self.model_name)

        root = QVBoxLayout()
        root.addLayout(form)
        root.addWidget(self.doctor_btn)
        root.addWidget(self.output)

        container = QWidget()
        container.setLayout(root)
        self.setCentralWidget(container)

    def _on_doctor(self) -> None:
        status = run_doctor()
        self.output.setPlainText("\n".join(f"{k}: {v}" for k, v in status.items()))


def main() -> int:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(720, 480)
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
