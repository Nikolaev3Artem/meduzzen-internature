import http.client

conn = http.client.HTTPSConnection("dev-wekvb206t4bwb1n8.us.auth0.com")

payload = '{"client_id":"YA4L6tyxTWfJtqj94AscKm28NJMqii0h","client_secret":"fclYC51RKyxdVPJ1WkqYTpEz1L1ZC7SIVaSiLXDhir9CPYpJTV8e2obkIb27BOVE","audience":"https://dev-wekvb206t4bwb1n8.us.auth0.com/api/v2/","grant_type":"client_credentials"}'

headers = {"content-type": "application/json"}

conn.request("POST", "/oauth/token", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
