import random
from collections import defaultdict

def generate_random_numbers(count, range_start, range_end):
    """生成指定数量的随机数"""
    return [random.randint(range_start, range_end) for _ in range(count)]

def find_matching_sums(numbers):
    """找到相同加法结果的组合数量"""
    sum_counts = defaultdict(int)
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            result = numbers[i]+ numbers[j]
            sum_counts[result] += 1
    return sum_counts

def main():
    # 生成 100 个范围在 1 到 100 之间的随机数
    random_numbers = generate_random_numbers(100, 1, 100)
    
    # 查找相同加法结果的组合数量
    matching_sums = find_matching_sums(random_numbers)
    
    # 输出结果
    for sum_value, count in matching_sums.items():
        print(f"Sum: {sum_value}, Combinations: {count}")

if __name__ == "__main__":
    main()
