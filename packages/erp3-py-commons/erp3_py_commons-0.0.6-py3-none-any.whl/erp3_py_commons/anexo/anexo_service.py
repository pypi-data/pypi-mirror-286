import base64
import os
import re
import uuid

from flask import request
from typing import Any, Callable, Dict, List, Set

from nsj_rest_lib.service.service_base import ServiceBase

from erp3_py_commons.anexo.anexo_dto import AnexoDTO
from erp3_py_commons.anexo.anexo_dao import AnexoDAO

from nsj_rest_lib.dto.dto_base import DTOBase
from nsj_rest_lib.entity.entity_base import EntityBase
from nsj_rest_lib.injector_factory_base import NsjInjectorFactoryBase


class AnexoService(ServiceBase):
    _dao: AnexoDAO

    def __init__(
        self,
        dao: AnexoDAO,
    ):
        self._dao = dao
        self.control_transaction = True

    def disable_control_transaction(self):
        self.control_transaction = False

    def get(
        self,
        id: str,
        partition_fields: Dict[str, Any],
        fields: Dict[str, Set[str]],
        conteudo_em_bytes: bool = False,
    ) -> DTOBase:
        model = self._dao.get(id)

        # Tratando da codificação do conteúdo em Base64
        conteudo = model["documento"]
        if conteudo is not None:
            if not conteudo_em_bytes:
                conteudo = base64.b64encode(conteudo).decode("utf-8")
                conteudo_bytes = None
            else:
                conteudo_bytes = conteudo
                conteudo = None
        del model["documento"]

        # Montando a URL de download
        url = self._get_url_download_anexo(model["documentoged"])

        # Construindo o DTO de retorno
        return AnexoDTO(
            **model,
            conteudo=conteudo,
            conteudo_binario=conteudo_bytes,
            kwargs_as_entity=True,
            url=url,
        )

    def _get_url_download_anexo(self, id: uuid.UUID, tenant: int = None):
        # Getting URL base from request
        if os.getenv("ENV", "").lower() != "erp_sql":
            base_url = request.base_url

            if tenant is None:
                if "tenant" in request.args:
                    tenant = request.args["tenant"]
                else:
                    raise Exception("Faltando parâmetro 'tenant' na requisição.")
        else:
            base_url = ""

        # Deixando apenas as duas primeiras partes da URL base
        if len(base_url) > 0:
            match = re.match("(https?://[^/]+/[^/]+)(/.*)?", base_url)
            if match is not None:
                base_url = match.group(1)

            if base_url[-1] != "/":
                base_url = f"{base_url}/"

        # Getting URL from download atach endpoint
        download_attach = os.getenv("URL_DOWNLOAD_ANEXOS", "")

        if len(download_attach) > 0 and download_attach[0] == "/":
            download_attach = download_attach[1:]

        if len(download_attach) > 0 and download_attach[-1] == "/":
            download_attach = download_attach[:-1]

        # Making final URL
        return f"{base_url}{download_attach}/{id}?tenant={tenant}"

    def list(
        self,
        after: uuid.UUID,
        limit: int,
        fields: Dict[str, Set[str]],
        order_fields: List[str],
        filters: Dict[str, Any],
        search_query: str = None,
    ) -> List[DTOBase]:

        # Tratando dos filtros
        grupo_anexos = None
        if "grupo_anexos" in filters:
            grupo_anexos = filters["grupo_anexos"]

        modulo = None
        if "modulo" in filters:
            modulo = filters["modulo"]

        tipo = None
        if "tipo" in filters:
            tipo = filters["tipo"]

        mimetype = None
        if "mimetype" in filters:
            mimetype = filters["mimetype"]

        data = None
        if "data" in filters:
            data = filters["data"]

        # Retrieving from DAO
        model_list = self._dao.list(grupo_anexos, modulo, tipo, mimetype, data)

        # Convertendo para uma lista de DTOs
        dto_list = []
        for model in model_list:
            # Tratando da codificação do conteúdo em Base64
            conteudo = model["documento"]
            if conteudo is not None:
                conteudo = base64.b64encode(conteudo).decode(encoding="utf-8")
            del model["documento"]

            # Montando a URL de download
            url = self._get_url_download_anexo(model["documentoged"])

            # Criando o DTO
            dto = AnexoDTO(**model, conteudo=conteudo, kwargs_as_entity=True, url=url)

            # Adicionando o DTO na lista
            dto_list.append(dto)

        # Returning
        return dto_list

    def insert(
        self,
        dto: AnexoDTO,
        aditional_filters: Dict[str, Any] = None,
        custom_before_insert: Callable = None,
        custom_after_insert: Callable = None,
    ) -> DTOBase:
        try:
            start_transaction = False
            if self.control_transaction and not self._dao._db.in_transaction():
                start_transaction = True
                self._dao._db.begin()

            # Inserindo na tabela documentosged
            conteudo_decodificado = dto.conteudo
            if conteudo_decodificado is not None:
                conteudo_decodificado = base64.b64decode(dto.conteudo)

            self._dao.inserir_documento_ged(
                dto.id,
                dto.nome,
                conteudo_decodificado,
                dto.mimetype,
                dto.data,
            )

            # Inserindo na tabela anexosmodulos
            self._dao.inserir_anexo_modulo(
                dto.nome,
                dto.descricao,
                dto.grupo_anexos,
                dto.id,
                dto.tipo.value[1],
                dto.modulo.value[1],
            )

            if start_transaction:
                self._dao._db.commit()

            return None
        finally:
            if start_transaction:
                self._dao._db.rollback()

    def update(
        self,
        dto: AnexoDTO,
        id: Any,
        aditional_filters: Dict[str, Any] = None,
        custom_before_update: Callable = None,
        custom_after_update: Callable = None,
    ) -> DTOBase:
        self._update(dto, id, False)
        return None

    def _update(
        self,
        dto: AnexoDTO,
        id: Any,
        partial_update: bool,
    ):

        try:
            start_transaction = False
            if self.control_transaction and not self._dao._db.in_transaction():
                start_transaction = True
                self._dao._db.begin()

            # Atualizando a tabela documentosged
            conteudo_decodificado = dto.conteudo
            if conteudo_decodificado is not None:
                conteudo_decodificado = base64.b64decode(dto.conteudo)

            self._dao.update_documento_ged(
                id,
                dto.nome,
                conteudo_decodificado,
                dto.mimetype,
                dto.data,
                partial_update=partial_update,
            )

            # Recuperando o ID da tabela anexosmodulos
            grupo_anexos = dto.grupo_anexos
            if grupo_anexos is None:
                dto_old = self.get(id)
                grupo_anexos = dto_old.grupo_anexos

            # Atualizando na tabela anexosmodulos
            self._dao.update_anexo_modulo(
                grupo_anexos,
                dto.nome,
                dto.descricao,
                dto.grupo_anexos,
                dto.id,
                dto.tipo.value if dto.tipo is not None else None,
                dto.modulo.value if dto.modulo is not None else None,
                partial_update=partial_update,
            )

            if start_transaction:
                self._dao._db.commit()
        finally:
            if start_transaction:
                self._dao._db.rollback()

    def partial_update(
        self,
        dto: DTOBase,
        id: Any,
        aditional_filters: Dict[str, Any] = None,
        custom_before_update: Callable = None,
        custom_after_update: Callable = None,
    ) -> DTOBase:
        self._update(dto, id, True)
        return None

    def delete(self, id: Any, additional_filters: Dict[str, Any] = None) -> DTOBase:
        try:
            start_transaction = False
            if self.control_transaction and not self._dao._db.in_transaction():
                start_transaction = True
                self._dao._db.begin()

            # Inserindo na tabela documentosged
            self._dao.delete_documento_ged(id)

            # Inserindo na tabela anexosmodulos
            self._dao.delete_anexo_modulo(id)

            if start_transaction:
                self._dao._db.commit()

            return None
        finally:
            if start_transaction:
                self._dao._db.rollback()
