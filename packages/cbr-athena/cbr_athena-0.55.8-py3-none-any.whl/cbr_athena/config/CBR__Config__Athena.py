import requests

from cbr_athena.config.CBR__Config                  import CBR__Config
from cbr_athena.utils.Version                       import version__cbr_athena
from osbot_utils.utils.Env                          import get_env
from osbot_utils.base_classes.Type_Safe import Type_Safe




class CBR__Config__Athena(Type_Safe):

    def aws_enabled(self):
        if get_env('AWS_ACCESS_KEY_ID'):
            return True
        return False

    def aws_disabled(self):
        enabled = self.aws_enabled()
        return enabled == False

    def cbr_config_athena(self):
        cbr_config = CBR__Config().cbr_config()
        return dict(cbr_config = cbr_config,
                    version    = version__cbr_athena)

    # def aws_enabled(self):
    #     return self.cbr_website().get('aws_enabled', False)
    #
    # def cbr_config(self):
    #     return self.cbr_config_active().get('cbr_config', {})
    #

    #
    # def aws_disabled(self):
    #     print('in aws_disabled')
    #     return self.aws_enabled() == False
    #
    # def cbr_website(self):
    #     return self.cbr_config().get('cbr_website', {})


cbr_config_athena = CBR__Config__Athena()