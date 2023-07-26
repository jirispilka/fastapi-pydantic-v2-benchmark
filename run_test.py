import itertools
import time

from starlette.testclient import TestClient
import pandas as pd

from app.main import create_app

N = 30
client = TestClient(create_app())

files = ["1kb", "10kb", "100kb", "1mb"]

FUNCS = [
    "1_return__dict__none__none",
    "2_return__dict__pydantic__none",
    "3_return__pydantic__pydantic__none",
    "4_return__dict__pydantic__json",
    "5_return__dict__none__orjson",
    "6_return__dict__pydantic__orjson",
    "7_return__pydantic__pydantic__orjson",
    "8_return__pydantic__pydantic__pydantic_json_response",
]

results = {}
for name, file in itertools.product(FUNCS, files):
    t0 = time.time()
    for _ in range(N):
        r = client.get(name, params={"file": file})
        assert r.status_code == 200
    t1 = time.time()
    v = 1000 * (t1 - t0) / N
    if file in results:
        results[file][name] = v
    else:
        results[file] = {name: v}


from tabulate import tabulate
pd.set_option("display.max_columns", None)
df = pd.DataFrame(results)
print(df.to_markdown(floatfmt=".0f"))
