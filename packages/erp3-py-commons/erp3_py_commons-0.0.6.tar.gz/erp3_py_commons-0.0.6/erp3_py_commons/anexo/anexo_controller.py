import io
import logging
import mimetypes
import os
import uuid

from flask import send_file

from nsj_gcf_utils.db_adapter2 import DBAdapter2
from nsj_gcf_utils.rest_error_util import format_json_error
from nsj_rest_lib.controller.controller_util import DEFAULT_RESP_HEADERS

from erp3_py_commons.anexo.anexo_dao import AnexoDAO
from erp3_py_commons.anexo.anexo_service import AnexoService


def get_logger():
    APP_NAME = os.getenv("APP_NAME", "erp3-py-commons")
    return logging.getLogger(APP_NAME)


def download_anexo(db: DBAdapter2, id: uuid.UUID):

    try:
        # Recuperando o nexo pelo ID
        dao = AnexoDAO(db)
        service = AnexoService(dao)

        # Conteúdo do arquivo em bytes (pode variar dependendo do ID)
        anexo = service.get(id, None, None, conteudo_em_bytes=True)

        # Crie um objeto BytesIO
        byte_io = io.BytesIO()
        byte_io.write(anexo.conteudo_binario)
        byte_io.seek(0)

        # Resolvendo o mimetype
        mimetype = anexo.mimetype
        if mimetype is None:
            mimetype, _ = mimetypes.guess_type(anexo.nome)

        # Envie o arquivo
        return send_file(
            byte_io,
            as_attachment=True,
            download_name=anexo.nome,
            mimetype=mimetype,
        )
    except Exception as e:
        get_logger().exception(e)
        return (
            format_json_error(f"Erro desconhecido: {e}"),
            500,
            {**DEFAULT_RESP_HEADERS},
        )
