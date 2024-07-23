import requests

class Analytics:
    def __init__(self, session, logger, base_url):
        self.session = session
        self.logger = logger
        self.base_url = base_url
    
    def search(self, form_id, query):
        """
        Fetch workspace details from domain.

        :param form_id:
        :param query:
        :return:
        """
        try:
            url = f"{self.base_url}/api/v1/analytics/search"
            response = self.session.post(url, json={'formId': form_id, 'query': query})
            response.raise_for_status()  # Raise an exception for HTTP errors

            resp = response.json()
            if resp.get('error') == False:
                self.logger.info(f"Successfully completed search operation for form {id}")
            else:
                raise ValueError(resp.get('message'))
            return resp['data']
        except requests.exceptions.RequestException as http_err:
            error_response = response.json()
            status_code = error_response.get('statusCode', response.status_code)
            error_message = error_response.get('message', str(http_err))

            error_message = f"{status_code} Error: {error_message}"
            self.logger.error(f"An error occurred: {error_message}")
            raise requests.exceptions.HTTPError(error_message)
        except Exception as e:
            self.logger.error(e)
            raise e