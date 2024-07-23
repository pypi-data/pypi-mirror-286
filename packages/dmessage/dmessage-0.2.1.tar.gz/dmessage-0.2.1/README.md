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

os.environ["WEBHOOK_URL"] = "YOUR_WEBHOOK_URL"

dm = DMessage()
dm.send("Hello, World!")
```