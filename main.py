import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit,
    QVBoxLayout, QHBoxLayout, QPushButton, QComboBox,
    QGroupBox, QMessageBox
)
from PyQt5.QtCore import Qt


class MyProject(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Настройка главного окна
        self.setWindowTitle("Расчет потребности в азотных удобрениях")
        self.setGeometry(200, 200, 700, 700)
        self.setFixedSize(700, 700)

        # Центральный виджет и главный макет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # ========== Заголовок ==========
        title_label = QLabel("РАСЧЕТ ПОТРЕБНОСТИ В АЗОТНЫХ УДОБРЕНИЯХ")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: darkgreen;")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # ========== Группа ввода данных ==========
        input_group = QGroupBox("Входные данные")
        input_layout = QVBoxLayout()

        # Тип культуры (выпадающий список)
        culture_layout = QHBoxLayout()
        culture_layout.addWidget(QLabel("Тип культуры:"))
        self.culture_combo = QComboBox()
        self.culture_combo.addItems(["Ячмень", "Пшеница", "Кукуруза"])
        self.culture_combo.currentTextChanged.connect(self.on_culture_changed)
        culture_layout.addWidget(self.culture_combo)
        culture_layout.addStretch()
        input_layout.addLayout(culture_layout)

        # Площадь (га)
        area_layout = QHBoxLayout()
        area_layout.addWidget(QLabel("Площадь, га:"))
        self.area_input = QLineEdit()
        self.area_input.setPlaceholderText("Введите площадь в гектарах")
        area_layout.addWidget(self.area_input)
        area_layout.addStretch()
        input_layout.addLayout(area_layout)

        # Норма внесения на 1 га (автоматически подставляется)
        norm_layout = QHBoxLayout()
        norm_layout.addWidget(QLabel("Норма внесения на 1 га, кг:"))
        self.norm_label = QLabel("60")
        self.norm_label.setStyleSheet("font-weight: bold; color: blue;")
        norm_layout.addWidget(self.norm_label)
        norm_layout.addStretch()
        input_layout.addLayout(norm_layout)

        input_group.setLayout(input_layout)
        main_layout.addWidget(input_group)

        # ========== Группа кнопок расчета ==========
        calc_group = QGroupBox("Расчет потребности")
        calc_layout = QHBoxLayout()

        self.calc_btn = QPushButton("Рассчитать потребность")
        self.calc_btn.clicked.connect(self.calculate_need)
        calc_layout.addWidget(self.calc_btn)

        self.main_btn = QPushButton("Основное внесение (50%)")
        self.main_btn.clicked.connect(self.calculate_main)
        calc_layout.addWidget(self.main_btn)

        calc_group.setLayout(calc_layout)
        main_layout.addWidget(calc_group)

        # ========== Группа дополнительных расчетов ==========
        extra_group = QGroupBox("Дополнительные расчеты")
        extra_layout = QHBoxLayout()

        self.pre_sowing_btn = QPushButton("Припосевное внесение (25%)")
        self.pre_sowing_btn.clicked.connect(self.calculate_pre_sowing)
        extra_layout.addWidget(self.pre_sowing_btn)

        self.top_dressing_btn = QPushButton("Подкормка (25%)")
        self.top_dressing_btn.clicked.connect(self.calculate_top_dressing)
        extra_layout.addWidget(self.top_dressing_btn)

        extra_group.setLayout(extra_layout)
        main_layout.addWidget(extra_group)

        # ========== Поля вывода результатов ==========
        result_group = QGroupBox("Результаты расчетов")
        result_layout = QVBoxLayout()

        # Общая потребность
        need_layout = QHBoxLayout()
        need_layout.addWidget(QLabel("Общая потребность в удобрениях, ц:"))
        self.need_result = QLineEdit()
        self.need_result.setReadOnly(True)
        self.need_result.setStyleSheet("background-color: #f0f0f0; font-weight: bold; color: darkblue;")
        need_layout.addWidget(self.need_result)
        result_layout.addLayout(need_layout)

        # Основное внесение
        main_layout_res = QHBoxLayout()
        main_layout_res.addWidget(QLabel("Основное внесение (50%), ц:"))
        self.main_result = QLineEdit()
        self.main_result.setReadOnly(True)
        self.main_result.setStyleSheet("background-color: #f0f0f0;")
        main_layout_res.addWidget(self.main_result)
        result_layout.addLayout(main_layout_res)

        # Припосевное внесение
        pre_sowing_layout = QHBoxLayout()
        pre_sowing_layout.addWidget(QLabel("Припосевное внесение (25%), ц:"))
        self.pre_sowing_result = QLineEdit()
        self.pre_sowing_result.setReadOnly(True)
        self.pre_sowing_result.setStyleSheet("background-color: #f0f0f0;")
        pre_sowing_layout.addWidget(self.pre_sowing_result)
        result_layout.addLayout(pre_sowing_layout)

        # Подкормка
        top_dressing_layout = QHBoxLayout()
        top_dressing_layout.addWidget(QLabel("Подкормка (25%), ц:"))
        self.top_dressing_result = QLineEdit()
        self.top_dressing_result.setReadOnly(True)
        self.top_dressing_result.setStyleSheet("background-color: #f0f0f0;")
        top_dressing_layout.addWidget(self.top_dressing_result)
        result_layout.addLayout(top_dressing_layout)

        result_group.setLayout(result_layout)
        main_layout.addWidget(result_group)

        # ========== Кнопка График ==========
        self.graph_btn = QPushButton("Построить график сравнения с прошлыми годами")
        self.graph_btn.clicked.connect(self.show_graph)
        self.graph_btn.setStyleSheet("background-color: #4CAF50; color: white; font-size: 12px; padding: 8px;")
        main_layout.addWidget(self.graph_btn)

        # Поле для статуса
        self.status_label = QLabel("Готов к работе")
        self.status_label.setStyleSheet("color: gray;")
        main_layout.addWidget(self.status_label)

        # Переменные для хранения данных
        self.current_need = 0
        self.norm_dict = {"Ячмень": 60, "Пшеница": 100, "Кукуруза": 10}
        self.dolya_N = 0.34  # доля N в 1 ц удобрения

    def on_culture_changed(self, culture):
        """Обновление нормы внесения при выборе культуры"""
        norm = self.norm_dict.get(culture, 60)
        self.norm_label.setText(str(norm))
        self.status_label.setText(f"Выбрана культура: {culture}, норма: {norm} кг/га")

    def calculate_need(self):
        """Расчет общей потребности"""
        try:
            area = float(self.area_input.text())
            culture = self.culture_combo.currentText()
            norm = self.norm_dict.get(culture, 60)

            # Потребность = Площадь * Норма / Доля N
            self.current_need = (area * norm) / self.dolya_N / 100  # /100 для перевода в центнеры

            self.need_result.setText(f"{self.current_need:.2f}")
            self.status_label.setText(f"Общая потребность рассчитана: {self.current_need:.2f} ц")

        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, введите корректные значения!")
            self.need_result.setText("")
            self.current_need = 0

    def calculate_main(self):
        """Расчет основного внесения (50%)"""
        if self.current_need == 0:
            QMessageBox.warning(self, "Ошибка", "Сначала рассчитайте общую потребность!")
            return
        main_need = self.current_need * 0.5
        self.main_result.setText(f"{main_need:.2f}")
        self.status_label.setText(f"Основное внесение: {main_need:.2f} ц")

    def calculate_pre_sowing(self):
        """Расчет припосевного внесения (25%)"""
        if self.current_need == 0:
            QMessageBox.warning(self, "Ошибка", "Сначала рассчитайте общую потребность!")
            return
        pre_sowing_need = self.current_need * 0.25
        self.pre_sowing_result.setText(f"{pre_sowing_need:.2f}")
        self.status_label.setText(f"Припосевное внесение: {pre_sowing_need:.2f} ц")

    def calculate_top_dressing(self):
        """Расчет подкормки (25%)"""
        if self.current_need == 0:
            QMessageBox.warning(self, "Ошибка", "Сначала рассчитайте общую потребность!")
            return
        top_dressing_need = self.current_need * 0.25
        self.top_dressing_result.setText(f"{top_dressing_need:.2f}")
        self.status_label.setText(f"Подкормка: {top_dressing_need:.2f} ц")

    def show_graph(self):
        """Построение графика сравнения с прошлыми годами"""
        if self.current_need == 0:
            QMessageBox.warning(self, "Ошибка", "Сначала рассчитайте потребность текущего года!")
            return

        # Данные по годам
        years = ["Позапрошлый год", "Прошлый год", "Текущий год"]
        values = [700, 250, self.current_need]
        colors_past = ["#ff9999", "#66b3ff", "#99ff99"]

        # Создание окна с графиком
        fig, ax = plt.subplots(figsize=(8, 6))
        bars = ax.bar(years, values, color=colors_past, edgecolor="black", linewidth=1.5)

        # Добавление значений на столбцы
        for bar, val in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 5,
                    f"{val:.2f} ц", ha="center", va="bottom", fontsize=10, fontweight="bold")

        ax.set_xlabel("Год", fontsize=12)
        ax.set_ylabel("Потребность в удобрениях, ц", fontsize=12)
        ax.set_title("Сравнение потребности в азотных удобрениях по годам", fontsize=14, fontweight="bold")
        ax.grid(axis="y", alpha=0.3)

        # Отображение графика
        plt.tight_layout()
        plt.show()

        self.status_label.setText("График построен")


# ============================================
# Запуск приложения
# ============================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyProject()
    window.show()
    sys.exit(app.exec_())