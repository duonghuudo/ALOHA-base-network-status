import numpy as np

def aloha_simulation(num_users, A, p, num_slots):
    # Khởi tạo các mảng trạng thái
    O = np.zeros(num_users)  # Trạng thái gửi thành công
    D = np.zeros(num_users)  # Trạng thái bộ đệm (1 = thành công, 0 = thất bại)
    Q = np.zeros(num_users)  # Ý định gửi trong slot

    successes = 0
    collisions = 0

    for slot in range(num_slots):
        # Cập nhật ý định gửi gói tin
        Q = (np.random.rand(num_users) < p).astype(int)  # Random theo xác suất p

        # Xác định các người gửi trong slot
        senders = np.where(Q == 1)[0]  # Danh sách index của người gửi
        num_senders = len(senders)

        if num_senders == 1:
            # Trường hợp chỉ 1 người gửi
            sender = senders[0]
            O[sender] = 1
            D[sender] = 1  # Thành công, xóa bộ đệm và tạo gói mới
            successes += 1
        elif 1 < num_senders <= A:
            # Trường hợp số người gửi ít hơn hoặc bằng A
            failed_senders = senders[D[senders] == 0]  # Chỉ những người thất bại trước đó
            #print(failed_senders)
            if len(failed_senders) > 0:
                chosen_sender = np.random.choice(failed_senders)
            else:
                chosen_sender = np.random.choice(senders)

            # Gửi ACK cho một người và NACK cho người còn lại
            for sender in senders:
                if sender == chosen_sender:
                    O[sender] = 1
                    D[sender] = 1  # Thành công
                else:
                    O[sender] = 0
                    D[sender] = 0  # Thất bại
            successes += 1
        elif num_senders > A:
            # Trường hợp số người gửi lớn hơn A
            for sender in senders:
                O[sender] = 0
                D[sender] = 0  # Tất cả thất bại
            collisions += 1

        # Cập nhật trạng thái D mới
        if num_senders <= A:  # Chỉ áp dụng logic này khi số người gửi không vượt quá A
            for i in range(num_users):
                if Q[i] == 0 or num_senders > A:
                    D[i] = D[i]  # Giữ nguyên trạng thái D cũ
                else:
                    D[i] = Q[i]  # Cập nhật theo ý định gửi


    # Tính hiệu suất thành công và tỷ lệ va chạm
    throughput = successes / num_slots
    collision_rate = collisions / num_slots

    return throughput, collision_rate, Q, senders

# Tham số đầu vào
# num_users = 10
# A = 3
# p = 0.2
# num_slots = 1000

# # Chạy mô phỏng
# efficiency, collision_rate, Q, senders = aloha_simulation(num_users, A, p, num_slots)
# print(Q)
# print(senders)
# # In kết quả
# print(f"Throughput (Hiệu suất thành công): {efficiency:.4f}")
# print(f"Collision rate (Tỷ lệ va chạm): {collision_rate:.4f}")
def collect_efficiency(num_users, A, num_slots, num_timers):
    efficiencies = []  # Mảng lưu kết quả hiệu suất
    p_values = np.linspace(0, 1, num_timers)  # Chia giá trị p từ 0 đến 1

    for p in p_values:
        throughput, collision_rate, Q, senders = aloha_simulation(num_users, A, p, num_slots)
        efficiencies.append(throughput)

    return p_values, efficiencies

# Tham số đầu vào
num_users = 10
A = 2
num_slots = 5000
num_timers = 20  # Chia giá trị p thành 20 bước

# Thu thập hiệu suất
p_values, efficiencies = collect_efficiency(num_users, A, num_slots, num_timers)

# In kết quả
print("p values:", p_values)
print("Efficiencies:", efficiencies)