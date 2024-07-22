# DMessage

DMessage 是一個簡單的 Python 套件，透過 webhook 發送訊息到 Discord 的 channel。

## 安裝

```bash
pip install dmessage
```

## 使用

```python
import os
from dmessage import DMessage

os.environ["WEBHOOK_ID"] = "YOUR_WEBHOOK_ID"
os.environ["WEBHOOK_TOKEN"] = "YOUR_WEBHOOK_TOKEN"

message = "Hello, World!"

dm = DMessage()
dm.send(message)
```