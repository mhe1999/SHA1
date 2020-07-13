from classes import sha1
from hashlib import sha1 as py_sha1

implemented_Hash_Object = sha1('Test text')
implemented_hash = implemented_Hash_Object.compute_hash()
python_hash_object = py_sha1('Test text'.encode())
python_hash = python_hash_object.hexdigest()

print('hash calculated by my code:', implemented_hash)
print('hash calculated by hashlib:', python_hash)

if implemented_hash == python_hash:
    print('two hashes are identical')
else:
    print('two hashes are not identical')
