import sys
import traceback
import numpy as np
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox

# 导入计算函数
from Staticpressureofliquidcolumn import cfcpif
from Wellborefriction import ctfi
from Orificefriction import cpf
from NetpressureBottom import calculate_bottomhole_pressure
from Plot import pressure_curve, plot_combined_curves
from Dataprocessing import analyze_and_plot_extension_modes

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.file_label = QLabel("文件路径:")
        self.file_input = QLineEdit()
        self.file_button = QPushButton("浏览文件目录")
        self.file_button.clicked.connect(self.browse_file)

        layout.addWidget(self.file_label)
        layout.addWidget(self.file_input)
        layout.addWidget(self.file_button)

        self.well_depth_label = QLabel("井深(m):")
        self.well_depth_input = QLineEdit()

        self.well_length_label = QLabel("井筒深度(m):")
        self.well_length_input = QLineEdit()

        self.density_sand_label = QLabel("支撑剂密度(kg/m³):")
        self.density_sand_input = QLineEdit()

        self.density_fluid_label = QLabel("压裂液密度(kg/m³):")
        self.density_fluid_input = QLineEdit()

        self.well_diameter_label = QLabel("井筒直径(m):")
        self.well_diameter_input = QLineEdit()

        self.min_horizontal_stress_label = QLabel("最小水平主应力(Pa):")
        self.min_horizontal_stress_input = QLineEdit()

        self.pdiameter_label = QLabel("孔眼直径(m):")
        self.pdiameter_input = QLineEdit()

        self.perforation_flow_coefficient_label = QLabel("孔眼流量系数:")
        self.perforation_flow_coefficient_input = QLineEdit()

        self.wellbore_roughness_label = QLabel("井筒绝对粗糙度(m):")
        self.wellbore_roughness_input = QLineEdit()

        self.perforation_quantity_label = QLabel("孔眼数量:")
        self.perforation_quantity_input = QLineEdit()

        self.dropoutrate_label = QLabel("降阻率:")
        self.dropoutrate_input = QLineEdit()

        self.calculate_button = QPushButton("运行")
        self.calculate_button.clicked.connect(self.calculate)

        layout.addWidget(self.well_depth_label)
        layout.addWidget(self.well_depth_input)
        layout.addWidget(self.well_length_label)
        layout.addWidget(self.well_length_input)
        layout.addWidget(self.density_sand_label)
        layout.addWidget(self.density_sand_input)
        layout.addWidget(self.density_fluid_label)
        layout.addWidget(self.density_fluid_input)
        layout.addWidget(self.well_diameter_label)
        layout.addWidget(self.well_diameter_input)
        layout.addWidget(self.min_horizontal_stress_label)
        layout.addWidget(self.min_horizontal_stress_input)
        layout.addWidget(self.pdiameter_label)
        layout.addWidget(self.pdiameter_input)
        layout.addWidget(self.perforation_flow_coefficient_label)
        layout.addWidget(self.perforation_flow_coefficient_input)
        layout.addWidget(self.wellbore_roughness_label)
        layout.addWidget(self.wellbore_roughness_input)
        layout.addWidget(self.perforation_quantity_label)
        layout.addWidget(self.perforation_quantity_input)
        layout.addWidget(self.dropoutrate_label)
        layout.addWidget(self.dropoutrate_input)
        layout.addWidget(self.calculate_button)

        self.setLayout(layout)

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Excel File", "", "Excel Files (*.xlsx *.xls)")
        if file_path:
            self.file_input.setText(file_path)

    def calculate(self):
        try:
            excel_path = self.file_input.text()
            well_depth_Z = float(self.well_depth_input.text())
            well_length_L = float(self.well_length_input.text())
            density_sand = float(self.density_sand_input.text())
            density_fluid = float(self.density_fluid_input.text())
            well_diameter = float(self.well_diameter_input.text())
            min_horizontal_stress = float(self.min_horizontal_stress_input.text())
            pdiameter = float(self.pdiameter_input.text())
            perforation_flow_coefficient = float(self.perforation_flow_coefficient_input.text())
            wellbore_roughness = float(self.wellbore_roughness_input.text())
            perforation_quantity = int(self.perforation_quantity_input.text())
            dropoutrate = float(self.dropoutrate_input.text())

            # 调用计算函数
            self.calculate_bottomhole_pressure_from_excel(excel_path, well_depth_Z, well_length_L, density_sand, density_fluid, well_diameter, min_horizontal_stress, pdiameter, perforation_flow_coefficient, wellbore_roughness, perforation_quantity, dropoutrate)

            QMessageBox.information(self, "Calculation Complete", "Bottomhole pressure calculation is complete!")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")
            traceback.print_exc()

    def calculate_bottomhole_pressure_from_excel(self, excel_path, well_depth_Z, well_length_L, density_sand, density_fluid, well_diameter, min_horizontal_stress, pdiameter, perforation_flow_coefficient, wellbore_roughness, perforation_quantity, dropoutrate):
        data = pd.read_excel(excel_path, header=0)
        displacement = data['排量'].values  # Excel文件中的排量列
        displacement_per_second = displacement / 60  # 立方米每分钟化为立方米每秒
        sand_ratio = data['砂比'].values  # Excel文件中的砂浓度列
        sand_concentration = sand_ratio / 100  # 百分比化为小数
        viscosity = data['液体粘度']
        fluid_viscosity = viscosity / 1000
        wellhead_pressure_MPa = data['施工泵压'].values  # Excel文件中的排量列
        wellhead_pressure = wellhead_pressure_MPa * 1000000
        time_in_seconds = data['时间s']

        # 井筒内携沙液柱静压力
        fluid_integral = cfcpif(displacement_per_second, sand_concentration, density_sand, density_fluid, 9.8, well_depth_Z, well_diameter)
        # 井筒流动摩阻
        tubing_friction_integral = ctfi(displacement_per_second, sand_concentration, density_sand, density_fluid, well_length_L, well_diameter, wellbore_roughness, fluid_viscosity, 1 - dropoutrate)
        # 计算孔眼摩阻
        perforation_friction = cpf(displacement_per_second, density_fluid, density_sand, sand_concentration, perforation_quantity, pdiameter, perforation_flow_coefficient)
        # 计算井底净压力
        bottomholepressure = calculate_bottomhole_pressure(wellhead_pressure, fluid_integral, tubing_friction_integral, perforation_friction, min_horizontal_stress)
        self.trim_zeros(bottomholepressure, time_in_seconds, fluid_integral, tubing_friction_integral, perforation_friction)

        # 定义要绘制的数据集和标签
        tfi = [val / 1000000 for val in tubing_friction_integral]
        fi = [val / 1000000 for val in fluid_integral]
        pf = [val / 1000000 for val in perforation_friction]
        wp = [val / 1000000 for val in wellhead_pressure]
        wp1 = [val - 20 for val in wp]
        bp = [val / 1000000 for val in bottomholepressure]
        tis = [val / 60 for val in time_in_seconds]

        dataset_tuple4 = (bp, displacement, sand_ratio, viscosity)
        label_tuple4 = ('井底净压力(MPa)', '排量 (m3/min) ', '砂比（%', '粘度 (mPa·s)')

        # 绘制多坐标曲线
        plot_combined_curves(tis, dataset_tuple4, label_tuple4, '149-1HF-24段压裂', tis, bottomholepressure)
        # 绘制井底压力曲线
        pressure_curve(time_in_seconds, bottomholepressure)
        analyze_and_plot_extension_modes(time_in_seconds, bottomholepressure)

        return time_in_seconds, bottomholepressure, fluid_integral, tubing_friction_integral, perforation_friction

    def trim_zeros(self, bottomholepressure, time_in_seconds, fluid_integral, tubing_friction_integral, perforation_friction):
        # 从数组末尾开始向前遍历，找到第一个非零值的索引
        for i in range(len(bottomholepressure) - 1, -1, -1):
            if bottomholepressure[i] != 0:
                # 剔除所有末尾的零值
                bottomholepressure = bottomholepressure
                bottomholepressure = bottomholepressure[:i + 1]
                time_in_seconds = time_in_seconds[:i + 1]
                fluid_integral = fluid_integral[:i + 1]
                tubing_friction_integral = tubing_friction_integral[:i + 1]
                perforation_friction = perforation_friction[:i + 1]
                break

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.setWindowTitle("井底压力折算")
    main_window.resize(400, 600)
    main_window.show()
    sys.exit(app.exec_())
