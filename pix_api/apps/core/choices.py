from easy_choices.choices import Choices
from django.utils.translation import gettext_lazy as _


pix_key_type_choices = Choices(
    ("CPF", "cpf", _("CPF")),
    ("CNPJ", "cnpj", _("CNPJ")),
    ("EMAIL", "email", _("E-mail")),
    ("TELEFONE", "telefone", _("Telefone")),
    ("CHAVE_ALEATORIA", "chave", _("Chave Aleatória")),
)

receiver_status_choices = Choices(
    ("VALIDADO", "validado", _("Validado")),
    ("INVALIDO", "invalido", _("Inválido")),
    ("RASCUNHO", "rascunho", _("Rascunho")),
)

document_type_choices = Choices(
    ("CNPJ", "cnpj", _("CNPJ")),
    ("CPF", "cpf", _("CPF")),
)
