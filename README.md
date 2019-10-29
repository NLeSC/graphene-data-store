Graphene+Flask+SQLAlchemy
================================

# Setup
---------------

Create a virtual environment

```bash
virtualenv venv
source venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Setup the database, and start the server:

```bash
./app.py

```


Now open
[http://127.0.0.1:5000/graphql](http://127.0.0.1:5000/graphql)
and run queries!

## Example queries

### Example-1
---------------

```
{
  allDatasets {
    edges {
      node {
        id
        name
        data
      }
    }
  }
}
```

### Example-2
---------------

```
query Dataset($id: ID!){
  dataset(id: $id) {
    id
    name
    items {
      keyData
    }
  }
}
```

variables:
```
{
  "id": "RGF0YXNldDox"
}
```


### Example-3
---------------

```
{
  dataset (id:"RGF0YXNldDox") {
    id
    name
    items {
      keyData
    }
  }
}
```