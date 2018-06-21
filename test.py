
import json

a = b'{"code":"err","resInfo":"\xe9\xaa\x8c\xe8\xaf\x81\xe7\xa0\x81\xe4\xb8\x8d\xe6\xad\xa3\xe7\xa1\xae"}'

b = a.decode('utf-8')


result_json = json.loads(b)

print(result_json)