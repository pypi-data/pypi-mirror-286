from NovaForger import ChatModel
from NovaForger.tools import pythonRuner
BASEURL = "YourBASEURL"
modelname = "YourModelname"
apikey = "YourAPIKEY"

model = ChatModel(BASEURL = BASEURL,modelname=modelname,apikey=apikey)

model.add_tools(pythonRuner)
message = model.run_with_tools("What time is now",max_token=150,temperature=0.1)
print(f"message:{message}")