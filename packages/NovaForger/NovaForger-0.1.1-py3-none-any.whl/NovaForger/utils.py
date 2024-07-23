from typing import List, Tuple, Dict, Any
import json
def build_history(conversations: List[Tuple[str, str]]) -> List[Dict[str, str]]:
    """
    构造对话历史记录的方法。

    :param conversations: 包含多轮对话的列表，每个元素是一个 (role, message) 的元组。
    :return: 构造好的对话历史记录列表。
    """
    history = []
    for role, message in conversations:
        history.append({"role": role, "content": message})
    return history


def readObject(obj: str) -> Tuple[str, Dict[str, Any]]:
    data = json.loads(obj)
    message = data['choices'][0]['message']['content']
    usage = data['usage']
    return message, usage


