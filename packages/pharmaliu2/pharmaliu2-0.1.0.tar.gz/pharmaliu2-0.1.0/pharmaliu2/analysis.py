import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

class PharmacokineticsAnalysis:
    
    def __init__(self, file_path):
        self.file_path = file_path
        self.V1, self.V2 = self.read_data()
    
    # 定义模型函数
    @staticmethod
    def one_compartment_model(V1, a, b, c, d, u, v, x, y, ka):
        return np.exp(-a * V1) * (v * np.sin(2 * np.pi * b * V1))  # 一室非血管

    @staticmethod
    def two_compartment_model(V1, a, b, c, d, u, v, x, y, ka):
        return 2 * np.exp(-a * V1) * (u * np.cos(b * V1) + v * np.sin(b * V1))  # 二室血管

    @staticmethod
    def four_compartment_model(V1, a, b, c, d, u, v, x, y, ka):
        return 2 * (
            np.exp(-a * V1) * (u * np.cos(2 * np.pi * b * V1) - v * np.sin(2 * np.pi * b * V1)) +
            np.exp(-c * V1) * (x * np.cos(2 * np.pi * d * V1) - y * np.sin(2 * np.pi * d * V1)) -
            (u + x) * np.exp(-ka * V1)
        )  # 四室非血管+消化道循环

    # 从CSV文件中读取数据
    def read_data(self):
        data = pd.read_csv(self.file_path, sep=',')
        V1 = data['V1'].values
        V2 = data['V2'].values
        return V1, V2

    # 使用curve_fit进行非线性回归
    def fit_model(self, model, initial_guess):
        try:
            params, params_covariance = curve_fit(model, self.V1, self.V2, p0=initial_guess, maxfev=10000)
            return params
        except RuntimeError as e:
            print(f"优化失败: {str(e)}")
            return None

    # 计算R方
    @staticmethod
    def calculate_r_squared(V1, V2, model, params):
        residuals = V2 - model(V1, *params)
        ss_res = np.sum(residuals**2)  # 残差平方和
        ss_tot = np.sum((V2 - np.mean(V2))**2)  # 总平方和
        r_squared = 1 - (ss_res / ss_tot)  # R平方值
        return r_squared

    # 计算药物动力学参数
    @staticmethod
    def calculate_pharmacokinetics_params(a, b, c, d, u, v, x, y, ka, X0, AUC, Vc):
        k = X0 / (AUC * Vc)
        ka1 = (a**2 + b**2) / k
        k1a = 2 * a - k - ka1
        return k, ka1, k1a

    def analyze(self, initial_guess, X0, AUC, Vc):
        # 拟合模型并计算R平方值
        models = {
            "one_compartment": self.one_compartment_model,
            "two_compartment": self.two_compartment_model,
            "four_compartment": self.four_compartment_model
        }

        best_model = None
        best_r_squared = -np.inf
        best_params = None

        for name, model_func in models.items():
            params = self.fit_model(model_func, initial_guess)
            if params is not None:
                r_squared = self.calculate_r_squared(self.V1, self.V2, model_func, params)
                print(f"{name} R平方值: {r_squared:.4f}")
                if r_squared > best_r_squared:
                    best_r_squared = r_squared
                    best_model = name
                    best_params = params

        if best_params is None:
            print("所有模型的优化均失败")
            return

        # 打印最优模型优化后的参数
        param_names = ['a', 'b', 'c', 'd', 'u', 'v', 'x', 'y', 'ka']
        print(f"最佳模型: {best_model}")
        for name, value in zip(param_names, best_params):
            print(f"{name}: {value:.4f}")

        # 优化后的药物动力学参数
        a, b, c, d, u, v, x, y, ka = best_params

        # 根据最佳模型选择相应的公式计算药物动力学参数
        k, ka1, k1a = self.calculate_pharmacokinetics_params(a, b, c, d, u, v, x, y, ka, X0, AUC, Vc)

        formula_used = {
            "one_compartment": "一室模型非血管给药公式",
            "two_compartment": "二室模型血管给药公式",
            "four_compartment": "四室模型非血管给药+消化道循环公式"
        }[best_model]

        print(f"使用的模型: {best_model}")
        print(f"使用的公式: {formula_used}")
        print(f"k: {k:.4f}")
        print(f"ka1: {ka1:.4f}")
        print(f"k1a: {k1a:.4f}")

        return {
            "model": best_model,
            "formula": formula_used,
            "params": best_params,
            "k": k,
            "ka1": ka1,
            "k1a": k1a
        }