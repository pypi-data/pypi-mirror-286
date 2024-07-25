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
from rockai_cli_app.data_class import PredictionResponse
from pathlib import Path
from fastapi import Path as FastApiPath
from typing import Any
import asyncio
from rockai_cli_app.server.runner import Runner, RunnerResult
import uuid
from .json import upload_files
from .files import upload_file
from datetime import datetime

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

    class PredictionRequest(
        rockai_cli_app.data_class.PredictionRequest.get_pydantic_model(
            input_type=input_type
        )
    ):
        pass

    InfereceResult = PredictionResponse.get_pydantic_model(
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
        response_model=InfereceResult,
        response_model_exclude_unset=True,
    )
    async def predict(
        request_body: PredictionRequest = Body(default=None),
    ) -> typing.Any:
        """
        Running the prediction.
        """
        logger.debug("prediction called...")
        if request_body is None or request_body.input is None:
            request_body = PredictionRequest(input={})
        request_body = request_body.dict()
        id = uuid.uuid4().hex
        start_time = datetime.now()
        result = await runner.predict(id, pred.predict, request_body, path)
        end_time = datetime.now()
        time_taken = (end_time - start_time).total_seconds()
        final_result = upload_files(
            result, upload_file=lambda fh: upload_file(fh, None)  # type: ignore
        )
        return JSONResponse(
            content=jsonable_encoder(
                InfereceResult(
                    input=request_body["input"],
                    inference_time=time_taken,
                    output=final_result,
                    id=id,
                    started_at=start_time,
                    completed_at=end_time,
                )
            )
        )

    @limited
    @app.post(
        "/predictions/{prediction_id}",
        response_model=InfereceResult,
        response_model_exclude_unset=True,
    )
    async def predic_with_id(
        prediction_id: str = FastApiPath(title="prediction ID"),
        request_body: PredictionRequest = Body(default=None),
    ) -> typing.Any:
        """
        Running the prediction.
        """
        logger.debug("prediction called... ID -> {}".format(prediction_id))
        if request_body is None or request_body.input is None:
            request_body = PredictionRequest(input={})
        request_body = request_body.dict()
        start_time = datetime.now()
        result = await runner.predict(prediction_id, pred.predict, request_body, path)
        end_time = datetime.now()
        time_taken = (end_time - start_time).total_seconds()
        final_result = upload_files(
            result, upload_file=lambda fh: upload_file(fh, None)  # type: ignore
        )
        logger.debug(result)
        if isinstance(result, RunnerResult):
            return JSONResponse(
                content=jsonable_encoder({"msg": result.msg}), status_code=400
            )
        return JSONResponse(
            content=jsonable_encoder(
                InfereceResult(
                    input=request_body["input"],
                    inference_time=time_taken,
                    output=final_result,
                    id=prediction_id,
                    started_at=start_time,
                    completed_at=end_time,
                )
            ),
            status_code=200,
        )

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
                "prediction_id": prediction_id,
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
