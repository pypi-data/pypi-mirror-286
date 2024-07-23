from NovaForger import ChatModel
from NovaForger.tools import pythonRuner
BASEURL = "YourBASEURL"
modelname = "YourModelname"
apikey = "YourAPIKEY"

model = ChatModel(BASEURL = BASEURL,modelname=modelname,apikey=apikey)
model.add_tools(pythonRuner)
messages = ""
for message in model.stream_with_tools(content="What time is now",max_token=150,temperature=0.1):
    print(message)
    messages += message

print(f"message:{messages}")