import re

regex = re.findall(r'https?://www.(\w*[.ru|.com]*)', input())
print(*regex, sep='\n')
