import requests


class HttpAgent:

    def __init__(self, api_key, base_url):
        self.api_key = api_key
        self.base_url = base_url

    def get_headers(self, extra=None):
        if extra is None:
            extra = {}
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Accept-Encoding": "identity",
            "Api-Key": self.api_key,
            **extra
        }

    def make_get_request(self, path, query_params=None, headers=None):
        headers = self.get_headers(headers)
        try:
            response = requests.get(self.make_absolute_url(path, query_params), headers=headers)
            return self.process_response(response, None)
        except Exception as error:
            return self.process_response(None, error)

    def make_post_request(self, path, data, headers=None):
        headers = self.get_headers(headers)
        try:
            response = requests.post(self.make_absolute_url(path), json=data, headers=headers)
            return self.process_response(response, None)
        except Exception as error:
            return self.process_response(None, error)

    def process_response(self, response, error):
        if error:
            return {"error": str(error)}

        return {"data": response.json()}

    def make_absolute_url(self, path, query_params=None):
        if path.startswith("http"):
            url = path
        else:
            url = f"{self.base_url}/{path}"

        query = []

        if query_params:
            for key, value in query_params.items():
                query.append(f"{key}={value}")

        if query:
            url += "?" + "&".join(query)

        return requests.utils.quote(url)
