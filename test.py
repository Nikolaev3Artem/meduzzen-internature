import http.client

conn = http.client.HTTPConnection("dev-wekvb206t4bwb1n8.us.auth0.com")

headers = {
    "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFydG5pazM0OUBnbWFpbC5jb20iLCJpc3MiOiJodHRwczovL2Rldi13ZWt2YjIwNnQ0YndiMW44LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDEwNTI2OTUxMDA4MDA5NTI4Mjc0OCIsImF1ZCI6WyIvbG9naW4iXSwiaWF0IjoxNzEzODk1NzIzLCJleHAiOjE3MTM5ODIxMjMsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJhenAiOiI5dWprTXpTRnZCTllOUXE5REFEVWtmUnF3Q0VHM1lXbyJ9.XhBQppzSxbUVwRc4uIFVORBGuYb6UYj6xTfCr8rPRUg"
}

conn.request("GET", "/", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
