import requests

APIKEY = ''
APIKEY_PASSWORD = ''

def to_csv(lista):
    string = ''
    for i in lista:
        string += i + ','
    return string[:-1]

def return_array(value):
    if isinstance(value, str):
        return [value]
    elif isinstance(value, (tuple, list)):
        return value
    raise SyntaxError("One of your params was supposed to be an array or tuple or string but wasn´t wny of it")

def makevariable(kwargs, name, type):
    if type != int:
        str_return = f"{name} property is needed as a {type}"
    else:
        str_return = f"{name} property is needed as an {type}"
    if not name in kwargs:
        raise AttributeError(str_return)
    if not isinstance(name, type):
        raise AttributeError(str_return)
    return kwargs[name]


class Client:

    def __init__(self, apikey=APIKEY, password=APIKEY_PASSWORD):
        if not apikey:
            raise ValueError("Apikey must be passed through")
        self.password = password

        self.apikey = apikey
        self.base_url = 'https://indertct.me/api/'

        response = self.GETrequests('validateApi', {})

        if response["code"] == "0":
            self.name = response["data"]
        elif response["code"] == "1":
            raise NameError("Invalid Apikey")
        elif response["code"] == "2":
            raise InterruptedError(f"Internal server error: {response["msg"]}")

    def get_pass(self, kwargs):
        if not "password" in kwargs:
            if not self.password:
                raise AttributeError(
                    "Must either provide the password param in the method or initialise it together with the object"
                )
            else:
                return self.password
        else:
            return kwargs["password"]
    def GETrequests(self, endpoint: str, params: dict):

        params["apikey"] = self.apikey

        string = self.base_url + endpoint + '?'
        for index, value in params.items():
            string += index + '=' + value + "&"

        return requests.get(string[:-1]).json()

    def POSTrequests(self, endpoint: str, params: dict):

        params["apikey"] = self.apikey

        return requests.post(self.base_url+endpoint, json=params).json()

    def pred_on_crypt(self, crs):
        if isinstance(crs, str):
            crs = [crs]

        if not isinstance(crs, (list, tuple)):
            raise SyntaxError("Cryptos variable must be a string containnng one crypto or a tuple or an array containing cryptos")

        return self.GETrequests("getPredCrypt", {"crs": to_csv(crs)})

    def pred_on_hour_and_crypt(self, **kwargs):

        crs = [] if not "cryptos" in kwargs else kwargs["cryptos"]
        time = [] if not "times" in kwargs else kwargs["times"]

        if not isinstance(crs, (list, tuple)) or not isinstance(time, (list, tuple)):
            raise SyntaxError("cryptos and times params must be either not existent or lists or tuples")

        crs, time = return_array(crs), return_array(time)

        return self.GETrequests("getPredCrHour", {"time": to_csv(time), "crs": to_csv(crs)})

    def pred_on_model_name(self, models):
        models = return_array(models)

        return self.GETrequests("postPredNames", {"models": to_csv(models)})

    def pred_all_models(self):

        return self.GETrequests("modelNames", {})

    def start_trading(self, **kwargs):

        password = self.get_pass(kwargs)

        if not "ndays" in kwargs:
            raise AttributeError("Must provide the number of days the user wants to be running the trading for, as an integer in the ndays variable")

        if not "test" in kwargs:
            raise AttributeError("Must provide data relating to if this is a test or not, as a boolean value in the test variable")

        return self.POSTrequests("StartTrading", {"password": password, "ndays": kwargs["ndays"], "test": kwargs["test"]})

    def stop_trading(self,  **kwargs):

        password = self.get_pass(kwargs)

        return self.POSTrequests("StopTrading", {"password": password})

    def get_tickers_binance(self):

        return self.GETrequests("getTickersApi", {})

    def manual_trading(self, **kwargs):

        password = self.get_pass(kwargs)

        symbol = makevariable(kwargs, "symbol", str)
        quantity = makevariable(kwargs, "quantity", (int, float))
        buy = makevariable(kwargs, "buy", bool)

        return self.POSTrequests("manualTrade", {"password": password, "symbol": symbol, "quantity": quantity, "buy": buy})

    def historical_data(self, **kwargs):

        times = makevariable(kwargs, "times", dict)

        if not "limit" in kwargs:
            limit = 1e40
        else:
            limit = kwargs["limit"]

        cryptos = return_array(makevariable(kwargs, "crs", (list, tuple, str)))

        if not "custom data" in kwargs:

             return self.POSTrequests("historicalCr", {"times": times, "limit": limit, "crs": cryptos})

        else:

            custom_data = makevariable(kwargs, "custom data", dict)

            return self.POSTrequests("historicalCr", {"times": times, "limit": limit, "crs": cryptos, "custom data": custom_data})

    def handle_privs(self, **kwargs):

        models = makevariable(kwargs, "models", (list, tuple, str))
        method = makevariable(kwargs, "method", str)
        password = self.get_pass(kwargs)

        return self.POSTrequests("handlePrivs", {"password": password, "method": method, "models": models})

    def handle_fav_pubs(self, **kwargs):

        models = makevariable(kwargs, "models", (list, tuple, str))
        method = makevariable(kwargs, "method", str)
        password = self.get_pass(kwargs)

        return self.POSTrequests("handleFavPubs", {"password": password, "method": method, "models": models})

    def handle_trading_variables(self, **kwargs):

        password = self.get_pass(kwargs)

        data = makevariable(kwargs, "data", list)

        return self.POSTrequests("handleTradingVariables", {"password": password, "data": data})
