import requests
from time import sleep, strftime
import subprocess
import json
from pathlib import Path


class Injector :

    def __init__(self,db_api_url = "http://chaos.db.openshift"):
        self.db_api_url = db_api_url


    def start_experiment(self, dns, fault_name):
        try:
            experiment_id = self._create_object_in_db(dns, fault_name,status = "loading",
                                                      db_api_collection_url = f"{self.db_api_url}/experiments")
            self._create_config_file(dns, experiment_id, fault_name, "/tmp/chaos/tmp")
            self._run_playbook(playbook_path='./ansible_scripts/insert_agent.yaml', dns = dns)

            # Set vars that decide how often to check if experiment is finished
            experiment_finished = False
            pause = 5
            waited_time = 0
            max_waited_time = 600
            # Wait for experiment to finish and then clean the victim.
            while not experiment_finished :
                experiment_finished = self._is_expirement_finished(
                    db_api_experiment_url=f"{self.db_api_url}/experiments/{experiment_id}")
                sleep(pause)
                waited_time = waited_time + pause
                if max_waited_time <= waited_time :
                    break

            self._run_playbook(playbook_path = './ansible_scripts/remove_agent.yaml',dns = dns)
            self._update_object_in_db(db_api_experiment_url= f"{self.db_api_url}/{experiment_id}",
                                      updated_values = {'status' : 'completed'})
        except PermissionError:
            return "failed create config file because of permissions error", 400
        except TypeError:
            return  "failed to contact db because of a bad json format", 400


    @staticmethod
    def _create_object_in_db(dns, fault_name, status, db_api_collection_url):
        experiment_object = {'id' : f"{dns}-{fault_name}-{Injector._get_current_time()}",
                             'start_time' : Injector._get_current_time(),
                             'victim' : dns, "fault_name" : fault_name,
                             'status' : status
                             }
        result_object = requests.post(db_api_collection_url, json=experiment_object).json()
        experiment_id = result_object['id']
        return experiment_id

    @staticmethod
    def _get_current_time():
        current_time = strftime('%Y%m%d%H%M%S')
        return current_time

    @staticmethod
    def _create_config_file(dns, experiment_id, fault_name,tmp_dir_path):
        # Make sure path exists if not, create it
        Path(tmp_dir_path).mkdir(parents=True, exist_ok=True)
        conf_file = f"{tmp_dir_path}/fault.conf"
        data = {'dns' : dns , 'experiment_id' : experiment_id,
                'fault_name' : fault_name}
        with open(conf_file, 'w') as outfile:
            json.dump(data, outfile)

    def _run_playbook(self, dns, playbook_path):
        os_type = self._get_os_type(dns)
        subprocess.run(["ansible-playbook", f"{playbook_path}", f'-e "host={dns} os_type={os_type}"'])

    def _get_os_type(self,dns):
        os_type = "linux"
        return os_type

    @staticmethod
    def _update_object_in_db(db_api_experiment_url, updated_values = {'status' : 'completed'}):
        result_object = requests.put(db_api_experiment_url, json = updated_values)
        if result_object.status_code == 200 :
            return True
        else:
            return False

    @staticmethod
    def _is_expirement_finished(db_api_experiment_url):
        experiment_obj = requests.get(db_api_experiment_url).json()
        if experiment_obj['status'] == 'finished_injection':
            return True
        else:
            return False