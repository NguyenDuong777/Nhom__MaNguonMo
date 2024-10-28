import numpy as np
import matplotlib.pyplot as plotter

# Thông số ban đầu
samplingFrequency = 100  # Tần số lấy mẫu
samplingInterval = 1 / samplingFrequency  # Khoảng thời gian giữa các mẫu
beginTime = 0
endTime = 10  # Thời gian kết thúc
signal1Frequency = 4  # Tần số tín hiệu 1 (Hz)
signal2Frequency = 7  # Tần số tín hiệu 2 (Hz)

# Tạo các điểm thời gian
time = np.arange(beginTime, endTime, samplingInterval)

# Tạo hai sóng sin
amplitude1 = np.sin(2 * np.pi * signal1Frequency * time)
amplitude2 = np.sin(2 * np.pi * signal2Frequency * time)

# Tín hiệu tổng hợp (bao gồm cả hai tần số)
amplitude = amplitude1 + amplitude2

# Biến đổi Fourier tín hiệu
fourierTransform = np.fft.fft(amplitude)

# Tính các tần số tương ứng với các hệ số Fourier
frequencies = np.fft.fftfreq(len(amplitude), samplingInterval)

# Chọn bộ lọc
print("Chọn bộ lọc:")
print("1. Bộ lọc thông thấp")
print("2. Bộ lọc thông cao")
filter_choice = input("Nhập lựa chọn của bạn (1 hoặc 2): ")

cutoff_frequency = 5  # Ngưỡng tần số cắt, có thể thay đổi tùy ý

# Áp dụng bộ lọc dựa trên lựa chọn
filteredFourier = np.copy(fourierTransform)  # Bản sao của phổ Fourier gốc

if filter_choice == '1':
    # Bộ lọc thông thấp: Chỉ giữ lại các tần số dưới ngưỡng
    filteredFourier[np.abs(frequencies) > cutoff_frequency] = 0
elif filter_choice == '2':
    # Bộ lọc thông cao: Chỉ giữ lại các tần số trên ngưỡng
    filteredFourier[np.abs(frequencies) < cutoff_frequency] = 0
else:
    print("Lựa chọn không hợp lệ! Sử dụng tín hiệu gốc.")

# Biến đổi ngược Fourier để đưa tín hiệu đã lọc về miền thời gian
filteredAmplitude = np.fft.ifft(filteredFourier)

# Vẽ kết quả
figure, axis = plotter.subplots(3, 1)
plotter.subplots_adjust(hspace=1)

# Biểu diễn miền thời gian của tín hiệu tổng hợp
axis[0].set_title('Tín hiệu gốc (4Hz + 7Hz)')
axis[0].plot(time, amplitude)
axis[0].set_xlabel('Thời gian')
axis[0].set_ylabel('Biên độ')

# Biểu diễn miền tần số của tín hiệu gốc
axis[1].set_title('Phổ Fourier của tín hiệu gốc')
axis[1].plot(np.abs(frequencies), np.abs(fourierTransform))
axis[1].set_xlabel('Tần số (Hz)')
axis[1].set_ylabel('Biên độ')

# Biểu diễn tín hiệu đã lọc
axis[2].set_title('Tín hiệu đã lọc')
axis[2].plot(time, filteredAmplitude.real)  # Lấy phần thực của tín hiệu
axis[2].set_xlabel('Thời gian')
axis[2].set_ylabel('Biên độ')

plotter.show()
