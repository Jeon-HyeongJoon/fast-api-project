from fastapi import Request
from user_agents import parse


class RequestService:
    def __init__(self, request: Request):
        self._request = request

    @property
    def request(self):
        return self._request

    @property
    def base_url(self):
        return self.request.base_url

    @property
    def ip_address(self):
        forwarded = self.request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0]
        return self.request.client.host

    @property
    def languages(self):
        accept_lang = self.request.headers.get("Accept-Language")
        if accept_lang and "," in accept_lang:
            return [v.split(";")[0].split("-")[0] for v in accept_lang.split(",")]
        else:
            return [accept_lang]

    @property
    def user_agent(self):
        return parse(self.request.headers.get("User-Agent", ""))

    @property
    def browser(self):
        return self.user_agent.get_browser()

    @property
    def device(self):
        return self.user_agent.get_device()

    @property
    def os(self):
        return self.user_agent.get_os()
