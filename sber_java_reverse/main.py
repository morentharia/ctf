import jwt
# encoded_jwt = jwt.encode({"some": "payload"}, "MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCrr5qE7iJbaIBfUQhVpWkqTDZAhfvua72/YFCjs8maoiViwHpgLi6hhnPd30RedgnKyOTvCiiTGe2LfEk8O2t4yYVvSovx3K9wON/MXdXlP4MJ6q5oRpf+IKQc6FmD48TyJhJvsxZcgk2E4hL6tzh1NO3zSv4YWOFZ2S1m/4a3cGW3ozBLMpcmOd5tuCHfSb/nG5jmAfiNQ+BXpVhVIZnQJlpT2UIQcday/l/DmxVwla5NKX7elGP5cdejMjN1oSRnkVTFko53MgJ2FcR1QJRPLjt3jAop08dViV/0OMevMBZWDmnS8owxvHJyB3fWYUPvzHeD0+aN1UBSxJ9GjRNjAgMBAAECggEACTSfOmVyXihaScIUilMWMnhnqEoG2h/YyrwlVsG7G5l6G7NqXGHdijelWs4v4ki9+auP6ulGh6yqOgJuAtbEynMzvmXm3w8QMRo7lb+qSmJ/aja1J04xtCSX6BzlP9ckpj84WdjmaAtskKV2kw7j7hTqdVMeELwjSSgF8THeTVOY6qfJlO0YTNNiiTF6VuyXZg6nsd4DNbca4G1TsPV4HGNgBWXShlkueG/r5pzG/enEvHsYcHlqHH20vQAof0yPUIrHKWxwmoiP61I0M2K0rf5OELzuUk3Sqg3zBBw7H6F80PEWOPytf7pjs0eP9Yzx0PFQqw3N17PFpoP+AChy0QKBgQDmw8KWEHW5oguO6GQ4McY7MhCEf4TDIc2zjT9udyvDHnu6tboTfPB9KSTzZNtfPxfxCCN89R0qV+W7hxqTJ2h5J0d8CymNuH7K+RaTG4EcGEe03h/wRZstWUORZCmS1epMTC73iWuMCSAVm0hylW0Af2nA+R4M9dv+fidnYhD+3wKBgQC+dfBSM0Hyy3Pbf8pB8cfUXAPQBxM0RiOErv26M4yQLyd2CTmPT3vA3p6uMF2utlEbYCLvcGWyt4/O+z5rdHbW4bh06DCdKK/VJbY6/zNMc+DWzj1mJlwVHQLZ7FgdG/XECJGOZwoZC1Un0715JvQEpjaX6tcBQsP6H61ajxHv/QKBgQDO+rrnmm/dRqkTTwHFHW/t3GPQVAgidYlpCMHiNOV9pzPXLfRuUlvqByNrZAUXkyHIQUKDa97zAc++udluL6SXNlH5wpFM2jRvnadP3xWYu3Zlle4TtnsO28es+qgHWfNC5/ogcJOUEQNEHfmHPNt93MpgGZGIkmT2CPUS13TjBQKBgHY5rXDJApHc+tDw1TL0C2/lojQ6gBA9zYRqP3Oa1hEWRC9/8GvmEdKaHfPQcAaog1Yz6dupcGdsjGcWDBwVkkM2oBJpouubOvJbU2/xw/0cHSAZq4FCJHyyond1vwhqt7b0/q1fhqQfJb/wLrgKlwRfzJmmm8nbkN0tVqVVE/RdAoGAF6GX7zDmJmtPP8PuwOhUXi/9djv3kZB/8Q3dss5B11mNWAxMczwm/5y7s+pSDkDHuR3TadThVnecwXdUwIrg5MCuFjH4/rOeiWrnUjg6KbtN084WNqvkCgHj5uuIMLyda41F9Kh2psK++2BsNwiY943Gt1h61EdNTTUNAW49jeA=", algorithm="RS256")
# print(encoded_jwt)
# # eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzb21lIjoicGF5bG9hZCJ9.4twFt5NiznN84AWoo1d7KO1T_yoc0Z6XOpOVswacPZg
# jwt.decode(encoded_jwt, "secret", algorithms=["HS256"])

import base64
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_der_public_key


# pem_bytes = open('/tmp/sources/private.key', 'rb').read()
# print(pem_bytes)
# derdata = base64.b64decode(pem_bytes)
# print(derdata)
# key = load_der_public_key(derdata, default_backend())
# print(key)
#
# # print(pem_bytes)
# # private_key = serialization.load_pem_private_key(
# #     pem_bytes, password="", backend=default_backend()
# # )
# # print(pem_bytes)
#
#  # The public key as provided by appendix A.


pem_bytes = open('/tmp/sources/private.key', 'r').read()
private_key = pem_bytes
# Format as PEM key
public_key_formatted = f'-----BEGIN PRIVATE KEY-----\n' \
    f'{private_key}' \
    f'\n-----END PRIVATE KEY-----'

# Time function
payload = {}
payload['sub'] = 'CTFer'
# payload['email'] = 'ctf-crew@mail.ru'
payload['mail'] = 'mor.entharia@gmail.com'
# payload['aud'] = 'audience.nl'
# payload['iss'] = 'issuer.nl'
# payload['resource_id'] = 'dagstructuur'
# payload['first_name'] = 'Klaas'
# payload['middle_name'] = 'de'
# payload['last_name'] = 'Vries'
# payload['iat'] = time.time()
# payload['exp'] = time.time() + (5 * 60 * 1000)
# payload['jti'] = str(uuid4())

jwt_encode = jwt.encode(payload, public_key_formatted, algorithm='RS256')
print(jwt_encode)
