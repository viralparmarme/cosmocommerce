
# Cosmocommerce

A sample E-commerce backend application in FastAPI, Python and MongoDB.


## Run Locally

Clone the project

```bash
  git clone https://github.com/viralparmarme/cosmocommerce
```

Go to the project directory

```bash
  cd cosmocommerce
```

Activate virtual env and nstall dependencies

```bash
  source venv/bin/activate
  pip install -r requirements.txt
```

Start the server

```bash
  uvicorn main:app --reload
```


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`MONGODB_URL`

Please not that I have excluded .env ONLY FOR THIS project so you can directly connect to my MongoDB instance.

## API Reference

FYI, you can also refer to the OpenAPI spec by visiting [http://localhost:8000/docs](http://localhost:8000/docs)

#### Get all products

```http
  GET localhost:8000/products
```
Example response with status 200:
```json
{
    "data": [
        {
            "id": "65b79eb33a27326b787ed9a8",
            "name": "iPhone 15",
            "price": 100.0,
            "available_quantity": 1000
        },
        {
            "id": "65b79f503a27326b787ed9ad",
            "name": "iPhone 14 Pro",
            "price": 800.0,
            "available_quantity": 50
        }
    ],
    "page": {
        "limit": 1000,
        "next_offset": null,
        "prev_offset": null,
        "total": 6
    }
}
```

#### Get product by ID

```http
  GET localhost:8000/products/${id}
```
Example response with status 200:
```json
{
    "id": "65b79f433a27326b787ed9ac",
    "name": "iPhone 15 Pro",
    "price": 1009.0,
    "available_quantity": 9990
}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. ID of product to fetch, eg. 65b79f433a27326b787ed9ac |


#### Place an order

```http
  POST localhost:8000/orders
```

Example order request:
```json
{
    "items": [
        {
            "product_id": "65b79f433a27326b787ed9ac",
            "bought_quantity": 10
        },

        {
            "product_id": "65b79f503a27326b787ed9ad",
            "bought_quantity": 50
        }
    ],
    "total_amount": 1000,
    "user_address": {
        "city": "ABC",
        "country": "IN",
        "zip_code": 123456
    }
}
```
Example response with status 201:
```json
{
    "id": "65b8e73470fdc5be6fe3aef3",
    "created_on": "2024-01-30T12:10:28.046043",
    "items": [
        {
            "product_id": "65b79f433a27326b787ed9ac",
            "bought_quantity": 10
        },
        {
            "product_id": "65b79f503a27326b787ed9ad",
            "bought_quantity": 50
        }
    ],
    "total_amount": 1000,
    "user_address": {
        "city": "ABC",
        "country": "IN",
        "zip_code": 123456
    }
}
```

The APIs will return status codes 200, 404, 400 or 422 based on the success and failure scenarios.

For example, if you get a product with an invalid ID:
```http
  GET localhost:8000/products/abc
```
Example response with status 404:
```json
{
    "detail": "Product abc not found"
}
```

## MongoDB Data Structure

Orders collection
```json
{
  "_id": {
    "$oid": "65b79fb2af81628a0f1a7529"
  },
  "items": [
    {
      "product_id": "65b79ef93a27326b787ed9a9",
      "bought_quantity": 100
    },
    {
      "product_id": "65b79f503a27326b787ed9ad",
      "bought_quantity": 50
    }
  ],
  "total_amount": 1000,
  "user_address": {
    "city": "ABC",
    "country": "IN",
    "zip_code": 123456
  },
  "created_on": {
    "$date": "2024-01-29T12:53:06.409Z"
  }
}
```

Products collection
```json
{
  "_id": {
    "$oid": "65b79fb2af81628a0f1a7529"
  },
  "items": [
    {
      "product_id": "65b79ef93a27326b787ed9a9",
      "bought_quantity": 100
    },
    {
      "product_id": "65b79f503a27326b787ed9ad",
      "bought_quantity": 50
    }
  ],
  "total_amount": 1000,
  "user_address": {
    "city": "ABC",
    "country": "IN",
    "zip_code": 123456
  },
  "created_on": {
    "$date": "2024-01-29T12:53:06.409Z"
  }
}
```

## Further optimizations

Due to lack of time, I could not add one logical check: 

The order amount in the create order requuest should be equal to the sum of products of price and quantity of an item for all the items in the order.
## Authors

- [@viralparmarme](https://github.com/viralparmarme)


## Acknowledgements

 A special thanks to Cosmocloud for sharing this backend hiring task. I got to learn a few things in the process of writing the code too.

