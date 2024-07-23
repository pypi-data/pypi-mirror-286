from NovaForger import ChatModel
from NovaForger.Message import *
BASEURL = "YourBASEURL"
modelname = "YourModelname"
apikey = "YourAPIKEY"


model = ChatModel(BASEURL = BASEURL,modelname=modelname,apikey=apikey)



# history = [
#     {"role":"system","content":"You are a helpful assistant,your name is Alice"},
#     {"role":"user","content":"Hello"},
#     {"role":"assistant","content":"Hello! How can I assist you today?"}
#     ]

history = [
    SystemMessage("You are a helpful assistant,your name is Alice"),
    HumanMessage("Hello"),
    AIMessage("Hello! How can I assist you today?")
]
message = model.run(content="Who are you",history=history)
print(message)