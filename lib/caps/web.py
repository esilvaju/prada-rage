from typing import TypeVar
# TODO: replace with Python requests and Python streams
#from streaming import PassThrough
#from next import NextApiResponse

class WebResponse:
    pass

"""
 A type that represents a response object that can be used in a Next.js API route.
 @remarks
 This type can be either a `NextApiResponse` object or a `PassThrough` stream.
"""
TWebResponse = TypeVar('TWebResponse', bound=WebResponse)
