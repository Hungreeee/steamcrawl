from steamcrawl import Request
import requests
import json
import pandas as pd

a = Request('76561199200399595%7C%7CeyAidHlwIjogIkpXVCIsICJhbGciOiAiRWREU0EiIH0.eyAiaXNzIjogInI6MTZFNF8yMjYxRTEzRV8wMEU4NyIsICJzdWIiOiAiNzY1NjExOTkyMDAzOTk1OTUiLCAiYXVkIjogWyAid2ViIiBdLCAiZXhwIjogMTY4MzY0ODYxMiwgIm5iZiI6IDE2NzQ5MjE2MjcsICJpYXQiOiAxNjgzNTYxNjI3LCAianRpIjogIjBEMjhfMjI3QjQxRDZfRkU2MTIiLCAib2F0IjogMTY4MTQ1NjgzNSwgInJ0X2V4cCI6IDE2OTk1NzUxNDEsICJwZXIiOiAwLCAiaXBfc3ViamVjdCI6ICI4Ni41MC4xNDEuMTE4IiwgImlwX2NvbmZpcm1lciI6ICI4Ni41MC4xNDEuMTE4IiB9.UqSNZQqYQuQejqlBYvu53OA6-G0aZtpNzB12LsMn6BHYrh2UaXLp-Sz1zxaY9IO2HJR61kH3ege0p6TmGbReBg')
a.get_market_history('76561199200399595', "730", 1000).to_csv('test.csv')
  
# headers = {
#   "Cookie":'76561199200399595%7C%7CeyAidHlwIjogIkpXVCIsICJhbGciOiAiRWREU0EiIH0.eyAiaXNzIjogInI6MTZFNF8yMjYxRTEzRV8wMEU4NyIsICJzdWIiOiAiNzY1NjExOTkyMDAzOTk1OTUiLCAiYXVkIjogWyAid2ViIiBdLCAiZXhwIjogMTY4MzY0ODYxMiwgIm5iZiI6IDE2NzQ5MjE2MjcsICJpYXQiOiAxNjgzNTYxNjI3LCAianRpIjogIjBEMjhfMjI3QjQxRDZfRkU2MTIiLCAib2F0IjogMTY4MTQ1NjgzNSwgInJ0X2V4cCI6IDE2OTk1NzUxNDEsICJwZXIiOiAwLCAiaXBfc3ViamVjdCI6ICI4Ni41MC4xNDEuMTE4IiwgImlwX2NvbmZpcm1lciI6ICI4Ni41MC4xNDEuMTE4IiB9.UqSNZQqYQuQejqlBYvu53OA6-G0aZtpNzB12LsMn6BHYrh2UaXLp-Sz1zxaY9IO2HJR61kH3ege0p6TmGbReBg'
# }

# a = requests.get('https://steamcommunity.com/inventory/76561199200399595/730/2?l=english&count=100', headers=headers)
# jsonObject = json.loads(a.content)['descriptions']
# pd.json_normalize(jsonObject).to_csv('test.csv')