import math
import matplotlib.pyplot as plt

def B(i, n, j, p):
    """
    Tính xác suất j người truyền trong khe tiếp theo.

    Parameters:
    - i: trạng thái hiện tại (0 hoặc 1).
    - n: số người trong trạng thái i (n(0, k) hoặc n(1, k)).
    - j: số người muốn truyền trong khe tiếp theo.
    - p: xác suất mỗi người muốn truyền.

    Returns:
    - Xác suất B(i, n, j).
    """
    if j > n or j < 0:
        return 0  # Không thể có j lớn hơn tổng số người hoặc nhỏ hơn 0

    # Tổ hợp "j trong n"
    comb = math.comb(n, j)  # math.comb là tổ hợp trong Python

    # Xác suất
    probability = comb * (p ** j) * ((1 - p) ** (n - j))
    
    return probability

# Ví dụ sử dụng:
# Tính xác suất 2 người muốn truyền trong khi có 5 người ở trạng thái D = 1,
# với xác suất p = 0.3
result = B(1, 5, 2, 0.3)
print("Xác suất:", result)
def P(i, n, U, p):
    """
    Tính xác suất Pi = tổng từ m=0 đến m=i của B(0, n, m, p) * B(1, U-n, i-m, p).

    Parameters:
    - i: số người truyền trong khe tiếp theo.
    - n: số người trong trạng thái D = 0.
    - U: tổng số người.
    - p: xác suất mỗi người muốn truyền.

    Returns:
    - Xác suất Pi.
    """
    total_probability = 0
    for m in range(0, i + 1):
        b0 = B(0, n, m, p)  # Xác suất m người trong trạng thái D=0 muốn truyền
        b1 = B(1, U - n, i - m, p)  # Xác suất i-m người trong trạng thái D=1 muốn truyền
        total_probability += b0 * b1
    return total_probability

# Ví dụ sử dụng:
# Tính Pi với i = 3, n = 5, U = 10, p = 0.3
result = P(3, 5, 10, 0.3)
print("Xác suất Pi:", result)
def Pack(A, n, U, p):
    """
    Tính tổng Pack = tổng từ i=1 đến i=A của P(i, n, U, p).

    Parameters:
    - A: số người tối đa muốn truyền.
    - n: số người trong trạng thái D = 0.
    - U: tổng số người.
    - p: xác suất mỗi người muốn truyền.

    Returns:
    - Tổng xác suất Pack.
    """
    total_pack = 0
    for i in range(1, A + 1):
        total_pack += P(i, n, U, p)
    return total_pack

# Ví dụ sử dụng:
# Tính Pack với A = 5, n = 5, U = 10, p = 0.3
result = Pack(5, 5, 10, 0.3)
print("Tổng xác suất Pack:", result)

def P_transition(N, l, U, A, p):
    """
    Tính xác suất P(N, N+l).

    Parameters:
    - N: trạng thái mạng hiện tại.
    - l: thay đổi trạng thái mạng (N+l là trạng thái kế tiếp).
    - U: tổng số người.
    - A: giới hạn tối đa.
    - p: xác suất mỗi người muốn truyền.

    Returns:
    - Xác suất P(N, N+l).
    """
    if 0 < l <= min(U - N, A - 1):
        # Trường hợp 1
        term1 = B(1, N, l + 1, p)
        term2 = sum(B(0, N, m, p) for m in range(1, A - l))
        return term1 * term2

    elif N != 0 and l == -1:
        # Trường hợp 2
        term1 = B(1, N, 0, p)
        term2 = sum(B(0, N, m, p) for m in range(1, A + 1))
        return term1 * term2

    elif l == 0:
        # Trường hợp 3
        total = sum(P_transition(N, m, U, A, p) for m in range(1, N + 1))
        return 1 - total

    else:
        # Trường hợp 4
        return 0

# Ví dụ sử dụng:
# Tính P(N, N+l) với N = 3, l = 2, U = 10, A = 5, p = 0.3
result = P_transition(3, 2, 10, 5, 0.3)
print("Xác suất P(N, N+l):", result)

def pi_0(U, p):
    """
    Tính xác suất pi(0).

    Parameters:
    - U: tổng số người.
    - p: xác suất mỗi người muốn truyền.

    Returns:
    - Xác suất pi(0).
    """
    def inner_product(M):
        numerator = B(1, M, 2, p) * B(0, M, 0, p)
        denominator = B(1, M + 1, 0, p) * sum(B(0, M + 1, m, p) for m in range(1, 3))
        return numerator / denominator

    total_sum = sum(
        math.prod(inner_product(M) for M in range(N))
        for N in range(1, U + 1)
    )

    return 1 / (1 + total_sum)

# Ví dụ sử dụng:
# Tính pi(0) với U = 10, p = 0.3
result = pi_0(10, 0.3)
print("Xác suất pi(0):", result)

def pi_N(N, U, p):
    """
    Tính xác suất pi(N).

    Parameters:
    - N: trạng thái mạng hiện tại (số người trong trạng thái).
    - U: tổng số người.
    - p: xác suất mỗi người muốn truyền.

    Returns:
    - Xác suất pi(N).
    """
    def inner_product(M):
        numerator = B(1, M, 2, p) * B(0, M, 0, p)
        denominator = B(1, M + 1, 0, p) * sum(B(0, M + 1, m, p) for m in range(1, 3))
        return numerator / denominator

    product = math.prod(inner_product(M) for M in range(N))
    return pi_0(U, p) * product

# Ví dụ sử dụng:
# Tính pi(N) với N = 5, U = 10, p = 0.3
result = pi_N(0, 10, 0.3)
print("Xác suất pi(N):", result)

def T(U, p):
    """
    Tính tổng T = tổng từ N=0 đến N=U của pi_N(N, U, p) * Pack(2, N, U, p).

    Parameters:
    - U: tổng số người.
    - p: xác suất mỗi người muốn truyền.

    Returns:
    - Tổng T.
    """
    total_T = 0
    for N in range(U + 1):
        total_T += pi_N(N, U, p) * Pack(2, N, U, p)
    return total_T

# Ví dụ sử dụng:
# Tính T với U = 10, p = 0.3
result = T(10, 0.3)
print("Tổng T:", result)

def plot_T_vs_p(U, p_values):
    """
    Vẽ đồ thị T (trục tung) theo p (trục hoành).

    Parameters:
    - U: tổng số người.
    - p_values: danh sách các giá trị xác suất p.
    """
    T_values = [T(U, p) for p in p_values]

    plt.figure(figsize=(10, 6))
    plt.plot(p_values, T_values, marker='o', linestyle='-', color='b')
    plt.title("Đồ thị T theo p")
    plt.xlabel("p (Xác suất mỗi người muốn truyền)")
    plt.ylabel("T (Tổng xác suất)")
    plt.grid(True)
    plt.show()

# Ví dụ sử dụng:
# Vẽ đồ thị với U = 10 và p từ 0.1 đến 0.9
p_values = [i / 20 for i in range(1, 20)]
plot_T_vs_p(10, p_values)