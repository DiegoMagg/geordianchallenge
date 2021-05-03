# geordianchallenge

[![codecov](https://codecov.io/gh/DiegoMagg/geordianchallenge/branch/main/graph/badge.svg?token=8PVYAMJNJH)](https://codecov.io/gh/DiegoMagg/geordianchallenge)

requirements:

1. [python3.8](http://https://www.python.org/ "1. python3.8")

## Instructions:

### Setup:

    $ git clone git@github.com:DiegoMagg/geordianchallenge.git


### Parsing files:

    $ python seatmap_parser.py seatmap1.xml
    $ python seatmap_parser.py seatmap2.xml

The output will be seatmap1_parsed.json and seatmap2_parsed.json
with the following structure (minified example):
```json
    {
      "seat_map":[
        {
          "cabin_layout":"AB EF",
          "cabin_type":"first",
          "row_one":[
            {
              "seat_id":"1A",
              "occupied":false,
              "features":[
                "window"
              ],
              "fee":{
                "amount":1200,
                "currency_code":"usd"
              },
              "taxes":{
                "amount":0,
                "currency_code":"usd"
              }
            },
            {
              "seat_id":"1B",
              "occupied":false,
              "features":[
                "aisle"
              ],
              "fee":{
                "amount":null,  # null if no seat price
                "currency_code":null
              },
              "taxes":{
                "amount":null,
                "currency_code":null
              }
            }
          ],
          "row_two":[
            {
              "seat_id":"2A",
              "occupied":false,
              "features":[
                "window"
              ],
              "fee":{
                "amount":1300,
                "currency_code":"usd"
              },
              "taxes":{
                "amount":0,
                "currency_code":"usd"
              }
            },
            {
              "seat_id":"2B",
              "occupied":false,
              "features":[
                "aisle"
              ],
              "fee":{
                "amount":null,
                "currency_code":null
              },
              "taxes":{
                "amount":null,
                "currency_code":null
              }
            }
          ]
        },
        {
          "cabin_layout": "ABC DEF",
          "cabin_type":"economy",
          "row_seven":[
            {
              "seat_id":"7A",
              "occupied":false,
              "features":[
                "window"
              ],
              "fee":{
                "amount":null,
                "currency_code":null
              },
              "taxes":{
                "amount":null,
                "currency_code":null
              }
            }
          ],
          "row_eight":[
            {
              "seat_id":"8A",
              "occupied":false,
              "features":[
                "window"
              ],
              "fee":{
                "amount":null,
                "currency_code":null
              },
              "taxes":{
                "amount":null,
                "currency_code":null
              }
            },
            {
              "seat_id":"8B",
              "occupied":false,
              "features":[
                "aisle"
              ],
              "fee":{
                "amount":null,
                "currency_code":null
              },
              "taxes":{
                "amount":null,
                "currency_code":null
              }
            }
          ]
        }
      ],
      "flight":{
        "number":"1179",
        "departure_airport":"LAS",
        "arrival_airport":"IAH",
        "departure_date_time":"2020-11-22T15:30:00",
        "air_equip_type":"739"
      }
    }
```

# Testing

    $ python tests.py

with code coverage:

    $ python3 -m venv env
    $ source env/bin/activate
    $ pip install -r requirements-dev.txt
    $ ./test.sh
