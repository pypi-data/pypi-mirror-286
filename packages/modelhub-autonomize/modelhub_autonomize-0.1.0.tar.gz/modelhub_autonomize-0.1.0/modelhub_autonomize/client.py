import requests
import base64

class ModelHubClient:
    def __init__(self, base_url, api_key=None):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {self.api_key}"
        } if api_key else {}

    def create_pipeline(self, name, description, experiment_id, dataset_id, stages, image_tag):
        url = f"{self.base_url}/pipelines/"
        payload = {
            "name": name,
            "description": description,
            "experiment_id": experiment_id,
            "dataset_id": dataset_id,
            "image_tag": image_tag,
            "stages": [
                {
                    "name": stage["name"],
                    "type": stage["type"],
                    "params": stage["params"],
                    "depends_on": stage["depends_on"],
                    "script": base64.b64encode(stage["script"].encode()).decode(),
                    "requirements": base64.b64encode(stage["requirements"].encode()).decode()
                } for stage in stages
            ]
        }
        response = requests.post(url, json=payload, headers=self.headers)
        return response.json()

    def submit_pipeline(self, pipeline_id):
        url = f"{self.base_url}/pipelines/{pipeline_id}/submit"
        response = requests.post(url, headers=self.headers)
        return response.json()

    def get_pipeline(self, pipeline_id):
        url = f"{self.base_url}/pipelines/{pipeline_id}"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def list_pipelines(self, page_number=1, page_size=10):
        url = f"{self.base_url}/pipelines/"
        params = {"page_number": page_number, "page_size": page_size}
        response = requests.get(url, headers=self.headers, params=params)
        return response.json()

    def delete_pipeline(self, pipeline_id):
        url = f"{self.base_url}/pipelines/{pipeline_id}"
        response = requests.delete(url, headers=self.headers)
        return response.json()

    def get_pod_logs(self, namespace, pod_name, container=None):
        url = f"{self.base_url}/pipelines/logs/{namespace}/{pod_name}"
        params = {"container": container} if container else {}
        response = requests.get(url, headers=self.headers, params=params)
        return response.json()