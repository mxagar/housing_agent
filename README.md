# Housing Agent

This small project analyzes some real estate data from [idealista](https://www.idealista.com/en/) and tries to find nice matches for defined user preferences.

### Usage

The Idealista API key is in the non-committed key file:

```bash
cat key.txt
echo -n 'key:secret' | base64
# we get base64(key:secrect)
```

Example call:

```bash
curl -X POST -H "Authorization: Basic <base64 key:secrect>" -H "Content-Type: application/x-www-form-urlencoded" -d 'grant_type=client_credentials&scope=read' "https://api.idealista.com/oauth/token" -k
```

### Interesting Links

- [SaaS Boilerplates](https://github.com/smirnov-am/awesome-saas-boilerplates)