from ebaysuds import EbaySuds, ebaysuds_config


class EbaySudsNoAuth(EbaySuds):
    """
    Horrible hack to use ebay without a token

    Will fork and submit pull request to repo https://github.com/anentropic/ebaysuds
    at a later date
    """
    def __init__(self, **kwargs):
        super(EbaySudsNoAuth, self).__init__(**kwargs)
        if kwargs.get('token') is None:
            if kwargs.get('sandbox'):
                key_section = 'sandbox_keys'
            else:
                key_section = 'production_keys'

            credentials = self.sudsclient.factory.create('RequesterCredentials')
            credentials.Credentials.AppId = self.app_id
            credentials.Credentials.DevId = kwargs.get('dev_id') or ebaysuds_config.get('keys', 'dev_id')
            credentials.Credentials.AuthCert = kwargs.get('cert_id') or ebaysuds_config.get(key_section, 'cert_id')
            self.sudsclient.set_options(soapheaders=credentials)
