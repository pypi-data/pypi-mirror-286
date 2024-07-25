import numpy as np
from scipy.signal import find_peaks, butter, filtfilt
# 滤波器设计
def butter_lowpass_filter(data, cutoff, fs, order=4):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data)
    return y


# 卡尔曼滤波器
class KalmanFilter:
    def __init__(self, process_variance, measurement_variance, estimated_measurement_variance):
        self.process_variance = process_variance
        self.measurement_variance = measurement_variance
        self.estimated_measurement_variance = estimated_measurement_variance
        self.posteri_estimate = 0.0
        self.posteri_error_estimate = 1.0

    def filter(self, measurement):
        priori_estimate = self.posteri_estimate
        priori_error_estimate = self.posteri_error_estimate + self.process_variance

        blending_factor = priori_error_estimate / (priori_error_estimate + self.measurement_variance)
        self.posteri_estimate = priori_estimate + blending_factor * (measurement - priori_estimate)
        self.posteri_error_estimate = (1 - blending_factor) * priori_error_estimate

        return self.posteri_estimate

class BreathDetector:
    def __init__(self, fs=30):
        self.id=0
        self.fs=fs
        self.kf= KalmanFilter(process_variance=1e-5, measurement_variance=1e-2, estimated_measurement_variance=1e-1)
        
        self.cutoff = 0.5  # 低通滤波器的截止频率
        self.buffer_size = self.fs * 10  # 缓冲区大小，存储最近10秒的数据
        self.window_size = 10  # 滑动窗口大小，单位：帧数
        self.freq_buffer_size = 10  # 呼吸频率缓冲区大小

        self.avg_freq=0
        self.phase='U'

        self.left_shoulder_z = []
        self.right_shoulder_z = []
        self.freq_buffer = []
    def update(self, left, right):
        self.id += 1
        self.left_shoulder_z.append(left)
        self.right_shoulder_z.append(right)
        
        if len(self.left_shoulder_z) > self.buffer_size:
            self.left_shoulder_z.pop(0)
            self.right_shoulder_z.pop(0)


        if len(self.left_shoulder_z) < self.buffer_size:
            return 'U'

        smoothed_left_shoulder = butter_lowpass_filter(np.array(self.left_shoulder_z), self.cutoff, self.fs)
        smoothed_right_shoulder = butter_lowpass_filter(np.array(self.right_shoulder_z), self.cutoff, self.fs)

        # 合并两个肩膀的信号（可以取平均值，也可以分别计算）
        smoothed_data = (smoothed_left_shoulder + smoothed_right_shoulder) / 2

        # 去除直流分量
        smoothed_data = smoothed_data - np.mean(smoothed_data)

        filtered_data = np.array([self.kf.filter(x) for x in smoothed_data])

        # 设置动态间距
        dynamic_distance = 1.5*self.fs

        # 时域分析
        peaks, _ = find_peaks(filtered_data, distance=dynamic_distance)  # 找到波峰
        valleys, _ = find_peaks(-filtered_data, distance=dynamic_distance)  # 找到波谷

        self.phase='U'
        if len(peaks) >0 and len(valleys) > 0:
            # 标记每一帧是吸气还是呼气
            breath_phase = np.zeros(len(smoothed_data), dtype=str)

            breath_phase[peaks] = 'I' #Inhale
            breath_phase[valleys] = 'E' #Exhale

            current_phase = 'E' if valleys[0] < peaks[0] else 'I'
            for i in range(len(smoothed_data)):
                if breath_phase[i] != '':
                    current_phase = breath_phase[i]
                breath_phase[i] = current_phase

            self.phase = str(breath_phase[-10])

            if self.id % self.fs == 0:
                last = ''
                count = 0
                for i in range(len(breath_phase)):
                    if breath_phase[i] != last:
                        count += 1
                        last = breath_phase[i]

                # 计算当前呼吸频率
                current_freq = 60 / ((len(breath_phase) / self.fs) / (count / 2))

                # 将当前呼吸频率添加到缓冲区
                self.freq_buffer.append(current_freq)
                if len(self.freq_buffer) > self.freq_buffer_size:
                    self.freq_buffer.pop(0)

                # 计算缓冲区内的平均呼吸频率
                self.avg_freq = round(np.mean(self.freq_buffer))
        else:
            self.avg_freq= -1

        return self.phase