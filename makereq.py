import json

import requests
from tkinter import filedialog

# URL to send the POST request to
url = "http://localhost:3000/check"


file = open(filedialog.askopenfilename(), 'rb')

data = {
    "file": file
}

# Send POST request
response = requests.post(url, files=data)

# Print response text (the content of the response)
print(json.dumps(response.json(), indent=4))
