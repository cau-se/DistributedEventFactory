from abc import abstractmethod


class PayloadUpdateProvider:

    @abstractmethod
    def get_payload_delta(self):
        pass
