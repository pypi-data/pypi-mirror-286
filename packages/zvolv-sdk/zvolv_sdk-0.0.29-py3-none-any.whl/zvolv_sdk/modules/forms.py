from ..models.form import Form
import requests

class Forms:
    def __init__(self, session, logger, base_url):
        self.session = session
        self.logger = logger
        self.base_url = base_url
        self.workspace_instance = None
    
    def get(self, id):
        """
        Get form details from id

        :param id:
        :return:
        """
        try:
            url = f"{self.base_url}/api/v1/forms/{id}"
            response = self.session.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors

            resp = response.json()
            if resp.get('error') == False:
                self.logger.info(f"Successfully fetched form for {id}")
            else:
                raise ValueError(resp.get('message'))
            return Form(**resp['data']['elements'][0])
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

    def put(self, form: Form, enableRetrofit: bool = False, enableReSync: bool = False):
        """
        Update existing form

        :param form:
        :param enableRetrofit:
        :param enableReSync:
        :return:
        """
        # form should be a valid Form model
        if not isinstance(form, Form):
            raise ValueError("form field should be an instance of Form model")
        # id or uuid field is required in the form model to update the form
        if not form.id and not form.uuid:
            raise ValueError("id or uuid field is required to update the form")

        try:
            url = f"{self.base_url}/api/v1/forms?enableRetrofit={enableRetrofit}&enableReSync={enableReSync}"
            response = self.session.put(url, json=form.model_dump(exclude_none=True, exclude_unset=True))
            response.raise_for_status()  # Raise an exception for HTTP errors

            resp = response.json()
            if resp.get('error') == False:
                self.logger.info(f"Successfully updated task for id {form.id}")
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
    
    def post(self, form: Form):
        """
        Create a new form

        :param form:
        :return:
        """
        if not isinstance(form, Form):
            raise ValueError("form field should be an instance of Form model")

        try:
            url = f"{self.base_url}/api/v1/forms"
            response = self.session.post(url, json=form.model_dump(exclude_none=True, exclude_unset=True))
            response.raise_for_status()  # Raise an exception for HTTP errors

            resp = response.json()
            if resp.get('error') == False:
                self.logger.info(f"Successfully completed search operation for form {form.title}")
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