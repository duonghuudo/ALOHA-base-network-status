import numpy as np
import matplotlib.pyplot as plt

def aloha_simulation(num_users, A, pf, pr, num_slots):
    O = np.zeros(num_users)  # Trạng thái gửi thành công
    D = np.ones(num_users)  # Bộ đệm người dùng (1 = tự do, 0 = backlog)

    successes = 0
    collisions = 0

    for slot in range(num_slots):
        # Xác suất gửi dựa trên trạng thái D
        p = np.where(D == 1, pf, pr)

        # Ý định gửi gói tin
        Q = (np.random.rand(num_users) < p).astype(int)
        senders = np.where(Q == 1)[0]
        num_senders = len(senders)

        if num_senders == 1:
            # Thành công nếu chỉ có 1 người gửi
            sender = senders[0]
            O[sender] = 1
            D[sender] = 1  # Thành công, tạo gói tin mới
            successes += 1
        elif 1 < num_senders <= A:
            # Sử dụng SIC nếu số người gửi <= A
            for sender in senders:
                O[sender] = 1
                D[sender] = 1  # Thành công
            successes += min(num_senders, A)
        else:
            # Thất bại nếu số người gửi > A
            for sender in senders:
                O[sender] = 0
                D[sender] = 0  # Tất cả thất bại
            collisions += 1

    throughput = successes / num_slots
    collision_rate = collisions / num_slots
    return throughput, collision_rate

# Thu thập hiệu suất
def collect_efficiency(num_users, A, pf, num_slots, num_timers):
    efficiencies = []
    pr_values = np.linspace(0.01, 1.0, num_timers)

    for pr in pr_values:
        throughput, _ = aloha_simulation(num_users, A, pf, pr, num_slots)
        efficiencies.append(throughput)

    return pr_values, efficiencies

# Tham số mô phỏng
num_users = 10
A = 3
pf = 0.1  # Xác suất gửi của người dùng tự do
num_slots = 5000
num_timers = 50

# Thu thập hiệu suất với các giá trị pr
pr_values, efficiencies = collect_efficiency(num_users, A, pf, num_slots, num_timers)

# Vẽ đồ thị
plt.figure(figsize=(8, 5))
plt.plot(pr_values, efficiencies, '-o', label='Throughput', color='blue')
plt.xlabel('Retransmission Probability (pr)')
plt.ylabel('Throughput')
plt.title('Throughput vs Retransmission Probability (pr)')
plt.grid(True)
plt.legend()
plt.show()
