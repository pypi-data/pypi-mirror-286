import time
from datetime import timedelta

import easymaker
from easymaker.common import constants, exceptions
from easymaker.common.utils import status_code_utils


class Experiment:
    def __init__(self):
        self.easymaker_api_sender = easymaker.easymaker_config.api_sender

    def _get(self, experiment_name: str) -> dict:
        if not experiment_name:
            raise ValueError("[AI EasyMaker] experiment_name is required.")

        experiments = self._list(experiment_name_list=[experiment_name])

        if not experiments:
            raise ValueError(f"[AI EasyMaker] No experiment is found with name {experiment_name}.")

        if len(experiments) > 1:
            raise ValueError(f"[AI EasyMaker] Multiple experiments is found with name {experiment_name}.")

        return experiments[0]

    def _list(self, experiment_name_list: list[str]) -> list[dict]:
        return self.easymaker_api_sender.get_experiment_list(experiment_name_list=experiment_name_list)

    def create(self, experiment_name, experiment_description=None, wait=True):
        """
        Args:
            experiment_name (str): Experiment name
            experiment_description (str): Experiment description
            wait (bool): wait for the job to complete
        Returns:
            experiment_id
        """
        if not experiment_name:
            raise ValueError("[AI EasyMaker] experiment_name is required.")

        try:
            experiment = self._get(experiment_name=experiment_name)
            experiment_id = experiment["id"]
            print(f"[AI EasyMaker] Experiment '{experiment_name}' already exists. Experiment Id : {experiment_id}")
            return experiment_id
        except ValueError:
            pass

        print(f"[AI EasyMaker] Creating experiment {experiment_name}.")
        response = self.easymaker_api_sender.create_experiment(experiment_name=experiment_name, experiment_description=experiment_description)
        experiment_id = response["experiment"]["experimentId"]
        if wait:
            waiting_time_seconds = 0
            experiment_status = status_code_utils.replace_status_code(response["experiment"]["experimentStatusCode"])
            while experiment_status != "ACTIVE":
                print(f"[AI EasyMaker] Experiment create status : {experiment_status} ({timedelta(seconds=waiting_time_seconds)}) Please wait...")
                time.sleep(constants.EASYMAKER_API_WAIT_INTERVAL_SECONDS)
                waiting_time_seconds += constants.EASYMAKER_API_WAIT_INTERVAL_SECONDS
                experiment = self.easymaker_api_sender.get_experiment_by_id(experiment_id)
                experiment_status = status_code_utils.replace_status_code(experiment["experiment"]["experimentStatusCode"])
                if "FAIL" in experiment_status:
                    experiment["experiment"]["experimentStatusCode"] = experiment_status
                    raise exceptions.EasyMakerError(experiment)
            print(f"[AI EasyMaker] Experiment create complete. Experiment Id : {experiment_id}")
        else:
            print(f"[AI EasyMaker] Experiment create request complete. Experiment Id : {experiment_id}")

        return experiment_id

    def delete(self, experiment_id):
        response = self.easymaker_api_sender.delete_experiment_by_id(experiment_id=experiment_id)
        print(f"[AI EasyMaker] Experiment delete request complete. Experiment Id : {experiment_id}")
        return response
