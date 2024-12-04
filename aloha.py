import numpy as np

# Thông số mô phỏng
num_users = 4  # Số lượng users
time_slots = 1000  # Số khe thời gian
transmission_prob = 0.05  # Xác suất gửi của mỗi user trong mỗi khe thời gian

# Thu thập dữ liệu
successful_transmissions = 0
collisions = 0

# # Mô phỏng Frameless Slotted ALOHA base network status
# for t in range(time_slots):
#     # Các node quyết định gửi hay không (1: gửi, 0: không gửi)
#     transmissions = np.random.rand(num_users) < transmission_prob
#     num_transmissions = np.sum(transmissions)

#     if num_transmissions == 1:
#         # Một gói thành công
#         successful_transmissions += 1
#     elif num_transmissions > 1:
#         # Có xung đột
#         collisions += 1


# Hiệu suất
throughput = successful_transmissions / time_slots
collision_rate = collisions / time_slots

print(f"Hiệu suất (Throughput): {throughput:.2f}")
print(f"Tỷ lệ xung đột (Collision Rate): {collision_rate:.2f}")
