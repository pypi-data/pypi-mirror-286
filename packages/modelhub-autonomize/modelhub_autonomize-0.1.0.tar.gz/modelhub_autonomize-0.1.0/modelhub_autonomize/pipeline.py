import yaml
import os
import base64

from modelhub.client import ModelHubClient

class Pipeline:
    def __init__(self, client: ModelHubClient, config_path: str):
        self.client = client
        self.config_path = config_path
        self.load_config()

    def load_config(self):
        with open(self.config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        self.pipeline_config = self.config.get('pipeline', {})
        self.name = self.pipeline_config.get('name', 'custom_pipeline')
        self.description = self.pipeline_config.get('description', '')
        self.experiment_id = self.pipeline_config.get('experiment_id', '')
        self.dataset_id = self.pipeline_config.get('dataset_id', '')
        self.image_tag = self.pipeline_config.get('image_tag', '')
        self.stages = self.config.get('stages', [])

    def create_stage(self, stage):
        with open(stage['script'], 'r') as f:
            script = f.read()
        with open(stage['requirements'], 'r') as f:
            requirements = f.read()

        return {
            "name": stage['name'],
            "type": "python",
            "params": {},
            "depends_on": stage.get('depends_on', []),
            "script": base64.b64encode(script.encode()).decode(),
            "requirements": base64.b64encode(requirements.encode()).decode(),
            "resources": stage.get('resources', {})
        }

    def create_pipeline(self):
        stages = [self.create_stage(stage) for stage in self.stages]
        return self.client.create_pipeline(
            name=self.name,
            description=self.description,
            experiment_id=self.experiment_id,
            dataset_id=self.dataset_id,
            stages=stages,
            image_tag=self.image_tag
        )

    def submit(self, pipeline_id):
        return self.client.submit_pipeline(pipeline_id)

    def get(self, pipeline_id):
        return self.client.get_pipeline(pipeline_id)

    def list(self, page_number=1, page_size=10):
        return self.client.list_pipelines(page_number, page_size)

    def delete(self, pipeline_id):
        return self.client.delete_pipeline(pipeline_id)

    def get_logs(self, namespace, pod_name, container=None):
        return self.client.get_pod_logs(namespace, pod_name, container)