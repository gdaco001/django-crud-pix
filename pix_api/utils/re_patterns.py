# Regex patterns for validation
import re
from apps.core.choices import pix_key_type_choices

PATTERN_MAP = {
    "CPF": r"^[0-9]{3}[\.]?[0-9]{3}[\.]?[0-9]{3}[-]?[0-9]{2}$",
    "CNPJ": r"^[0-9]{2}[\.]?[0-9]{3}[\.]?[0-9]{3}[\/]?[0-9]{4}[-]?[0-9]{2}$",
    "EMAIL": r"^[A-Z0-9+_.-]+@[A-Z0-9.-]+$",
    "TELEFONE": r"^((?:\+?55)?)([1-9][0-9])(9[0-9]{8})$",
    "CHAVE_ALEATORIA": r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
}

FILTERING_MAP_PATTERNS = {
    "CPF": PATTERN_MAP["CPF"],
    "CNPJ": PATTERN_MAP["CNPJ"],
    "TELEFONE": PATTERN_MAP["TELEFONE"],
}


def turn_cpf_cnpj_telefone_into_numeric(string: str) -> str:
    for pattern in FILTERING_MAP_PATTERNS.values():
        match = re.match(pattern, string)
        if match:
            return re.sub("[^0-9]", "", string)
    return string


def mask_document(document: str) -> str:
    if re.match(PATTERN_MAP["CPF"], document):
        return f"{document[:3]}.{document[3:6]}.{document[6:9]}-{document[9:]}"
    return f"{document[:2]}.{document[2:5]}.{document[5:8]}/{document[8:12]}-{document[12:]}"


def convert_to_numerals(string: str) -> str:
    return re.sub("[^0-9]", "", string)


def unmask_pix_key(pix_key: str, pix_key_type) -> str:
    if pix_key_type not in [
        pix_key_type_choices.chave,
        pix_key_type_choices.email,
    ]:
        return convert_to_numerals(pix_key)

    elif pix_key_type == pix_key_type_choices.email:
        return pix_key.upper()
    else:
        return pix_key


def mask_pix_key(pix_key: str, pix_key_type) -> str:
    if pix_key_type in [
        pix_key_type_choices.cpf,
        pix_key_type_choices.cnpj,
    ]:
        return mask_document(pix_key)
    else:
        return pix_key
