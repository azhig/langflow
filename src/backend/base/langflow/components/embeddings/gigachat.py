from langchain_gigachat import GigaChatEmbeddings

from langflow.base.embeddings.model import LCEmbeddingsModel
from langflow.base.models.gigachat_constants import GIGACHAT_EMBEDDING_MODEL_NAMES, GIGACHAT_MODEL_NAMES, GIGACHAT_SCOPE_NAMES
from langflow.field_typing import Embeddings
from langflow.field_typing.range_spec import RangeSpec
from langflow.io import BoolInput, DropdownInput, IntInput, MessageTextInput, SecretStrInput


class GigaChatEmbeddingsComponent(LCEmbeddingsModel):
    display_name = "GigaChat Embeddings"
    description = "Генерация векторных представлений с использованием GigaChat."
    icon = "GigaChat"
    name = "GigaChatEmbeddings"

    inputs = [

        MessageTextInput(
            name="base_url",
            display_name="Base URL",
            advanced=True,
            info="Базовый API GigaChat"
            "По умолчанию https://gigachat.devices.sberbank.ru/api/v1.",
        ),
        MessageTextInput(
            name="auth_url",
            display_name="Auth URL",
            advanced=True,
            info="Авторизационный API GigaChat"
            "По умолчанию https://gigachat.devices.sberbank.ru/api/v1.",
        ),
        SecretStrInput(
            name="credentials",
            display_name="Credential Key",
            info="Ключ авторизации. Доступен в личном кабинете в разделе Авторизационные данные.",
            advanced=True,
            value=None,
        ),
        DropdownInput(
            name="scope",
            display_name="Scope",
            advanced=True,
            info="Выбор персонального или корпоративного пространства"
            "GIGACHAT_API_PERS — версия API для физических лиц;"
            "GIGACHAT_API_B2B — доступ для ИП и юридических лиц по предоплате;"
            "GIGACHAT_API_CORP — доступ для ИП и юридических лиц по схеме pay-as-you-go.",
            options=GIGACHAT_SCOPE_NAMES,
            value=None,
        ),
        SecretStrInput(
            name="access_token",
            display_name="Access Token",
            info="Авторизация с временным токеном.",
            advanced=True,
            value=None
        ),
        DropdownInput(
            name="model",
            display_name="Model",
            advanced=False,
            options=GIGACHAT_EMBEDDING_MODEL_NAMES,
            value=GIGACHAT_EMBEDDING_MODEL_NAMES[0],
        ),
        MessageTextInput(
            name="user",
            display_name="User",
            advanced=True,
            info="Логин при авторизации через логин и пароль.",
        ),
        SecretStrInput(
            name="password",
            display_name="Password",
            info="Пароль при авторизации через логин и пароль.",
            advanced=True,
            value=None
        ),
        IntInput(
            name="timeout",
            display_name="Timeout",
            advanced=True,
            info="Таймаут реквеста в секундах",
            range_spec=RangeSpec(min=0, max=300),
        ),

        BoolInput(
            name="verify_ssl_certs",
            display_name="Verify SSL certs",
            advanced=True,
            value = False,
            info="Использовать ли клиенскую проверку серверного сертификата",
        ),
        # Support for connection to GigaChat through SSL certificates
        MessageTextInput(
            name="ca_bundle_file",
            display_name="CA bundle file",
            advanced=True,
            info="Путь к файлу CA цепочки сертификатов. Например certs/ca.pem # chain_pem.txt",
        ),
        MessageTextInput(
            name="cert_file",
            display_name="Cert file",
            advanced=True,
            info="Путь к файлу с публичной частью сертификата. Например certs/tls.pem # published_pem.txt",
        ),
        MessageTextInput(
            name="key_file",
            display_name="Key file",
            advanced=True,
            info="Путь к файл с публичной частью сертификата",
        ),
        MessageTextInput(
            name="key_file_password",
            display_name="Key file password",
            advanced=True,
            info="Пароль от файла с публичной частью ключа",
        ),
        MessageTextInput(
            name="prefix_query",
            display_name="Prefix query",
            advanced=True,
            value="Дано предложение, необходимо найти его парафраз \nпредложение: ",
            info="Предзапрос",
        ),
        BoolInput(
            name="use_prefix_query",
            display_name="Use prefix Query",
            advanced=True,
            value = False,
            info="Использовать ли предзапрос",
        )
    ]

    def build_embeddings(self) -> Embeddings:
        return GigaChatEmbeddings(
            base_url=self.base_url or None,
            auth_url=self.auth_url or None,
            credentials= self.credentials or None,
            scope=self.scope or None,
            access_token=self.access_token or None,
            model=self.model or None,
            user=self.user or None,
            password=self.password or None,
            timeout=self.timeout or None,
            verify_ssl_certs=self.verify_ssl_certs,
            ca_bundle_file=self.ca_bundle_file or None,
            cert_file=self.cert_file or None,
            key_file=self.key_file or None,
            key_file_password=self.key_file_password or None,
            prefix_query=self.prefix_query or "Дано предложение, необходимо найти его парафраз \nпредложение: ",
            use_prefix_query=self.use_prefix_query or False,
        )
