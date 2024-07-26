import requests


class BaseApi:
    def get_headers(self):
        raise NotImplementedError

    def _get(self, end_point):
        r = requests.get(self.get_url(end_point), headers=self.get_headers())

        self.__raise_for_status(r)

        return r.json()

    def _post(self, end_point, json: dict):
        r = requests.post(
            self.get_url(end_point), headers=self.get_headers(), json=json
        )

        self.__raise_for_status(r)

        return r

    def _put(self, end_point, json: dict):
        r = requests.put(self.get_url(end_point), headers=self.get_headers(), json=json)

        self.__raise_for_status(r)

        return r

    def __raise_for_status(self, r):
        try:
            r.raise_for_status()
        except:
            try:
                message = r.json()

                print("=" * 78)
                print("Raw Response:\n")
                print(message)
                print("\n" + "=" * 78)
            except requests.exceptions.JSONDecodeError:
                pass

            raise
