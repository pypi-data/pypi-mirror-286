import asyncio
import json
import typing as t
from json import JSONDecodeError

from httpx import AsyncClient
from pydantic import BaseModel, ValidationError

from lifeomic_chatbot_tools._utils import ImportExtraError


try:
    import boto3
except ImportError:
    raise ImportExtraError("aws", __name__)


class _AsyncLambdaClient:
    def __init__(self):
        self.__client: t.Any = None

    @property
    def _client(self):
        """Lazily instantiated boto3 Lambda client."""
        if not self.__client:
            self.__client = boto3.client("lambda")
        return self.__client

    async def invoke(self, FunctionName: str, Payload: str):
        """
        A wrapper around boto3's Lambda `invoke` method that makes the call asynchronous, enabling parallel Lambda
        invocations to be made in Python code. The Lambda is still invoked synchronously, but the Python code can
        continue to run other tasks while waiting for the Lambda to complete.
        """
        loop = asyncio.get_running_loop()
        res = await loop.run_in_executor(None, lambda: self._client.invoke(FunctionName=FunctionName, Payload=Payload))
        return res


class AlphaResponse(BaseModel):
    status_code: int  # the http response status code
    text: str  # the http response body

    @property
    def body(self):
        """Attempts to parse the response body as JSON."""
        try:
            return json.loads(self.text)
        except JSONDecodeError as e:
            raise RuntimeError(f"could not parse text {self.text} as json, reason: {e}")

    @property
    def ok(self):
        """Returns ``True`` if the response's status code is in the 200-300 range."""
        return self.status_code < 400

    def raise_for_status(self):
        """Raises an exception if the response status code is not in the 200-300 range."""
        if not self.ok:
            raise AssertionError(f"Found not ok status {self.status_code}. Response body: {self.text}")


class Alpha:
    """
    A minimal Python port of LifeOmic's `alpha` utility for calling Lambda functions that operate
    as web services using the [AWS API Gateway event format](https://docs.aws.amazon.com/lambda/latest/dg/services-apiga
    teway.html#apigateway-example-event).
    """

    def __init__(self, target: str):
        """
        If ``target`` begins with ``lambda://`` e.g. ``lambda://function-name``, then ``boto3`` will attempt to use the
        environment credentials and call an actual Lambda function named ``function-name``. Alternatively, an actual URL
        can be passed in as the ``target`` to support calling e.g. a locally running Lambda function.
        """
        self._target = target
        self._lambda_client: t.Optional[_AsyncLambdaClient] = None
        self._http_client: t.Optional[AsyncClient] = None
        prefix = "lambda://"
        if target.startswith(prefix):
            self._target = target[len(prefix) :]
            self._lambda_client = _AsyncLambdaClient()
        else:
            self._http_client = AsyncClient()

    def get(
        self, path: str, params: t.Optional[t.Dict[str, t.Any]] = None, headers: t.Optional[t.Dict[str, str]] = None
    ):
        payload = self._make_payload(path=path, method="GET", params=params, headers=headers)
        return self._invoke_lambda(payload)

    def post(self, path: str, body: t.Any = None, headers: t.Optional[t.Dict[str, str]] = None):
        payload = self._make_payload(path=path, method="POST", body=body, headers=headers)
        return self._invoke_lambda(payload)

    def put(self, path: str, body: t.Any = None, headers: t.Optional[t.Dict[str, str]] = None):
        payload = self._make_payload(path=path, method="PUT", body=body, headers=headers)
        return self._invoke_lambda(payload)

    def delete(self, path: str, headers: t.Optional[t.Dict[str, str]] = None):
        payload = self._make_payload(path=path, method="DELETE", headers=headers)
        return self._invoke_lambda(payload)

    @staticmethod
    def _make_payload(
        path: str,
        method: str,
        body: t.Any = None,
        params: t.Optional[t.Dict[str, t.Any]] = None,
        headers: t.Optional[t.Dict[str, str]] = None,
    ):
        payload: t.Dict[str, t.Union[str, t.Dict[str, str]]] = {"path": path, "httpMethod": method}
        if body:
            payload["body"] = json.dumps(body)
        if params:
            payload["queryStringParameters"] = params
        if headers:
            payload["headers"] = headers
        return payload

    async def _invoke_lambda(self, payload: dict):
        if self._lambda_client:
            res = await self._lambda_client.invoke(FunctionName=self._target, Payload=json.dumps(payload))
            return self._parse_response(res["Payload"].read())
        else:
            assert self._http_client  # this should never fail but we put it here to satisfy the typing engine
            res = await self._http_client.post(self._target, json=payload)
            return self._parse_response(res.content)

    @staticmethod
    def _parse_response(payload: bytes):
        """Creates an `AlphaResponse` object from a raw Lambda response payload."""
        try:
            parsed = json.loads(payload.decode("utf-8"))
            return AlphaResponse(status_code=parsed["statusCode"], text=parsed["body"])
        except (JSONDecodeError, KeyError, ValidationError) as e:
            raise RuntimeError(f"could not parse payload {payload!r} as an API Gateway event, reason: {e}")
