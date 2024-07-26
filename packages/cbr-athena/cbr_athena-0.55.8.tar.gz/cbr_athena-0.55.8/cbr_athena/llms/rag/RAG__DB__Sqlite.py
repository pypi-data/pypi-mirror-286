from cbr_athena.llms.API_Open_AI import API_Open_AI
from osbot_utils.base_classes.Type_Safe             import Type_Safe
from osbot_utils.decorators.methods.cache_on_self   import cache_on_self
from osbot_utils.helpers.sqlite.domains.Sqlite__DB  import Sqlite__DB
from osbot_utils.helpers.sqlite.Sqlite__Database    import Sqlite__Database


class Schema__RAG_DATA(Type_Safe):
    status: str


TABLE_NAME__RAG__RAG_DATA       = 'rag_data'
TABLE_NAME__RAG__RAG_EMBEDDINGS = 'rag_embeddings'
TABLE_SCHEMA__RAG_DATA          = Schema__RAG_DATA


class RAG__DB__Sqlite(Sqlite__DB):
    api_open_ai : API_Open_AI

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def tables_to_add(self):
        return { TABLE_NAME__RAG__RAG_DATA: TABLE_SCHEMA__RAG_DATA }

    @cache_on_self
    def table_rag_data(self):
        return self.table(TABLE_NAME__RAG__RAG_DATA)

    def add_content(self, title, content):
        rag_data = self.table_rag_data()
        embeddings = self.api_open_ai.embeddings(content,dimensions=256)           # try with 256 embeddings values
        return embeddings