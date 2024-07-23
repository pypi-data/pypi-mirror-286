# Alchimie Data Solutions : Generic functions

The purpose of this Python package is to group together all the generic functions used in Onyx development.

## adsGenericFunctions

### class PostgresInput:
#### def __init__(self, database: str, user: str, password:str, port:str, host: str, batch_size=1000)

This class is used to communicate with a postgres database. Initialising the class starts the connection, so it needs the database name, user, password, port and host. It also sets the default read buffer to 1000.

#### def __del__(self)

This method just closes the connection to the database.

#### def read(self, query: str)

This method belongs to the PostgresInput class. It reads the parameter query and yield the results in batches of size `batch_size`.

#### def write(self, query: str, params=None)

This method belong to the PostgresInput class. It executes the parameter query, this query can be an insert, an update or a delete operation. We can add parameters to the execution by the parameter `params` set to None by default.

#### def send_mail(sgApiClient: str, destinataire: List[str], msg: str, from_email: str, subject: str) -> Response

This function sends an email to the `destinataire` from `from_email` with the subject `subject` and a message `msg`. It also needs the api key `sgApiClient`.
It returns the send response.
