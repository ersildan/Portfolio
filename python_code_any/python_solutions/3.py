from collections import Counter
import re

regex = Counter(re.findall(r'(?:www\.)?(\w+\.(?:ru|com))\b', input()))
print(max(regex.items(), key=lambda x: x[1])[0])