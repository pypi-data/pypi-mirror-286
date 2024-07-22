import datetime
from abc import ABC, abstractmethod
from typing import List

from freshpointsync import Product
from rich.padding import Padding
from rich.style import Style
from rich.table import Table, box
from rich.text import Text

from .styles import AppColors


class QueryResultTableABC(ABC):
    def __init__(self) -> None:
        self.table = self._construct()

    @abstractmethod
    def _construct(self) -> Table:
        pass


class QueryResultTable(QueryResultTableABC):
    def _construct(self) -> Table:  # noqa: PLR6301
        now = datetime.datetime.now().strftime('%Y/%m/%d, %H:%M:%S')
        table = Table(
            title=f'Query results {now}',
            title_justify='center',
            show_header=True,
            header_style='bold default',
            expand=True,
        )
        table.add_column('Name', ratio=4)
        table.add_column('Category', ratio=2)
        table.add_column('Price', ratio=1)
        table.add_column('Quantity', ratio=1)
        table.box = box.ASCII2
        return table

    @property
    def is_empty(self) -> bool:
        return self.table.row_count == 0

    @staticmethod
    def format_name(product: Product) -> Text:
        if product.is_sold_out:
            style = Style(color='default', dim=True)
        elif product.is_last_piece:
            style = Style(color='default', blink=False)
        else:
            style = Style(color='default')
        return Text(product.name, style=style)

    @staticmethod
    def format_category(product: Product) -> Text:
        style = Style(color='default')
        return Text(product.category, style=style)

    @staticmethod
    def format_price(product: Product) -> Text:
        if product.is_on_sale:
            discount = int(round(product.discount_rate * 100))
            text = f'{product.price_curr:.02f} CZK (-{discount}%)'
            style = Style(color=AppColors.GREEN.value)
        else:
            text = f'{product.price_curr:.02f} CZK'
            style = Style(color='default')
        return Text(text, style=style)

    @staticmethod
    def format_quantity(product: Product) -> Text:
        if product.is_sold_out:
            style = Style(color=AppColors.RED.value)
        elif product.is_last_piece:
            style = Style(color=AppColors.YELLOW.value)
        else:
            style = Style(color=AppColors.GREEN.value)
        return Text(str(product.quantity), style=style)

    def add_row(self, product: Product, end_section: bool = False) -> None:
        padding = (0, 0, 0, 0) if end_section else (0, 0, 1, 0)  # t, r, b, l
        self.table.add_row(
            Padding(self.format_name(product), padding),
            Padding(self.format_category(product), padding),
            Padding(self.format_price(product), padding),
            Padding(self.format_quantity(product), padding),
            end_section=end_section,
        )

    def add_rows(self, products: List[Product]) -> None:
        if not products:
            return
        end_section = False
        for i, product in enumerate(products[:-1]):
            product_next = products[i + 1]
            end_section = product.category != product_next.category
            self.add_row(product, end_section)
        self.add_row(product=products[-1], end_section=True)


class QueryResultTableFailed(QueryResultTableABC):
    def __init__(self, reason: str) -> None:
        self.reason = reason
        super().__init__()

    def _construct(self) -> Table:
        now = datetime.datetime.now().strftime('%Y/%m/%d, %H:%M:%S')
        table = Table(
            title=f'Query results {now}',
            show_header=False,
            expand=True,
        )
        text = Text(
            self.reason,
            style=Style(color=AppColors.RED.value),
            justify='center',
        )
        table.add_row(text)
        table.box = box.ASCII2
        return table
