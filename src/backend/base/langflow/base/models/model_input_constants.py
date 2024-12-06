from langflow.base.models.model import LCModelComponent
from langflow.components.models.openai import OpenAIModelComponent
from langflow.components.models.gigachat import GigaChatModelComponent
from langflow.inputs.inputs import SecretStrInput


def get_filtered_inputs(component_class):
    base_input_names = {field.name for field in LCModelComponent._base_inputs}
    component_instance = component_class()

    return [process_inputs(input_) for input_ in component_instance.inputs if input_.name not in base_input_names]


def process_inputs(component_data):
    if isinstance(component_data, SecretStrInput):
        component_data.value = ""
        component_data.load_from_db = False
    elif component_data.name == "temperature":
        component_data = set_advanced_true(component_data)
    return component_data


def set_advanced_true(component_input):
    component_input.advanced = True
    return component_input


def create_input_fields_dict(inputs, prefix):
    return {f"{prefix}{input_.name}": input_ for input_ in inputs}


def _get_openai_inputs_and_fields():
    try:
        from langflow.components.models.openai import OpenAIModelComponent

        openai_inputs = get_filtered_inputs(OpenAIModelComponent)
    except ImportError as e:
        msg = "OpenAI is not installed. Please install it with `pip install langchain-openai`."
        raise ImportError(msg) from e
    return openai_inputs, {input_.name: input_ for input_ in openai_inputs}


def _get_gigachat_inputs_and_fields():
    try:
        from langflow.components.models.gigachat import GigaChatModelComponent

        gigachat_inputs = get_filtered_inputs(GigaChatModelComponent)
    except ImportError as e:
        msg = "NVIDIA is not installed. Please install it with `pip install langchain-gigachat`."
        raise ImportError(msg) from e
    return gigachat_inputs, create_input_fields_dict(gigachat_inputs, "")


MODEL_PROVIDERS_DICT = {}

# Try to add each provider
try:
    openai_inputs, openai_fields = _get_openai_inputs_and_fields()
    MODEL_PROVIDERS_DICT["OpenAI"] = {
        "fields": openai_fields,
        "inputs": openai_inputs,
        "prefix": "",
        "component_class": OpenAIModelComponent(),
    }
except ImportError:
    pass


try:
    gigachat_inputs, gigachat_fields = _get_gigachat_inputs_and_fields()
    MODEL_PROVIDERS_DICT["GigaChat"] = {
        "fields": gigachat_fields,
        "inputs": gigachat_inputs,
        "prefix": "",
        "component_class": GigaChatModelComponent(),
    }
except ImportError:
    pass

MODEL_PROVIDERS = list(MODEL_PROVIDERS_DICT.keys())
ALL_PROVIDER_FIELDS: list[str] = [field for provider in MODEL_PROVIDERS_DICT.values() for field in provider["fields"]]
