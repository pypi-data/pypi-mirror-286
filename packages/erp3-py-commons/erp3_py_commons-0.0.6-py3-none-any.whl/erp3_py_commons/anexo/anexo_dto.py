import datetime
import uuid

from enum import Enum

from nsj_rest_lib.decorator.dto import DTO
from nsj_rest_lib.descriptor.dto_field import DTOField
from nsj_rest_lib.dto.dto_base import DTOBase


class TipoAnexo(Enum):
    GENERICO = ("generico", 0)
    NFE_XML = ("nfe_xml", 1)
    NFE_DANFE = ("nfe_danfe", 2)
    NFSE_XML = ("nfse_xml", 3)
    NFSE_PDF = ("nfse_pdf", 4)
    BOLETO_PDF = ("boleto_pdf", 5)
    BOLETO_REMESSA = ("boleto_remessa", 6)

    @classmethod
    def from_int_value(cls, int_value):
        for item in cls:
            if item.value[1] == int(int_value):
                return item
        raise ValueError(f"TipoAnexo {int_value} inválido.")


class ModuloAnexo(Enum):
    # Desktop
    BEM_PATRIMONIAL = ("bem_patrimonial", 0)
    CONTRATO = ("contrato", 1)
    OS_RPS_TITULO = ("os_rps_titulo", 2)
    ORDEM_SERVICO = ("ordem_servico", 3)
    REQUISICAO_COMPRA = ("requisicao_compra", 4)
    NEGOCIO = ("negocio", 5)
    DOCUMENTO_FISCAL = ("documento_fiscal", 6)
    ESTABELECIMENTO = ("estabelecimento", 7)
    # Web
    ATENDIMENTO = ("atendimento", 1001)
    FOLLOWUP = ("followup", 1002)
    ATIVIDADE = ("atividade", 1003)


@DTO()
class AnexoDTO(DTOBase):
    id: uuid.UUID = DTOField(
        pk=True, resume=True, default_value=uuid.uuid4, entity_field="documentoged"
    )  # description="Conteúdo do anexo em base64"
    url: str = DTOField(resume=True)  # description="URL para download do anexo"
    conteudo: str = DTOField()  # description="Conteúdo do anexo em base64"
    conteudo_binario: bytes = DTOField()
    nome: str = DTOField(
        not_null=True, resume=True, max=255, strip=True
    )  # description="Nome do anexo"
    descricao: str = DTOField(
        resume=True, max=255, strip=True
    )  # description="Descrição do anexo"
    mimetype: str = DTOField(
        resume=True, max=255, strip=True
    )  # description="MIME type do anexo"
    tipo: TipoAnexo = DTOField(
        resume=True, default_value=TipoAnexo.GENERICO
    )  # description="Tipo do anexo"
    data: datetime.datetime = DTOField(
        default_value=datetime.datetime.now, resume=True
    )  # description="Tipo do anexo"
    grupo_anexos: uuid.UUID = DTOField(
        not_null=True, resume=True, entity_field="id_modulodoanexo"
    )  # description="ID do grupo de anexos ao qual este anexo pertence"
    modulo: ModuloAnexo = DTOField(
        not_null=True, resume=True, entity_field="modulodoanexo"
    )  # description="Enum indicando o módulo do ERP, ao qual o anexo pertence"
