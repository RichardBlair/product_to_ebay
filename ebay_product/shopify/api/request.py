import hashlib


class ShopifyRequest(object):
    """
    Class interface to validate whether a signature from shopify is valid.
    """

    def __init__(self, shared_secret):
        self.shared_secret = shared_secret

    def is_valid(self, shop, code, timestamp, signature):
        """
        Given the shop, code, and timestamp validate that the provided
        signature is valid.

        Params:
            shop: The my shopify domain for the shop
            code: The code sent by shopify
            timestamp: The timestamp sent by shopify
            signature: The signature sent by shopify

        Returns:
            true if the signature is valid, false otherwise
        """
        #Take the params and put them in a dictionary in alphabetical order
        sig_params = {
                    'timestamp': timestamp,
                    'shop': shop,
                    'code': code
                }

        #Iterate over the key value pairs, joining them together
        sig_params = ['%s=%s' % (key, val) for key, val in sig_params.iteritems() if val]
        sig_params.sort()
        sig_params = ''.join(sig_params)

        #Add the secret to the beginning of the signature
        sig_plain = '%s%s' % (self.shared_secret, sig_params)

        #Create the digest and compare it to the signature parameter
        sig_hash = hashlib.new('md5')
        sig_hash.update(sig_plain)
        return str(sig_hash.hexdigest()) == str(signature)
