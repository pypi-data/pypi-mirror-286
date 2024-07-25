from __future__ import annotations

import array

import numpy as np
import pandas as pd
from pandas import DataFrame

from k2health.k2_health_rev2 import health_train


class Pipeline:
    def __init__(self, cleaner: DataCleaner, partitioner: ConditionPartitioner, trainer: ModelTrainer):
        self.cleaner = cleaner
        self.partitioner = partitioner
        self.trainer = trainer

    def process(self, data: DataFrame):
        data = self.cleaner.process(data)
        data = self.partitioner.process(data)
        models = self.trainer.process(data)
        print("Trained models: ", models)


class DataCleaner:

    def __init__(self, point_config: DataFrame, y_col: array, x_col: array):
        self.point_config = point_config
        self.y_col = y_col
        self.x_col = x_col

    def process(self, data: DataFrame) -> DataFrame:
        data['timestamp'] = pd.to_datetime(data['timestamp'])
        data = data.set_index('timestamp').sort_index()
        data = data.astype(float)
        data = data.rename(columns=self.point_config.set_index('point_name')['name_en'].to_dict())
        data = data[self.y_col + self.x_col].interpolate()
        return data


class ConditionPartitioner:

    def __init__(self, device_config: DataFrame, device_tree: DataFrame):
        self.device_config = device_config
        self.device_tree = device_tree

    def process(self, data: DataFrame) -> DataFrame:
        data['k_cond'] = np.logical_and.reduce([data["motor_current"] > 1200,
                                                data["oil_temperature"] > 41,
                                                data["total_inlet_flow"] > 160000,
                                                data["total_power"] > 33000])
        data['k_cond'] = data['k_cond'].astype(bool)  # 多余?
        return data


class ModelTrainer:
    def __init__(self, y_col: array, model_config_sheet: DataFrame):
        self.y_col = y_col
        self.model_config_sheet = model_config_sheet

    def process(self, data: DataFrame):
        data = data['2022-2-1':'2022-5-1']

        model_config = self._sheet_to_model_config()
        models = health_train(data, self.y_col, None, model_config, False)
        return models

    def _sheet_to_model_config(self):
        result_dict = {}

        # 遍历DataFrame的每一行
        for index, row in self.model_config_sheet.iterrows():
            objective_var = row['objective_var']
            factor_var = row['factor_var']
            input_scale = row['input_scale']
            model_type = row['model_type']
            outlier_filter = row['outlier_filter']
            model_param = row.get('model_param', {})  # 如果model_param存在则获取，否则使用空字典
            if pd.isna(model_param) or model_param == '':
                model_param = {}

            # 在result_dict中创建或更新objective_var的条目
            if objective_var not in result_dict:
                result_dict[objective_var] = {
                    'X': [factor_var],
                    'input_scale': input_scale,
                    'model_type': model_type,
                    'outlier_filter': outlier_filter,
                    'model_param': model_param
                }
            else:
                # 如果objective_var已经存在，则追加factor_var到现有的'X'列表
                result_dict[objective_var]['X'].append(factor_var)

        return result_dict
