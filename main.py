import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QGridLayout,
    QPushButton,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QInputDialog,
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect

class Lift:
    def __init__(self, capacity):
        self.current_floor = 0
        self.capacity = capacity
        self.current_weight = 0

class LiftManagementApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.lifts = []
        self.average_weight = 68  # Default average weight per person in kg
        self.total_floors = 10  # Default total floors
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Lift Management Simulation")
        self.setGeometry(100, 100, 800, 600)

        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        self.layout = QVBoxLayout(self.main_widget)

        self.upper_layout = QGridLayout()
        self.lower_layout = QVBoxLayout()

        self.setup_lifts()
        self.setup_floor_buttons()

        self.layout.addLayout(self.upper_layout)
        self.layout.addLayout(self.lower_layout)

        self.setup_inside_lift_controls()

        self.show()

    def setup_lifts(self):
        lift_section = QVBoxLayout()
        lift_count, ok = QInputDialog.getInt(self, "Input", "Enter number of lifts:", 1, 1)
        if ok:
            lift_capacity, ok = QInputDialog.getInt(self, "Input", "Enter lift capacity (kg):", 1000, 1)
            if ok:
                average_weight, ok = QInputDialog.getInt(self, "Input", "Enter average weight per passenger (kg):", self.average_weight, 1)
                if ok:
                    self.average_weight = average_weight
                    self.total_floors, ok = QInputDialog.getInt(self, "Input", "Enter total number of floors:", self.total_floors, 1)
                    if ok:
                        for i in range(lift_count):
                            lift = Lift(lift_capacity)
                            self.lifts.append(lift)
                            lift_label = QLabel(f"Lift {i + 1}: Floor {lift.current_floor} | Weight {lift.current_weight}/{lift.capacity} kg")
                            lift_label.setObjectName(f"lift_label_{i}")
                            lift_section.addWidget(lift_label)

                        self.upper_layout.addLayout(lift_section, 0, 0)

    def setup_floor_buttons(self):
        floor_buttons_layout = QVBoxLayout()
        for floor in range(self.total_floors):
            floor_label = QLabel(f"Floor {self.total_floors - 1 - floor}")
            floor_buttons_layout.addWidget(floor_label)

            if floor == 0:
                button = QPushButton("Up")
                button.clicked.connect(lambda _, f=floor: self.request_passengers_and_call_lift(f))
                floor_buttons_layout.addWidget(button)
            elif floor == self.total_floors - 1:
                button = QPushButton("Down")
                button.clicked.connect(lambda _, f=floor: self.request_passengers_and_call_lift(f))
                floor_buttons_layout.addWidget(button)
            else:
                button_up = QPushButton("Up")
                button_down = QPushButton("Down")
                button_up.clicked.connect(lambda _, f=floor: self.request_passengers_and_call_lift(f))
                button_down.clicked.connect(lambda _, f=floor: self.request_passengers_and_call_lift(f))
                floor_buttons_layout.addWidget(button_up)
                floor_buttons_layout.addWidget(button_down)

        self.upper_layout.addLayout(floor_buttons_layout, 0, 1)

    def setup_inside_lift_controls(self):
        self.inside_lift_layout = QVBoxLayout()

        for i, lift in enumerate(self.lifts):
            inside_layout = QVBoxLayout()
            passenger_exit_label = QLabel(f"Lift {i + 1} - Number of passengers exiting:")
            passenger_exit_input = QLineEdit(self)
            passenger_exit_input.setPlaceholderText("Enter number of passengers exiting")
            inside_layout.addWidget(passenger_exit_label)
            inside_layout.addWidget(passenger_exit_input)

            target_label = QLabel(f"Lift {i + 1} - Enter target floor:")
            target_floor_input = QLineEdit(self)
            target_floor_input.setPlaceholderText("Enter target floor")
            inside_layout.addWidget(target_label)
            inside_layout.addWidget(target_floor_input)

            go_button = QPushButton("Go")
            go_button.clicked.connect(lambda _, lift_idx=i, exit_input=passenger_exit_input, t_input=target_floor_input: self.move_lift(lift_idx, exit_input.text(), t_input.text()))
            inside_layout.addWidget(go_button)

            self.inside_lift_layout.addLayout(inside_layout)

        self.lower_layout.addLayout(self.inside_lift_layout)

    def request_passengers_and_call_lift(self, target_floor):
        num_passengers, ok = QInputDialog.getInt(self, "Input", "Enter number of passengers:", 1, 1)
        if ok:
            total_weight = num_passengers * self.average_weight
            print(f"Requested weight: {total_weight} kg to floor {target_floor}")
            self.call_lifts_for_weight(target_floor, total_weight)

    def call_lifts_for_weight(self, target_floor, total_weight):
        actual_target_floor = self.total_floors - 1 - target_floor
        lifts_to_send = []
        remaining_passengers = total_weight // self.average_weight

        for lift in sorted(self.lifts, key=lambda l: abs(l.current_floor - actual_target_floor)):
            if remaining_passengers <= 0:
                break
            available_capacity_passengers = (lift.capacity - lift.current_weight) // self.average_weight
            if available_capacity_passengers > 0:
                assigned_passengers = min(available_capacity_passengers, remaining_passengers)
                lift_load = assigned_passengers * self.average_weight
                lifts_to_send.append((lift, lift_load))
                remaining_passengers -= assigned_passengers
                print(f"Assigning {assigned_passengers} passengers ({lift_load} kg) to Lift {self.lifts.index(lift) + 1}")

        if remaining_passengers > 0:
            QMessageBox.warning(self, "Over Capacity", "No lifts available to accommodate all passengers, even with split load!")
        else:
            for lift, weight in lifts_to_send:
                print(f"Moving Lift {self.lifts.index(lift) + 1} to floor {actual_target_floor} with weight {weight} kg")
                self.animate_lift(lift, actual_target_floor, weight)

    def animate_lift(self, lift, target_floor, weight):
        lift_label = self.findChild(QLabel, f"lift_label_{self.lifts.index(lift)}")
        animation = QPropertyAnimation(lift_label, b"geometry")
        start_rect = QRect(0, (self.total_floors - 1 - lift.current_floor) * 50, 200, 50)
        end_rect = QRect(0, (self.total_floors - 1 - target_floor) * 50, 200, 50)
        animation.setDuration(1000)
        animation.setStartValue(start_rect)
        animation.setEndValue(end_rect)
        animation.start()

        lift.current_floor = target_floor
        lift.current_weight += weight
        lift_label.setText(f"Lift {self.lifts.index(lift) + 1}: Floor {lift.current_floor} | Weight {lift.current_weight}/{lift.capacity} kg")

    def move_lift(self, lift_idx, num_exiting, target_floor):
        lift = self.lifts[lift_idx]
        try:
            num_exiting = int(num_exiting)
            target_floor = int(target_floor)
            weight_to_remove = num_exiting * self.average_weight

            if lift.current_weight - weight_to_remove >= 0:
                lift.current_weight -= weight_to_remove
                self.animate_lift(lift, target_floor, 0)
            else:
                QMessageBox.warning(self, "Weight Error", "Cannot remove more weight than is currently in the lift.")
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid numbers for passengers exiting and target floor.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LiftManagementApp()
    sys.exit(app.exec_())
