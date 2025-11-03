import re

pattern = r'[\\/]([^\\/.]+)\.'
matches = re.findall(pattern, input())

print(*matches)
