from osbot_utils.base_classes.Type_Safe import Type_Safe
from osbot_utils.utils.Env import get_env


#PORT_LOCAL__CBR_WEBSITE = get_env('PORT', 3000)                                                            # todo: check side effect of mapping this here (vs later when the load_dotenv has happened)
#URL__LOCAL__CBR_CONFIG  = f'http://localhost:{PORT_LOCAL__CBR_WEBSITE}/site_info/cbr-config-active'        # todo: refactor this to a better solution to get this data exposed to this service

class CBR__Config(Type_Safe):

    def cbr_config(self):
        cbr_config = {}
        return dict(cbr_config = cbr_config,
                    port       = self.port())

    def port(self):
        return get_env('PORT')


# @cache_on_self
    # def cbr_config_active(self):  # this is handling the entire server ( i think is because of the internal call to an internal endpoint)
    #     try:
    #         print(f'in cbr_config_active: {URL__LOCAL__CBR_CONFIG}')
    #         cbr_config = GET_json(URL__LOCAL__CBR_CONFIG)
    #         pprint(cbr_config)
    #         return cbr_config
    #     except:
    #         return {}
    #         # response = requests.get(URL__LOCAL__CBR_CONFIG)  # this was hanging the entire server
    #         # if response.status_code == 200:
    #         #     return response.json()
    #         # return {}