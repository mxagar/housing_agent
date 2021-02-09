# Housing Analysis
This small project analyzes some real estate data.

API key:
cat key.txt
echo -n 'key:secret' | base64
we get base64(key:secrect)

Example call:
curl -X POST -H "Authorization: Basic <base64 key:secrect>" -H "Content-Type: application/x-www-form-urlencoded" -d 'grant_type=client_credentials&scope=read' "https://api.idealista.com/oauth/token" -k
