from fastapi import FastAPI, Body
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
from typing import Any
import asyncio
from rockai_cli_app.server.runner import Runner, RunnerResult
import uuid
# Set up logging
logging.basicConfig(level=logging.DEBUG)  # Set the initial logging level to INFO

# Create a logger
logger = logging.getLogger(__name__)


class MyFastAPI(FastAPI):
    pass


def load_predictor_from_file(path) -> BasePredictor:
    pred: BasePredictor = load_class_from_file(
        Path.cwd() / get_predictor_path(parse_config_file(path / "rock.yaml")),
        get_predictor_class_name(parse_config_file(path / "rock.yaml")),
        BasePredictor,
    )
    return pred


def create_app(path: Path) -> MyFastAPI:

    app: MyFastAPI = MyFastAPI()

    pred: BasePredictor = load_predictor_from_file(path)

    input_type = get_input_type(pred)

    output_type = get_output_type(pred)

    runner = Runner()

    class InferenceRequest(
        rockai_cli_app.data_class.InferenceRequest.get_pydantic_model(
            input_type=input_type
        )
    ):
        pass

    InfereceResult = InferenceResponse.get_pydantic_model(
        input_type=input_type, output_type=output_type
    )

    semaphore = asyncio.BoundedSemaphore(1)

    def limited(func):
        async def wrapper(*args, **kwargs):
            async with semaphore:
                return await func(*args, **kwargs)

        return wrapper

    @app.on_event("startup")
    async def start_up_event():
        """
        Run the setup function of the predictor and load the model
        """
        logger.debug("setup start...")
        pred.setup()
        logger.debug("setup finish...")

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
        id = uuid.uuid4().hex
        result = await runner.predict(id,request_body, path)
        return JSONResponse(content=jsonable_encoder(InfereceResult(output=result,id=id)))

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
        result = await runner.predict(prediction_id, request_body, path)
        logger.debug(result)
        if isinstance(result, RunnerResult):
            return JSONResponse(
                content=jsonable_encoder({"msg": result.msg}), status_code=400
            )
        return JSONResponse(content=jsonable_encoder(InfereceResult(output=result,id=prediction_id)))

    @app.post("/predictions/{prediction_id}/cancel")
    async def cancel(prediction_id: str) -> Any:
        result = runner.cancel(prediction_id)
        """Cancel prediction by id"""
        logger.debug("cancel prediction start...{}".format(prediction_id))
        return JSONResponse(
            content={
                "message": "Prediction {} is cancelled -> {}".format(
                    prediction_id, result
                ),
                "is_canceled": result,
                "prediction_id":prediction_id
            },
            status_code=200,
        )

    @app.post("/shutdown")
    async def shutdown():
        """
        Shutdown the server.
        """
        runner.clean_up()
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
