from alas_ce0.common.client_base import EntityClientBase


class DataJobClient(EntityClientBase):
    entity_endpoint_base_url = '/task/'

    def get_content(self, id):
        return self.http_get(
            self.entity_endpoint_base_url + "{0}/data-jobs/_content".format(id)
        )

    def custom_deferred(self, params):
        return self.http_post_json(self.entity_endpoint_base_url + "custom/path", params)
    def task_handler(self, params):
        return self.http_post_json(self.entity_endpoint_base_url + "task_handler", params)