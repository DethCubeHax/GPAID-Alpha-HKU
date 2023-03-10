# Scraper for RICHKU-Parasite
The scraper is a python script that uses a unique methodological approach to scrape the data from the RICHKU-Parasite website. The scraper is written in python and uses the following libraries:

* [json](https://docs.python.org/3/library/json.html)
* [requests](https://requests.readthedocs.io/en/master/)
* [random](https://docs.python.org/3/library/random.html)
* [os](https://docs.python.org/3/library/os.html)
* [time](https://docs.python.org/3/library/time.html)

The website uses a midddleware that obtains its data from an API under the domain `https://api.richku.com`. The API is protected by a token that is generated by the website and is stored in the browser's local storage. The scraper uses a methodological approach to obtain the token and then scrape the data from the API.

## Methodology
If the api were to be directly accessed from a browser window, it would return a `403 Forbidden` error. This is because the API is protected by a token that is generated by the website and is stored in the browser's local storage. In order to obtain the data, we need to trick the API into thinking that we are a browser window. This is done by using the `requests` library to send a request to the API. The request is sent with a payload consisting of the username and password, which are first used in conjunction with the additional headers to obtain the token. The token is then used to obtain the data from the API. The token is obtained by sending a POST request to the `/v1/auth` endpoint with the following headers and payload:
    
```python
def generatePayload(type, CURRENT, PAGESIZE):
    if (type == "login"):
        payload = {
            "email": USERNAME, 
            "password": PASSWORD, 
        }
        return payload
    elif (type == "course"):
        payload = {
            "search": "",
            "current": CURRENT,
            "page_size": PAGESIZE,
            "order": "asc",
            "sort": "course_code"
        }
        return payload
    return None
```
```python
def generateHeaders(METHOD, PATH, token):
    TOKENSTR=f"Bearer {token}"
    headers={
        'authority':'api.richku.com',
        'method':METHOD,
        'path':PATH,
        'scheme':'https',
        "accept":"application/json, text/plain, */*",
        "accept-language":"en-GB,en;q=0.9",
        "authorization":TOKENSTR,
        "origin":"https://richku.com",
        "referer":"https://richku.com/",
        "sec-ch-ua":"Not?A_Brand';v='8', 'Chromium';v='108', 'Microsoft Edge';v='108",
        "sec-ch-ua-mobile":"?0",
        "sec-ch-ua-platform":"Linux",
        "sec-fetch-dest":"empty",
        "sec-fetch-mode":"cors",
        "sec-fetch-site":"same-site",
        "user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54"
    }

    if (PATH == "/v1/auth"):
        headers["content-type"] = "application/json"

    return headers
```

Notice that the `headers["content-type"]` is set to `application/json` only when the path is `/v1/auth`. This is because the API expects the payload to be in JSON format only when the path is `/v1/auth`. The token is then used to obtain the data from the API. 

The token is then used to obtain the data from the API. The data is obtained by sending a GET request to the `/v1/courses` endpoint with the same payload, except that the `headers["content-type"]` is not specified, and the `headers["authorization"]` is set to the token. The data is then stored in an array temporarily, and the `current` and `page_size` values are incremented by 10. This is done until the `current` value is greater than the `total` value. The data is then stored in a JSON file.

```python
def updateCourseList(CURR, SIZE, headers, existingCourses):
    while(CURR*10 < SIZE+10):
        PATH="/v1/courses?search=&current="+str(CURR)+"&page_size=10&order=asc&sort=code"
        resp = session_requests.get(URL+PATH, headers=headers)
        if (resp.status_code != 200):
            print("Unable to get course list for batch: " + str(CURR))
            return 1
        processedData = json.loads(resp.text)['data']['list']
        for item in processedData:
            tmpDict = {}
            for key in item:
                if key in includes:
                    tmpDict[key] = item[key]
            with open(f"{DIR}courseList.txt", "a") as f:
                if tmpDict not in existingCourses:
                    f.write(json.dumps(tmpDict)+",\n")
                    print("Course added: " + str(tmpDict["code"]))
                else:
                    print("Course already exists: " + str(tmpDict["code"]))

        CURR+=1
        sleep(random.randint(5,10))
    return 0
```
Note that the program also checks if the course already exists in the `courseList.txt` file. This is done to prevent the program from adding the same course multiple times. The program also sleeps for a random amount of time between 5 and 10 seconds after each request to prevent the API from blocking the request.

A similar procedure is followed to obtain the user reviews. The user reviews are obtained by sending a GET request to the `/v1/courses/{course_id}/reviews` endpoint with the same payload, except that the `headers["content-type"]` is not specified, and the `headers["authorization"]` is set to the token. The data is then stored in an array temporarily, and the `current` and `page_size` values are incremented by 10. This is done until the `current` value is greater than the `total` value. The data is again stored temporarily in an array.

```python
def updateReviews(CURR, SIZE, headers, COURSEID):
    commentList = []
    exists = False
    tmpLst = []
    if os.path.isfile(f"{DIR}/reviews/{COURSEID}.txt"):
        exists = True
        with open(f"{DIR}/reviews/{COURSEID}.txt", "r") as f:
            data = f.read()
            data = data.split(",\n")
            data = data[:-1]
            for item in data:
                commentList.append(json.loads(item))
    PATH=f"/v1/courses/{COURSEID}/reviews?current="+str(CURR)+"&page_size=10&order=desc&sort=liked_count"
    resp = session_requests.get(URL+PATH, headers=headers)
    if (resp.status_code != 200):
        print("Unable to get comment list for batch: " + str(CURR))
        return 1
    SIZE = json.loads(resp.text)['data']["total"]
    if (SIZE > len(commentList) or not exists):
        while(CURR*10 < SIZE+10):
            excludes=["course_code", "deleted_at", "has_liked"]
            PATH=f"/v1/courses/{COURSEID}/reviews?current="+str(CURR)+"&page_size=10&order=desc&sort=liked_count"
            resp = session_requests.get(URL+PATH, headers=headers)
            if (resp.status_code != 200):
                print("Unable to get comment list for batch: " + str(CURR))
                return 1
            processedData = json.loads(resp.text)['data']["list"]
            for item in processedData:
                print(item)
                tmpLst.append(item)
            CURR+=1
            sleep(random.randint(5,10))
    else:
        print("No new comments for course: " + str(COURSEID))
    if not exists or SIZE > len(commentList):
        with open(f"{DIR}/reviews/{COURSEID}.txt", "w") as f:
            for item in tmpLst:
                f.write(json.dumps(item)+",\n")
```

Note that the program also checks if the review already exists in the `reviews/<COURSENAME>.txt` file. This is done to prevent the program from adding the same review multiple times. The program also sleeps for a random amount of time between 5 and 10 seconds after each request to prevent the API from blocking the request.

The main function is then called, and the program is run.

```python
def main():
    existingCourses = []
    updatedCourseList = False
    token = None
    val = 0
    METHOD = "POST"
    PATH = "/v1/auth"
    SIZE = 10
    CURR = 1
    payload = generatePayload("login", CURR, SIZE)
    headers = generateHeaders(METHOD, PATH, token)
    resp = session_requests.post(URL+PATH, headers = headers ,data=json.dumps(payload))
    if (resp.status_code != 201):
        print("Login failed")
        return
    token = json.loads(resp.text)['data']
    payload = generatePayload("course",CURR, SIZE)
    METHOD = "GET"
    PATH = "/v1/courses?search=&current=1&page_size=10&order=asc&sort=code"
    
    headers = generateHeaders(METHOD, PATH, token)
    resp = session_requests.get(URL+PATH, headers=headers)

    if (resp.status_code != 200):
        print("Unable to get course list")
        return
    SIZE = json.loads(resp.text)['data']['total']
    
    existingCourses = getExistingCourses()

    if (SIZE > len(existingCourses)):
        updatedCourseList = True

    if (updatedCourseList):    
        val = updateCourseList(CURR, SIZE, headers, existingCourses)
        existingCourses = []
        existingCourses = getExistingCourses()
    else:
        print("Course list is up to date")

    if (val == 1):
        print("Unable to update course list")
        return
    
    CURR = 1
    for item in existingCourses:
        updateReviews(CURR, SIZE, headers, item["code"])
    courseName = input("Enter a course name: ")

    METHOD = "GET"
    PATH = "/v1/courses/" + str(courseName)
    headers = generateHeaders(METHOD, PATH, token)
    data = session_requests.get(URL+PATH, headers=headers)
    if (data.status_code != 200):
        print("Unable to get course data")
        return
    processedData = json.loads(data.text)['data']

    for key in processedData:
        if key not in excludes:
            print(str(key) + " : " + str(processedData[key]))

if __name__ == "__main__":
    main()
```