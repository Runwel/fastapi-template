import jwt

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjIyLCJyb2xlIjoiQURNSU4iLCJwZXJtaXNzaW9ucyI6WyJDUkVBVEUiLCJSRUFEIiwiVVBEQVRFIiwiREVMRVRFIl0sImV4cCI6MTc0MzE1MDkwMn0.M2GiIZCWofnH-0nytv2okIcf8mD8qH3qZsp4VawFHtI"
secret_key = "f6a8b8e3b26f0b2fa23c9434bcb9f7ac33f8b9c32c2bb04ed1233b46578d4587"

try:
    payload = jwt.decode(token, secret_key, algorithms=["HS256"])
    print("Token is valid ✅")
    print("Decoded Payload:", payload)
except jwt.ExpiredSignatureError:
    print("Token has expired ❌")
except jwt.InvalidSignatureError:
    print("Invalid signature ❌")
except jwt.PyJWTError as e:
    print("JWT Error:", e)
