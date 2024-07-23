from python_http_client.client import Response
from sendgrid import SendGridAPIClient, Mail
import psycopg2
import logging

logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('adsGenericFunctions')


class PostgresInput:
    def __init__(self, database: str, user: str, password: str, port: str, host: str, batch_size=1000):
        try:
            self.__connection = psycopg2.connect(
                database=database,
                user=user,
                password=password,
                port=port,
                host=host
            )
            self.__cursor = self.__connection.cursor()
            self.__batch_size = batch_size
            logger.info(f"Connexion établie avec la base de données {database} sur {host}:{port} en tant que {user}")
        except Exception as e:
            logger.error(f"Échec de la connexion à la base de données {database}: {e}")
            raise

    def __del__(self):
        try:
            self.__connection.close()
            logger.info("Connexion à la base de données fermée.")
        except Exception as e:
            logger.error(f"Échec de la fermeture de la connexion: {e}")

    def read(self, query: str):
        logger.debug(f"Exécution de la requête de lecture: {query}")
        try:
            with self.__connection.cursor() as cursor:
                cursor.execute(query)
                logger.info("Requête exécutée avec succès, début de la lecture des résultats.")
                while True:
                    rows = cursor.fetchmany(self.__batch_size)
                    if not rows:
                        break
                    yield from rows
                    logger.info(f"{len(rows)} lignes lues.")
        except Exception as e:
            logger.error(f"Échec de la lecture des données: {e}")

    def write(self, query: str, params=None):
        try:
            if params:
                logger.debug(f"Exécution de la requête d'écriture: {query} avec paramètres: {params}")
                self.__cursor.execute(query, params)
            else:
                logger.debug(f"Exécution de la requête d'écriture: {query}")
                self.__cursor.execute(query)
            self.__connection.commit()
            logger.info("Données écrites et transaction commise avec succès.")
        except Exception as e:
            self.__connection.rollback()
            logger.error(f"Échec de l'écriture des données, transaction annulée: {e}")
            raise


def send_mail(sgApiClient: str, destinataire: str, msg: str, from_email: str, subject: str, ) -> Response:
    logger.debug(f"Envoi d'un email de {from_email} à {destinataire} avec le sujet '{subject}'.")
    try:
        sg = SendGridAPIClient(sgApiClient)
        mail = Mail(
            from_email=from_email,
            to_emails=destinataire,
            subject=subject,
            html_content=msg
        )
        response = sg.send(mail)
        logger.info(f"Email envoyé avec succès à {destinataire}. Statut de la réponse: {response.status_code}.")
        return response
    except Exception as e:
        logger.error(f"Échec de l'envoi de l'email à {destinataire}: {e}")
