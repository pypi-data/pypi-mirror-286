def AIMessage(content:str):
    return {"role":"assistant","content":content}

def HumanMessage(content:str):
    return {"role":"user","content":content}

def SystemMessage(content:str):
    return {"role":"system","content":content}