from rockai_cli_app.predictor import BasePredictor
import asyncio
from pebble import ProcessFuture, ProcessPool
from rockai_cli_app.parser.config_util import (
    parse_config_file,
    get_predictor_class_name,
    get_predictor_path,
)
from rockai_cli_app.server.utils import (
    load_class_from_file,
)
from pathlib import Path
import logging


def load_predictor_from_file(path) -> BasePredictor:
    pred: BasePredictor = load_class_from_file(
        Path.cwd() / get_predictor_path(parse_config_file(path / "rock.yaml")),
        get_predictor_class_name(parse_config_file(path / "rock.yaml")),
        BasePredictor,
    )
    return pred


def predict_woker(request_body, path):
    pred: BasePredictor = load_predictor_from_file(path)
    return pred.predict(**request_body["input"])


class RunnerResult:
    def __init__(self, msg):
        self.msg = msg


class Runner:
    def __init__(self) -> None:
        self.futures = {}

    async def predict(self, id, request_body, path):
        if id not in self.futures:
            with ProcessPool(max_workers=5, max_tasks=10) as pool:
                future = pool.schedule(
                    predict_woker, kwargs={"request_body": request_body, "path": path}
                )
                self.futures[id] = future
                while future.done() is False:
                    await asyncio.sleep(0.1)
                del self.futures[id]
                return future.result()
        else:
            return RunnerResult(
                "A prediction is already running with id -> {}".format(id)
            )
    
    

    def cancel(self, id) -> bool:
        if id not in self.futures:
            return False  # prediction is not found
        result: ProcessFuture = self.futures[id]
        result.cancel()
        del self.futures[id]
        logging.debug("Cancel result {}".format(result))
        return result
    
    def clean_up(self):
        for id, future in self.futures.items():
            future.cancel()
