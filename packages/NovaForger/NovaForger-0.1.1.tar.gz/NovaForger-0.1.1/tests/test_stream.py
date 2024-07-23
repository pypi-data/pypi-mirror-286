from NovaForger import ChatModel
BASEURL = "YourBASEURL"
modelname = "YourModelname"
apikey = "YourAPIKEY"

model = ChatModel(BASEURL = BASEURL,modelname=modelname,apikey=apikey)

messages = ""
for message in model.stream("What you're going to do next"):
    print(message)
    messages += message

print(f"message:{messages}")