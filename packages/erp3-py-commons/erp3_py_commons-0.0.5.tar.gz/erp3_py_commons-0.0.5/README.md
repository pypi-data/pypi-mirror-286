# ERP3-PY-COMMONS

Utilitários python comuns a diversos aplicativos relacionados ao BD desktop (para APIs multibanco).

## Módulos disponíveis

### Anexos

Código, compatível com o RestLib, para manipulação de anexos no padrão do ERP SQL (gerindo as tabelas ns.documentosged e ns.anexosmodulos).

O DTO pode ser diretamente utilizado em propriedades do tipo DTOListFiel, conforme exemplo:

```python
anexos: list[AnexoDTO] = DTOListField(
    dto_type=AnexoDTO,
    service_name="anexo_service",
    relation_key_field="id_conjunto_anexo",
    related_entity_field="grupo_anexos",
)
```

Note que é preciso declarar um "service_name" customizado (que deve estar contido em seu InjectorFactory), apontando para o service de anexos contido no mesmo módulo. O que pode ser feito conforme exemplo abaixo:

```python
def anexo_dao(self):
    from erp3_py_commons.anexo.anexo_dao import AnexoDAO

    return AnexoDAO(self.db_adapter())

def anexo_service(self):
    from erp3_py_commons.anexo.anexo_service import AnexoService

    return AnexoService(self.anexo_dao())
```

## Ambiente de desenvolvimento

Sugere-se utilizar um virtual environment para cooperar com esse projeto:

```sh
python3 -m venv .venv
source ./.venv/bin/activate
pip install -r requirements.txt
```

Obs.: Instale também as dependências de desenvolvimento:

> pip install -r requirements-dev.txt

## Testes automatizados

Após qualquer alteração no projeto, e antes de qualquer commit, rode os testes automatizados;

> make tests

## Verisionando o projeto

1. Instale os pacotes de build de upload do python:
 
> make install_to_pkg

2. Altere o número da versão no arquivo `setup.cfg`:

```cfg
version = 0.0.1
```

3. Construa o pacote:

> make build_pkg

4. Faça upload do pacote:

> make upload_pkg

**Obs.: Como pré-requisito, é preciso ter sua conta do pypi configurada em sua máquina, além de autorização para gestão do projeto em si (ver site oficial pypi.org).**