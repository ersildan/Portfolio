from collections import Counter

print(['Bad', 'Good'][max(Counter(input().lower()).items(), key=lambda x: x[1])[1] > 1])