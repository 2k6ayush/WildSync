import requests

url = 'http://localhost:5000/api/uploads'
files = {'file': ('test.txt', 'This is a text file', 'text/plain')}
try:
    r = requests.post(url, files=files)
    print(r.status_code)
    print(r.text)
except Exception as e:
    print(f"Error: {e}")
