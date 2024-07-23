from django.conf import settings

from afex_logger.http_agent import HttpAgent


class AppLogService:

    def __init__(self):
        from afex_logger.util import LogTypes

        self.path_mappings = {
            LogTypes.activities: "activities",
            LogTypes.errors: "errors",
            LogTypes.process: "process",
            LogTypes.requests: "requests",
        }

        self.https_agent = HttpAgent(
            settings.LOG_SERVER_API_KEY, settings.LOG_SERVER_URL + "/api/v1/logs/"
        )

    def fetch_logs(self, log_type, filter_params):
        return self.https_agent.make_get_request(self.path_mappings[log_type], filter_params)

    def send_logs(self, log_type, payload):
        return self.https_agent.make_post_request(self.path_mappings[log_type], payload)
