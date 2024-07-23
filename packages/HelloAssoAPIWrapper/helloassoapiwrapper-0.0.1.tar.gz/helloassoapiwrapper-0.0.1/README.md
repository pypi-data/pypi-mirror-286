# HelloAsso API Wrapper

[![versions](https://img.shields.io/pypi/pyversions/HelloAssoAPIWrapper)](https://github.com/aeecleclair/HelloAssoAPIWrapper)
[![license](https://img.shields.io/github/license/aeecleclair/HelloAssoAPIWrapper)](https://github.com/aeecleclair/HelloAssoAPIWrapper/blob/main/LICENSE)
[![Pydantic v2](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json)](https://pydantic.dev)

A Python wrapper for the HelloAsso API, using [Pydantic](https://docs.pydantic.dev/latest/) for models validation.

# Usage

```python
from HelloAssoAPIWrapper import HelloAssoAPIWrapper
```

### Notification result webhooks

You should configure a webhook to receive the notification results.
HelloAsso will make a POST request to the URL you provided with a JSON payload corresponding to a `NotificationResultContent` object.

## HelloAsso sandbox

HelloAsso provide a sandbox: api.helloasso-sandbox.com

# Development

Models when first generated using HelloAsso swagger documentation, and then adapted to include additional models, use stricter types and add documentation

## Add new methods

todo

## Models auto-generation

Download the swagger file from the HelloAsso API documentation. It use an old swagger 2 version. You need to convert it to OpenAPI 3.0.0 version. You can use the online tool [Swagger Editor](https://editor.swagger.io/).

Then you can use the [datamodel-codegen](https://docs.pydantic.dev/latest/integrations/datamodel_code_generator/) tool to generate the models:

```bash
datamodel-codegen --input HelloAssoV5OpenAPI.json --output HelloAssoAPIWrapper
```

Make a release on Pypi

You need to edit HelloAssoAPIWrapper version in [helloasso_api_wrapper/\_\_about\_\_.py](./helloasso_api_wrapper/__about__.py). Then make a release on GitHub and add a tag. The tag should match v*.*.\*.

