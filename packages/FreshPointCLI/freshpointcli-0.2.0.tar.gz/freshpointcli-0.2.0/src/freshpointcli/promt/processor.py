import argparse
from typing import List, Optional

from freshpointsync import Product, ProductPage
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.history import FileHistory
from prompt_toolkit.patch_stdout import patch_stdout

from ..logger import logger
from .completers import QueryCompleter
from .lexers import PygmentsLexer, QueryLexer
from .parsers import QueryParser, get_constraints
from .styles import FreshpointStyle
from .tables import (
    QueryResultTable,
    QueryResultTableABC,
    QueryResultTableFailed,
)


class PromptProcessor:
    def __init__(
        self,
        app_name: str,
        page: ProductPage,
        history_file: Optional[str] = None,
    ) -> None:
        self.page = page
        self.parser = QueryParser()
        self.completer = QueryCompleter(page.data.products.values())
        self.prompt_text = FormattedText([
            ('class:app_name', app_name),
            ('class:at', '@'),
            ('class:location', page.data.location),
            ('class:prompt_arrow', '> '),
        ])
        self.session: PromptSession = PromptSession(
            completer=self.completer,
            lexer=PygmentsLexer(QueryLexer),
            style=FreshpointStyle,
            history=FileHistory(history_file) if history_file else None,
            auto_suggest=AutoSuggestFromHistory(),
        )

    async def await_responce(self) -> str:
        with patch_stdout():
            response = await self.session.prompt_async(self.prompt_text)
        return response

    def parse_responce(self, responce: str) -> Optional[argparse.Namespace]:
        try:
            responce_split = self.parser.split_args(responce)
            return self.parser.parse_args_safe(responce_split)
        except Exception as e:
            logger.warning(f'Error parsing query: {e}')
            return None

    def filter_products(self, args: argparse.Namespace) -> List[Product]:
        constaints = get_constraints(args)
        return self.page.find_products(
            constraint=lambda p: all(constr(p) for constr in constaints)
        )

    def process_responce_args(
        self, args: Optional[argparse.Namespace]
    ) -> QueryResultTableABC:
        if args is None:
            return QueryResultTableFailed('No products found for given query.')
        products = self.filter_products(args)
        if products:
            table = QueryResultTable()
            table.add_rows(products)
            return table
        else:
            return QueryResultTableFailed('No products found for given query.')
