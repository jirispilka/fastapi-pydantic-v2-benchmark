# fastapi-pydantic-v2-benchmark

Understand how FastAPI is internally serializing JSON data when it is returned. Originally it was intended to explore
serialization speed of fastapi with pydantic v1. Later, a comparison to fastapi with pydantic v2 was added.

# Install

```shell
pipenv install
```

## Install with pydantic-v1

In the Pipfile you need to setup pydantic lower than 2.0.0 `pydantic = "<=2.0.0"` and then run `pipenv update`

## Install with pydantic-v2

Change the version of pydantic to pydantic `>=2.0.0` and run then `pipenv update`

# Benchmark data

[data_1kb.json](data%2Fdata_1kb.json)  
[data_1mb.json](data%2Fdata_1mb.json)  
[data_10kb.json](data%2Fdata_10kb.json)  
[data_100kb.json](data%2Fdata_100kb.json)  

Example of data_1kb.json (reformatted with a new line characters for better readability)

```json
{
  "_id": "zNSjA3ONYySYXFut Cwo2iPq",
  "business_name": "3ttf7M9Dv",
  "created_at": "",
  "updated_at": "",
  "customers": [
    {
      "customer_id": "08auCb0H",
      "mobile": "kH3auvXBi5",
      "name": "aRXpkU",
      "email": "",
      "dob": "",
      "created_at": "c 49f3aMKd",
      "updated_at": "zAnUv0sDJy"
    }
  ],
  "bookings": [
    {
      "booking_id": "4v0C3rd8U0h69f",
      "service_name": "EHJMMF1JHxeK95M9VVh49U",
      "date": "siTTpyjrw7",
      "start_time": "XJ4JjU39",
      "readable_booking": "e3RzIxLM7yMFi9K4w52zS5XYeYGWOwIOtsEIIcmjzqderP1m4edrIq5BQxqkvHXktcGYPHvuH",
      "created_at": "0MdAo4LQ3d",
      "updated_at": "IzF42ltRTq",
      "num_of_customers": "",
      "status": "F1PEiS",
      "readable_booking_with_id": {
        "text": "dECE6MItzRx03Bk23AOIHhrFJDB7USI7UBPaOXVV6cyrBDXb591NHV6 ANHrlIoopTLSjX OH",
        "post_back": "pAIawNXs5EiVTy"
      }
    }
  ],
  "services": [
    {
      "service_id": "gPSMVWepaWc5EfCRNcLp",
      "name": "AErs24kQfWeQWFt0Z",
      "created_at": "wBPN7zQyiQyXDWvLRYMwry4R",
      "updated_at": "cJMrtZT85L0K7f3rouXBoEZe"
    }
  ],
  "resources": []
}
```

# Versions

HW:
```text
CPU: 11th Gen Intel(R) Core(TM) i7-1185G7 @ 3.00GHz
```

## pydantic v1
```text
fastapi==0.100.0
httpcore==0.17.3
httptools==0.6.0
orjson==3.9.2
pydantic==1.10.12
starlette==0.27.0
```

## pydantic v2
```text
fastapi==0.100.0
httpcore==0.17.3
httptools==0.6.0
orjson==3.9.2
pydantic==2.1.1
pydantic_core==2.4.0
starlette==0.27.0
```

# Comments

 - `jsonable_encoder` is an internal fastapi function
 - `model.dict()` and `model.json()` are internal pydantic functions
 - `orjson` - library to serialize dict to json written in rust
 - `ORJSONResponse`
   - skips fastapi internals like validation, serialization
    - comment from the fastapi maintainer (reference missing): "Yep, returning responses directly is an escape hatch 
      for you to override anything FastAPI would do and take over directly. It is not intended as the main use case.
      And yes, this means there are two ways to do things, do them through the normal ways, returning data directly,
      or taking over the wheel and doing things yourself. It's not great to have two ways to do things, but there's
      no other way to let you take the wheel, so we have to leave with that.
      Also, any data validation won't be done, and no additional headers or background tasks will be set

# Test functions and APIs

Several combinations of returned data types, response model, and response class are created.
For instance, in the simplest use case, one could return a plain Python dictionary without any specified response model
or response class. This is henceforth referred to as `return_dict_none_none`.

Python code:
```text
@router.get("/1_return__dict__none__none")
def return__dict__none__none(file: files):
    return DATA[file]
```
Alternatively, one could return a Pydantic model, with a response Pydantic model, and the default response class:
```text
@router.get("/3_return__pydantic__pydantic__none", response_model=BusinessModel)
def return_pydantic_pydantic_none(file: files):
    return DATA_OBJ[file]
```
Here's what each endpoint does:
- `1_return__dict__none__none`: Fastapi calls `jsonable_encoder`, which takes dict and ensures that all fields (Enum, Path, datetime) are JSON serializable 
- `2_return__dict__pydantic__none`: Fastapi creates a pydantic model in `prepare_response_content` based on response model then runs `jsonable_encoder` (calls model.dict() and again iterates over all fields and ensures that are JSON serializable)
- `3_return__pydantic__pydantic__none`: Create python dictionary using `model.dict()` →  in `prepare_response_content` create pydantic model model based on response model definition →  run `jsonable_encoder` (calls `model.dict()` and again iterates over all fields and ensures that are JSON serializable)
- `4_return__dict__pydantic__json`: Dump dict to JSON using a standard library 
- `5_return__dict__none__orjson`: Dump dict to JSON using orjson library
- `6_return__dict__pydantic__orjson`: Dump dict to JSON using orjson library (Response model is used only for openapi documentation)
- `7_return__pydantic__pydantic__orjson`: Call `model.dict()` and return dict using orjson library
- `8_return__pydantic__pydantic__pydantic_json_response`: Call `model.json()` and return it

# Results in ms (lower is better) - pydantic v1

|                                                      |   1kb |   10kb |   100kb |   1mb |
|:-----------------------------------------------------|------:|-------:|--------:|------:|
| 1_return__dict__none__none                           |     2 |      3 |      13 |    97 |
| 2_return__dict__pydantic__none                       |     2 |      6 |      31 |   261 |
| 3_return__pydantic__pydantic__none                   |     2 |      7 |      38 |   311 |
| 4_return__dict__pydantic__json                       |     2 |      2 |       2 |    12 |
| 5_return__dict__none__orjson                         |     2 |      2 |       2 |     4 |
| 6_return__dict__pydantic__orjson                     |     2 |      2 |       2 |     3 |
| 7_return__pydantic__pydantic__orjson                 |     2 |      3 |      10 |    68 |
| 8_return__pydantic__pydantic__pydantic_json_response |     2 |      3 |      11 |    81 |

# Results in ms (lower is better) - pydantic v2

|                                                      |   1kb |   10kb |   100kb |   1mb |
|:-----------------------------------------------------|------:|-------:|--------:|------:|
| 1_return__dict__none__none                           |     2 |      2 |      10 |    68 |
| 2_return__dict__pydantic__none                       |     2 |      2 |       3 |    27 |
| 3_return__pydantic__pydantic__none                   |     2 |      2 |       3 |    15 |
| 4_return__dict__pydantic__json                       |     2 |      2 |       3 |    11 |
| 5_return__dict__none__orjson                         |     2 |      2 |       2 |     3 |
| 6_return__dict__pydantic__orjson                     |     2 |      2 |       2 |     3 |
| 7_return__pydantic__pydantic__orjson                 |     2 |      2 |       2 |    10 |
| 8_return__pydantic__pydantic__pydantic_json_response |     2 |      2 |       2 |     5 |



# References:
- [Validation in the FastAPI response handler is a lot heavier than expected #1359](https://github.com/tiangolo/fastapi/issues/1359)
- [Enhance serialization speed #360](https://github.com/tiangolo/fastapi/issues/360)
- [Return a Response Directly](https://fastapi.tiangolo.com/advanced/response-directly/)