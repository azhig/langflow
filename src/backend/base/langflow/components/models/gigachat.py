import operator
from functools import reduce

from langchain_gigachat import GigaChat
from pydantic.v1 import SecretStr

from langflow.base.models.model import LCModelComponent
from langflow.base.models.gigachat_constants import GIGACHAT_MODEL_NAMES, GIGACHAT_SCOPE_NAMES
from langflow.field_typing import LanguageModel
from langflow.field_typing.range_spec import RangeSpec
from langflow.inputs import BoolInput, DictInput, DropdownInput, IntInput, SecretStrInput, SliderInput, StrInput
from langflow.inputs.inputs import FloatInput, HandleInput


class GigaChatModelComponent(LCModelComponent):
    display_name = "GigaChat"
    description = "Генерация текста с использованием GigaChat."
    icon = "GigaChat"
    name = "GigaChatModel"

    inputs = [
        *LCModelComponent._base_inputs,
        SecretStrInput(
            name="credentials",
            display_name="Credential Key",
            info="Ключ авторизации. Доступен в личном кабинете в разделе Авторизационные данные.",
            advanced=True,
            value=None
        ),
        SecretStrInput(
            name="access_token",
            display_name="Access Token",
            info="Авторизация с временным токеном.",
            advanced=True,
            value=None
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
        IntInput(
            name="max_tokens",
            display_name="Max tokens",
            advanced=True,
            info="Максимальное количество токенов для генерации. Установите значение 0 для неограниченного количества токенов.",
            range_spec=RangeSpec(min=0, max=200000),
        ),
        DropdownInput(
            name="model",
            display_name="Model",
            advanced=False,
            options=GIGACHAT_MODEL_NAMES,
            value=GIGACHAT_MODEL_NAMES[0],
        ),
        StrInput(
            name="base_url",
            display_name="Base URL",
            advanced=True,
            info="Базовый API GigaChat"
            "По умолчанию https://gigachat.devices.sberbank.ru/api/v1.",
        ),
        StrInput(
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
        # Support for connection to GigaChat through SSL certificates
        StrInput(
            name="ca_bundle_file",
            display_name="CA bundle file",
            advanced=True,
            info="Путь к файлу CA цепочки сертификатов. Например certs/ca.pem # chain_pem.txt",
        ),
        StrInput(
            name="cert_file",
            display_name="Cert file",
            advanced=True,
            info="Путь к файлу с публичной частью сертификата. Например certs/tls.pem # published_pem.txt",
        ),
        StrInput(
            name="key_file",
            display_name="Key file",
            advanced=True,
            info="Путь к файл с публичной частью сертификата",
        ),
        StrInput(
            name="key_file_password",
            display_name="Key file password",
            advanced=True,
            info="Пароль от файла с публичной частью ключа",
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
        BoolInput(
            name="profanity_check",
            display_name="Profanity check",
            advanced=True,
            info="Проверка на использование нецензурной лексики. ",
        ),
        SliderInput(
            name="temperature", 
            display_name="Temperature", 
            value=0.1, 
            range_spec=RangeSpec(min=0, max=1)
            ),
        FloatInput(
            name="some_other_param", 
            display_name="Top p", 
            # info="top_p value to use for nucleus sampling. Must be between 0.0 and 1.0 ",
            range_spec=RangeSpec(min=0, max=1),
            advanced=True,
            value=1.0,
            ),
        BoolInput(
            name="json_mode",
            display_name="JSON Mode",
            advanced=True,
            info="If True, it will output JSON regardless of passing a schema.",
        ),
        DictInput(
            name="output_schema",
            is_list=True,
            display_name="Schema",
            advanced=True,
            info="The schema for the Output of the model. "
            "You must pass the word JSON in the prompt. "
            "If left blank, JSON mode will be disabled. [DEPRECATED]",
        ),
        BoolInput(
            name="streaming",
            display_name="streaming",
            advanced=True,
            info="Whether to stream the results or not. ",
            value=False
        ),
        # TODO - add later
        # use_api_for_tokens: bool = False
        # """ Use GigaChat API for tokens count """
        # verbose: bool = False
        # """ Verbose logging """
        # flags: Optional[List[str]] = None
        # """ Feature flags """
        # repetition_penalty: Optional[float] = None
        # """ The penalty applied to repeated tokens """
        # update_interval: Optional[float] = None
        # """ Minimum interval in seconds that elapses between sending tokens """
        # function
        # tools
        # function_call
    ]

    def build_model(self) -> LanguageModel:  # type: ignore[type-var]
        # self.output_schema is a list of dictionaries
        # let's convert it to a dictionary
        output_schema_dict: dict[str, str] = reduce(operator.ior, self.output_schema or {}, {})
        credentials= self.credentials or None
        access_token= self.access_token or None
        scope= self.scope or None
        max_tokens= self.max_tokens or None
        model= self.model
        base_url= self.base_url or "https://gigachat.devices.sberbank.ru/api/v1"
        user= self.user or None
        password= self.password or None
        ca_bundle_file= self.ca_bundle_file or None
        cert_file= self.cert_file or None
        key_file= self.key_file or None
        key_file_password= self.key_file_password or None
        timeout= self.timeout or None
        verify_ssl_certs= self.verify_ssl_certs
        profanity_check= self.profanity_check
        temperature= self.temperature if self.temperature is not None else 0.1
        some_other_param = self.some_other_param or None
        json_mode = bool(output_schema_dict) or self.json_mode
        streaming = self.streaming 

        output = GigaChat(
                credentials=credentials,
                access_token= access_token,
                scope=scope,
                model=model,
                verify_ssl_certs=verify_ssl_certs,
                streaming=streaming,
                max_tokens=max_tokens,
                base_url=base_url,
                user=user,
                password=password,
                ca_bundle_file=ca_bundle_file,
                cert_file=cert_file,
                key_file=key_file,
                key_file_password=key_file_password,
                timeout=timeout,
                profanity_check=profanity_check,
                temperature=temperature,
                top_p=some_other_param,
            )
        
        if json_mode:
            if output_schema_dict:
                output = output.with_structured_output(schema=output_schema_dict, method="json_mode")
            else:
                output = output.bind(response_format={"type": "json_object"})

        return output
