from . import codec_pb2_grpc as importStub

class CodecService(object):

    def __init__(self, router):
        self.connector = router.get_connection(CodecService, importStub.CodecStub)

    def decode(self, request, timeout=None, properties=None):
        return self.connector.create_request('decode', request, timeout, properties)

    def encode(self, request, timeout=None, properties=None):
        return self.connector.create_request('encode', request, timeout, properties)