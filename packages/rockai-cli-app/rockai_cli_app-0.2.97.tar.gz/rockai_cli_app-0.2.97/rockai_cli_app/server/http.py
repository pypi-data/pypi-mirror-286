from fastapi import FastAPI, Body, Header
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import os
import signal
from rockai_cli_app.predictor import BasePredictor
import uvicorn
from rockai_cli_app.parser.config_util import (
    parse_config_file,
    get_predictor_class_name,
    get_predictor_path,
)
from rockai_cli_app.server.utils import (
    load_class_from_file,
    get_input_type,
    get_output_type,
)
import rockai_cli_app.data_class
import typing
import logging
from rockai_cli_app.data_class import InferenceResponse
from pathlib import Path
from fastapi import Path as FastApiPath
from typing import (
    TYPE_CHECKING,
    Any,
    Awaitable,
    Callable,
    Dict,
    Optional,
    TypeVar,
)

if TYPE_CHECKING:
    from typing import ParamSpec
import asyncio
import concurrent.futures
import functools

# Set up logging
logging.basicConfig(level=logging.DEBUG)  # Set the initial logging level to INFO

# Create a logger
logger = logging.getLogger(__name__)


class MyFastAPI(FastAPI):
    pass


def create_app(path: Path) -> MyFastAPI:

    app: MyFastAPI = MyFastAPI()
    future_map = {}

    pred: BasePredictor = load_class_from_file(
        Path.cwd() / get_predictor_path(parse_config_file(path / "rock.yaml")),
        get_predictor_class_name(parse_config_file(path / "rock.yaml")),
        BasePredictor,
    )

    input_type = get_input_type(pred)

    output_type = get_output_type(pred)

    class InferenceRequest(
        rockai_cli_app.data_class.InferenceRequest.get_pydantic_model(
            input_type=input_type
        )
    ):
        pass

    InfereceResult = InferenceResponse.get_pydantic_model(
        input_type=input_type, output_type=output_type
    )

    http_semaphore = asyncio.Semaphore(1)

    if TYPE_CHECKING:
        P = ParamSpec("P")
        T = TypeVar("T")

    def limited(f: "Callable[P, Awaitable[T]]") -> "Callable[P, Awaitable[T]]":
        @functools.wraps(f)
        async def wrapped(*args: "P.args", **kwargs: "P.kwargs") -> "T":
            async with http_semaphore:
                return await f(*args, **kwargs)

        return wrapped

    @app.on_event("startup")
    async def start_up_event():
        """
        Run the setup function of the predictor and load the model
        """
        logger.debug("setup start...")
        pred.setup()
        logger.debug("setup finish...")

    @limited
    @app.post(
        "/predictions",
        response_model=InferenceRequest,
        response_model_exclude_unset=True,
    )
    async def predict(
        request_body: InferenceRequest = Body(default=None),
    ) -> typing.Any:
        """
        Running the prediction.
        """
        logger.debug("prediction called...")
        if request_body is None or request_body.input is None:
            request_body = InferenceRequest(input={})
        request_body = request_body.dict()
        loop = asyncio.get_running_loop()
        with concurrent.futures.ThreadPoolExecutor() as pool:
            partial_pred = functools.partial(pred.predict, **request_body["input"])
            result = await loop.run_in_executor(pool, partial_pred)
        return JSONResponse(content=jsonable_encoder(InfereceResult(output=result)))
    
    @limited
    @app.post(
        "/predictions/{prediction_id}",
        response_model=InferenceRequest,
        response_model_exclude_unset=True,
    )
    async def predic_with_id(
        prediction_id: str = FastApiPath(title="prediction ID"),
        request_body: InferenceRequest = Body(default=None),
    ) -> typing.Any:
        """
        Running the prediction.
        """
        logger.debug("prediction called... ID -> {}".format(prediction_id))
        if request_body is None or request_body.input is None:
            request_body = InferenceRequest(input={})
        request_body = request_body.dict()
        loop = asyncio.get_running_loop()
        with concurrent.futures.ThreadPoolExecutor() as pool:
            partial_pred = functools.partial(pred.predict, **request_body["input"])
            future = loop.run_in_executor(pool, partial_pred)
            future_map[prediction_id] = future
            result = await future_map[prediction_id]
            del future_map[prediction_id]

        return JSONResponse(content=jsonable_encoder(InfereceResult(output=result)))

    @app.post("/predictions/{prediction_id}/cancel")
    async def cancel(prediction_id: str) -> Any:
        """Cancel prediction by id"""
        logger.debug("cancel prediction start...{}".format(prediction_id))
        if prediction_id in future_map:
            cancel_future = future_map.pop(prediction_id)
            result = cancel_future.cancel()
            return JSONResponse(
                content={
                    "message": "Prediction {} is cancelled -> {}".format(
                        prediction_id, result
                    ),
                    "is_canceled": result,
                },
                status_code=200,
            )
        else:
            return JSONResponse(
                content={
                    "message": "Prediction ID {} is not found".format(prediction_id),
                    "is_canceled": False,
                },
                status_code=404,
            )

    @app.post("/shutdown")
    async def shutdown():
        """
        Shutdown the server.
        """
        pid = os.getpid()
        os.kill(pid, signal.SIGINT)
        return JSONResponse(content={"message": "Shutting down"}, status_code=200)

    @app.get("/")
    async def root():
        """
        Hello World!, when you see this message, it means the server is up and running.
        """
        return JSONResponse(
            content={"docs_url": "/docs", "model_schema": "/openapi.json"},
            status_code=200,
        )

    # finally create the application
    return app


def start_server(port):
    app = create_app(path=Path.cwd())
    uvicorn.run(app, host="0.0.0.0", port=port)
