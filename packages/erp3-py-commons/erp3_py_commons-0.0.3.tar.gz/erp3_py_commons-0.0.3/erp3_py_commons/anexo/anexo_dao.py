import datetime
import uuid

from nsj_gcf_utils.db_adapter2 import DBAdapter2
from nsj_rest_lib.exception import (
    ConflictException,
    NotFoundException,
)


class AnexoDAO:

    def __init__(self, db_adapter: DBAdapter2):
        self._db = db_adapter

    def get(self, id: uuid.UUID):
        sql = """
        with anexo_modulo_por_doc as (
            select
                am.documentoged, max(am.anexomodulo::text)::uuid as anexomodulo
            from
                ns.anexosmodulos as am
            group by
                am.documentoged
        )
        select
            dg.data, dg.nome, dg.documento, dg.mimetype, dg.documentoged, am.descricao, am.tipo, am.id_modulodoanexo, am.modulodoanexo
        from
            ns.documentosged as dg
            left join anexo_modulo_por_doc as amd on (amd.documentoged = dg.documentoged)
            left join ns.anexosmodulos as am on (am.anexomodulo = amd.anexomodulo)
        where
            dg.documentoged = :id
        """

        # Executando a query
        resp = self._db.execute_query(sql, id=id)

        # Checking if ID was found
        if len(resp) <= 0:
            raise NotFoundException(f"Anexo com id {id} não encontrado.")

        # Verificando se foi encontrado mais de um registro para o ID passado
        if len(resp) > 1:
            raise ConflictException(f"Encontrado mais de um Anexo, para o id {id}.")

        return resp[0]

    def list(
        self,
        grupo_anexos: uuid.UUID,
        modulo: int,
        tipo: int,
        mimetype: str,
        data: datetime.datetime,
    ):
        # Montando os filtros
        sql_where = "true"

        if grupo_anexos is not None:
            sql_where += "\nand am.id_modulodoanexo = :grupo_anexos"

        if modulo is not None:
            sql_where += "\nand am.modulodoanexo = :modulo"

        if tipo is not None:
            sql_where += "\nand am.tipo = :tipo"

        if mimetype is not None:
            sql_where += "\nand dg.mimetype = :mimetype"

        if data is not None:
            sql_where += "\nand dg.data = :data"

        # Motando a query principal
        sql = f"""
        with anexo_modulo_por_doc as (
            select
                am.documentoged, max(am.anexomodulo::text)::uuid as anexomodulo
            from
                ns.anexosmodulos as am
            group by
                am.documentoged
        )
        select
            dg.data, dg.nome, dg.documento, dg.mimetype, dg.documentoged, am.descricao, am.tipo, am.id_modulodoanexo, am.modulodoanexo
        from
            ns.documentosged as dg
            left join anexo_modulo_por_doc as amd on (amd.documentoged = dg.documentoged)
            left join ns.anexosmodulos as am on (am.anexomodulo = amd.anexomodulo)
        where
            {sql_where}
        """

        return self._db.execute_query(
            sql,
            grupo_anexos=grupo_anexos,
            modulo=modulo,
            tipo=tipo,
            mimetype=mimetype,
            data=data,
        )

    def inserir_documento_ged(
        self,
        id: uuid.UUID,
        nome: str,
        conteudo: str,
        mimetype: str,
        data: datetime.datetime,
    ) -> str:
        self._db.execute(
            "INSERT INTO ns.documentosged (data, nome, documento, mimetype, documentoged) VALUES (:data, :nome, :conteudo, :mimetype, :id)",
            data=data,
            nome=nome,
            conteudo=conteudo,
            mimetype=mimetype,
            id=id,
        )

    def inserir_anexo_modulo(
        self,
        nome: str,
        descricao: str,
        id_modulodoanexo: str,
        documento_ged_id: str,
        tipo: int,
        modulo_anexo: int,
    ) -> str:
        anexo_modulo_id = str(uuid.uuid4())
        self._db.execute(
            """INSERT INTO ns.anexosmodulos (anexomodulo, arquivo, descricao, modulodoanexo, id_modulodoanexo, documentoged, tipo)
            VALUES (:anexomodulo, :arquivo, :descricao, :modulodoanexo, :id_modulodoanexo, :documentoged, :tipo)""",
            anexomodulo=anexo_modulo_id,
            arquivo=nome,
            descricao=descricao,
            modulodoanexo=modulo_anexo,
            id_modulodoanexo=id_modulodoanexo,
            documentoged=documento_ged_id,
            tipo=tipo,
        ),
        return anexo_modulo_id

    def delete_documento_ged(
        self,
        id: uuid.UUID,
    ) -> str:
        self._db.execute("delete from ns.documentosged where documentoged = :id", id=id)

    def delete_anexo_modulo(
        self,
        documento_ged_id: uuid.UUID,
    ) -> str:
        self._db.execute(
            "delete from ns.anexosmodulos where documentoged=:documento_ged_id",
            documento_ged_id=documento_ged_id,
        ),

    def update_documento_ged(
        self,
        id: uuid.UUID,
        nome: str,
        conteudo: str,
        mimetype: str,
        data: datetime.datetime,
        partial_update: bool = False,
    ) -> str:
        dados = {
            "data": data,
            "nome": nome,
            "conteudo": conteudo,
            "mimetype": mimetype,
            "id": id,
        }

        # Montando a parte dos campos no SQL
        sql_fields_set = []
        if not partial_update or data is not None:
            sql_fields_set.append("data=:data")
        if not partial_update or nome is not None:
            sql_fields_set.append("nome=:nome")
        if not partial_update or conteudo is not None:
            sql_fields_set.append("documento=:conteudo")
        if not partial_update or mimetype is not None:
            sql_fields_set.append("mimetype=:mimetype")

        if len(sql_fields_set) <= 0:
            raise Exception(
                "Ao menos uma das propriedades deve ser passada para uma atualização parcial (PATCH)."
            )

        sql_fields_set = ", ".join(sql_fields_set)

        # Executando o update
        self._db.execute(
            f"update ns.documentosged set {sql_fields_set} where documentoged=:id",
            **dados,
        )

    def update_anexo_modulo(
        self,
        id: uuid.UUID,
        nome: str,
        descricao: str,
        id_modulodoanexo: str,
        documento_ged_id: str,
        tipo: int,
        modulo_anexo: int,
        partial_update: bool = False,
    ) -> str:
        dados = {
            "id": id,
            "nome": nome,
            "descricao": descricao,
            "id_modulodoanexo": id_modulodoanexo,
            "documento_ged_id": documento_ged_id,
            "tipo": tipo,
            "modulo_anexo": modulo_anexo,
        }

        # Montando a parte dos campos no SQL
        sql_fields_set = []
        if not partial_update or nome is not None:
            sql_fields_set.append("arquivo=:nome")
        if not partial_update or descricao is not None:
            sql_fields_set.append("descricao=:descricao")
        if not partial_update or id_modulodoanexo is not None:
            sql_fields_set.append("id_modulodoanexo=:id_modulodoanexo")
        if not partial_update or documento_ged_id is not None:
            sql_fields_set.append("documentoged=:documento_ged_id")
        if not partial_update or tipo is not None:
            sql_fields_set.append("tipo=:tipo")
        if not partial_update or modulo_anexo is not None:
            sql_fields_set.append("modulodoanexo=:modulo_anexo")

        if len(sql_fields_set) <= 0:
            raise Exception(
                "Ao menos uma das propriedades deve ser passada para uma atualização parcial (PATCH)."
            )

        sql_fields_set = ", ".join(sql_fields_set)

        # Executando o update
        self._db.execute(
            f"update ns.anexosmodulos set {sql_fields_set} where anexomodulo=:id",
            **dados,
        )
