class Vault:
    """
    The Vault class provides methods to authenticate and interact with Vault.

    Methods:
        - __init__(role_id, secret_id):
            Initializes the Vault class instance.

            :param role_id: The role ID to authenticate with.
            :param secret_id: The secret ID to authenticate with.

        - get_kv_secret(path, mount_point='secret', version=None):
            Retrieves a key-value secret from Vault.

            :param path: The path of the secret.
            :param mount_point: The mount point for the secret engine. Default is 'secret'.
            :param version: The version of the secret. Default is None.
            :return: The secret value.

        - get_dynamic_credentials(mount_point, database):
            Generates dynamic credentials for a database from Vault.

            :param mount_point: The mount point for the database engine.
            :param database: The name of the database.
            :return: The generated credentials (username and password).
    """
    import time
    import struct
    import hvac
    from azure.identity import ClientSecretCredential
    def __init__(self, role_id, secret_id):
        """
        Initialize the class instance.

        :param role_id: The role ID to authenticate with.
        :param secret_id: The secret ID to authenticate with.
        """
        hvac = self.hvac
        self.Client = hvac.Client(url='https://vault.mycarrier.tech')
        self.SourceCredentials = None
        try:
            self.Client.auth.approle.login(
                role_id=role_id,
                secret_id=secret_id,
            )
        except Exception as error:
            raise error
        self.ServicePrincipalCredentials = None

    def kv_secret(self, path, mount_point='secret', version=None):
        output = None
        if version is None:
            output = self.Client.secrets.kv.v2.read_secret_version(
                path=path, mount_point=mount_point)
        else:
            output = self.Client.secrets.kv.v2.read_secret_version(
                path=path, mount_point=mount_point, version=version)
        return output

    def db_basic(self, mount_point, database):

        credentials = self.Client.secrets.database.generate_credentials(
            name=database,
            mount_point=mount_point
        )
        output = {
            'username': credentials['username'],
            'password': credentials['password']
        }
        return output

    def db_oauth(self, mount_point, role):
        time = self.time
        struct = self.struct
        ClientSecretCredential = self.ClientSecretCredential
        vaultspnCreds = self.Client.secrets.azure.generate_credentials(
            name=role,
            mount_point=mount_point
        )
        i = 0
        while i < 10:
            i += 1
            try:
                spnCreds = ClientSecretCredential(client_id=vaultspnCreds['client_id'],
                                                  client_secret=vaultspnCreds['client_secret'],
                                                  tenant_id="033c43bf-e5b3-42d4-93d2-e7e0fd5e2d3d")
                time.sleep(10)
                token_bytes = spnCreds.get_token(
                    "https://database.windows.net/.default").token.encode("UTF-16-LE")
                token_struct = struct.pack(
                    f'<I{len(token_bytes)}s', len(token_bytes), token_bytes)
                return token_struct
            except Exception as e:
                print(e)
            print('SPN not ready, sleeping 30s')
            time.sleep(30)

    def azure(self, mount_point, role):
        time = self.time
        hvac = self.hvac
        max_retries = 5
        retry_delay = 5
        retry_count = 0
        while retry_count < max_retries:
            try:
                creds = self.Client.secrets.azure.generate_credentials(
                    name=role,
                    mount_point=mount_point
                )
                return creds
            except hvac.exceptions.InternalServerError as e:
                if "deadlocked on lock resources" in str(e):
                    print(
                        f"Deadlock detected when getting SQL dynamic creds, retrying... ({retry_count + 1}/{max_retries})")
                    retry_count += 1
                    time.sleep(retry_delay)
                else:
                    raise
        raise Exception(
            "Max retries reached for generating credentials due to deadlock")


class dbConnection:
    """
    Class for establishing a database connection and executing queries.

    Args:
        server (str): The name or IP address of the server.
        port (int): The port number of the server.
        db_name (str): The name of the database to connect to.
        driver (str, optional): The ODBC driver name. Defaults to 'ODBC Driver 18 for SQL Server'.
        encrypt (str, optional): Specify whether the connection should be encrypted. Defaults to 'yes'.
        trustservercertificate (str, optional): Specify whether to trust the server certificate. Defaults to 'no'.
        timeout (int, optional): The connection timeout in seconds. Defaults to 30.

    Attributes:
        connection: The pyodbc connection object representing the database connection.

    Methods:
        query: Executes a SQL query and returns the results.
        close: Closes the database connection.

    Examples:
        # Instantiate dbConnection
        conn = dbConnection('localhost', 1433, 'mydb')

        # Execute a query and get all results
        results = conn.query('SELECT * FROM mytable', outputResults='all')

        # Close the connection
        conn.close()
    """
    import snowflake
    import pyodbc
    def __init__(self, connection):
        self.connection = connection

    @property
    def cursor(self):
        return self.connection.cursor

    @classmethod
    def from_sql(cls, server, port, db_name, driver='ODBC Driver 18 for SQL Server', encrypt='yes',
                 trustservercertificate='no', timeout=30, auth_method='token', token=None, username=None,
                 password=None):
        pyodbc = cls.pyodbc

        if username is not None and token is not None:
            print(
                "Token and basic auth are mutually exclusive, please use either username & password or Token")

        if auth_method == 'token':
            if token is None:
                print("Token is required when using Token authentication")
                exit(1)
            SQL_COPT_SS_ACCESS_TOKEN = 1256
            con_string = (f"Driver={{{driver}}}; Server={server},{port}; Database={db_name}; Encrypt={encrypt}; "
                          f"TrustServerCertificate={trustservercertificate}; Connection Timeout={timeout},")

            return cls(pyodbc.connect(con_string, attrs_before={SQL_COPT_SS_ACCESS_TOKEN: token}))

        if auth_method == 'basic':
            if username is None or password is None:
                print("When auth method is basic, username and password are required")
                exit(1)
            conn_string = (f"Driver={{{driver}}}; Server={server},{port}; Database={db_name}; Encrypt={encrypt}; "
                           f"TrustServerCertificate={trustservercertificate}; Connection Timeout={timeout};"
                           f"UID={username};PWD={password}")

            return cls(pyodbc.connect(conn_string))

    @classmethod
    def from_snowflake(cls, user, password, role, account, warehouse, database=None, schema=None):
        snowflake = cls.snowflake
        conn = snowflake.connector.connect(
            user=user,
            password=password,
            role=role,
            account=account,
            warehouse=warehouse,
            database=database,
            schema=schema
        )
        return cls(conn)

    def query(self, sql, outputResults: str = None, commit: bool = False, params: tuple = ()):
        cursor = self.cursor()
        try:
            if commit:
                self.connection.autocommit = True
            cursor.execute(sql, params)
            if outputResults == "one":
                return cursor.fetchone()
            if outputResults == "all":
                return cursor.fetchall()
        finally:
            cursor.close()
            self.connection.autocommit = False

    def close(self):
        self.connection.close()

class githubAuth:
    """
    Class for authenticating and retrieving auth token from GitHub.

    Args:
        private_key_pem (str): Private Key PEM for GitHub authentication
        app_id (str): GitHub App id
        installation_id (str): GitHub App installation id

    Methods:
        get_auth_token: Get auth token from GitHub for the GitHub App

    Examples:
        # Get auth token from GitHub
        github_auth = githubAuth(private_key_pem, app_id, installation_id)
        
        # The returned token could be used with PyGithub API: https://github.com/PyGithub/PyGithub/tree/main/doc/examples
        g = Github(login_or_token=github_auth.token)
        org = g.get_organization("ORGNAME")
        repo = org.get_repo("REPONAME")
        
    """
    from jwt import JWT, jwk_from_pem
    import time
    import requests
    import json
    def __init__ (self, private_key_pem: str, app_id: str, installation_id: str):
        jwk_from_pem = self.jwk_from_pem
        JWT = self.JWT
        time = self.time
        self.installation_id = installation_id
        self.signing_key = jwk_from_pem(str.encode(private_key_pem))

        self.payload = {
            # Issued at time
            'iat': int(time.time()),
            # JWT expiration time (10 minutes maximum)
            'exp': int(time.time()) + 600,
            # GitHub App's identifier
            'iss': app_id
        }

        self.jwt_instance = JWT()
        self.token = self.get_auth_token()

    def get_auth_token(self):
        requests = self.requests
        json = self.json
        try:
            encoded_jwt = self.jwt_instance.encode(self.payload, self.signing_key, alg='RS256')
            # Set Headers
            headers = {"Authorization": "Bearer {}".format(encoded_jwt),
                    "Accept": "application/vnd.github+json",
                    "X-GitHub-Api-Version": "2022-11-28" }
            # Get Access Token
            resp = requests.post('https://api.github.com/app/installations/{}/access_tokens'.format(self.installation_id), headers=headers)
            token = json.loads(resp.content.decode())['token']
            return token
        except Exception as error:
            raise error
