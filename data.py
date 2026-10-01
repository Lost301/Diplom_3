"""URL-ы приложения Stellar Burgers и его API."""


class Urls:
    BASE_URL = "https://stellarburgers.education-services.ru"
    API_URL = BASE_URL + "/api"

    MAIN_PAGE = BASE_URL + "/"
    FEED_PAGE = BASE_URL + "/feed"

    REGISTER_USER = API_URL + "/auth/register"
    DELETE_USER = API_URL + "/auth/user"
