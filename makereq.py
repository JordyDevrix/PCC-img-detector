import json
import time

import requests
from tkinter import filedialog

file = open(filedialog.askopenfilename(), 'rb')
idx = 0
while idx < 20:
    url = "https://pcc.jordydevrix.com/check"
    data = {
        "file": file
    }

    # Send POST request
    response = requests.post(url, files=data)

    # Print response text (the content of the response)
    # print(json.dumps(response.json(), indent=4))
    if response.status_code == 200:
        print(response.json())
    else:
        print(response.status_code)

    time.sleep(5)
    idx += 1
