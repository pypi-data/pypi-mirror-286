import argparse
import os
import shlex
from functools import lru_cache
from typing import Any, Callable, List, Optional, Sequence, Tuple, Type, TypeVar

from freshpointsync import Product
from rich.console import Console
from rich.markdown import Markdown
from unidecode import unidecode


@lru_cache(maxsize=4096)
def format_str(s: object) -> str:
    return unidecode(str(s)).strip().casefold()


T = TypeVar('T', int, float)


class ArgTypes:
    @staticmethod
    def nonnegative_number(value: object, type_cls: Type[T]) -> T:
        try:
            value_converted = type_cls(value)  # type: ignore[arg-type]
        except Exception as e:
            raise ValueError(f'Value "{value}" is not a valid number') from e
        if value_converted < 0:
            raise ValueError(f'Value "{value}" cannot be negative')
        return value_converted

    @classmethod
    def nonnegative_float(cls, value: object) -> float:
        return cls.nonnegative_number(value, float)

    @classmethod
    def nonnegative_int(cls, value: object) -> int:
        if not str(value).isdigit():
            raise ValueError(f'Value "{value}" is not an integer')
        return cls.nonnegative_number(value, int)


def parse_args_init() -> argparse.Namespace:
    class ArgumentParser(argparse.ArgumentParser):
        def print_help(self, file=None) -> None:  # noqa: PLR6301, ANN001
            prompt_dir = os.path.dirname(os.path.abspath(__file__))
            root_dir = os.path.dirname(prompt_dir)
            readme_path = os.path.join(root_dir, 'README.md')
            with open(readme_path, encoding='utf-8') as f:
                message = Markdown(f.read())
            console = Console(file=file)
            console.print(message)

    parser = ArgumentParser()
    parser.add_argument('location_id', nargs='?', type=ArgTypes.nonnegative_int)
    return parser.parse_args()


class QueryParserHelpFormatter(argparse.HelpFormatter):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        if 'max_help_position' not in kwargs:
            kwargs['max_help_position'] = 52
        super().__init__(*args, **kwargs)


class QueryParser(argparse.ArgumentParser):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        if 'formatter_class' not in kwargs:
            kwargs['formatter_class'] = QueryParserHelpFormatter
        kwargs['add_help'] = False
        super().__init__(*args, **kwargs)
        self._add_arguments_init()

    def _add_arguments_init(self) -> None:
        group_name = self.add_mutually_exclusive_group()
        group_name.add_argument(
            'positional_name',
            nargs='?',
            help=(
                'Product name. Filters search results by name. '
                'Mutually exclusive with the --name argument.'
            ),
        )
        group_name.add_argument(
            '-n',
            '--name',
            help=(
                'Product name. Filters search results by name. '
                'Enables autocompletion after a query argument. '
                'Mutually exclusive with the positional product name argument.'
            ),
        )
        self.add_argument(
            '-c',
            '--category',
            help='Product category. Filters search results by category.',
        )
        self.add_argument(
            '-p',
            '--price-min',
            type=ArgTypes.nonnegative_float,
            help=(
                'Minimum product price (CZK). '
                'Sets the lowest price of a product listing.'
            ),
        )
        self.add_argument(
            '-P',
            '--price-max',
            type=ArgTypes.nonnegative_float,
            help=(
                'Maximum product price (CZK). '
                'Sets the highest price of a product listing.'
            ),
        )
        self.add_argument(
            '-q',
            '--quantity-min',
            type=ArgTypes.nonnegative_int,
            help=(
                'Minimum product quantity (pcs). '
                'Sets the minimum number of available product pieces.'
            ),
        )
        self.add_argument(
            '-Q',
            '--quantity-max',
            type=ArgTypes.nonnegative_int,
            help=(
                'Maximum product quantity (pcs). '
                'Sets the maximum number of available product pieces.'
            ),
        )
        self.add_argument(
            '-s',
            '--sale',
            action='store_true',
            help=(
                'Sale flag. Filters search results to include '
                'only products that are currently on sale.'
            ),
        )
        self.add_argument(
            '-a',
            '--available',
            action='store_true',
            help=(
                'Availability flag. Filters search results to include '
                'only products that are currently in stock.'
            ),
        )
        self.add_argument(
            '-g',
            '--glutenfree',
            action='store_true',
            help=(
                'Gluten-free flag. Filters search results to include '
                'only gluten-free products.'
            ),
        )
        self.add_argument(
            '-v',
            '--vegetarian',
            action='store_true',
            help=(
                'Vegetarian flag. Filters search results to include '
                'only vegetarian products.'
            ),
        )
        self.add_argument(
            '-D',
            '--setdefault',
            action='store_true',
            help=(
                'Set-Default flag. Sets the current query as the default, '
                'i.e., the query that is used when an empty query is submitted.'
            ),
        )
        self.add_argument(
            '-h',
            '--help',
            action='help',
            help='Show this help message.',
        )

    @property
    def optional_args(self) -> List[Tuple[str, str]]:
        optional_args = []
        for action in self._actions:
            if len(action.option_strings) == 2:
                short, full = action.option_strings
            elif len(action.option_strings) == 1:
                arg = action.option_strings[0]
                short, full = arg, arg
            else:  # empty or more than 2 option strings, should not happen
                continue
            optional_args.append((short, full))
        return optional_args

    @staticmethod
    def split_args(args: str) -> List[str]:
        try:
            return shlex.split(args)
        except ValueError:
            try:
                return shlex.split(f'{args}"')
            except ValueError:
                try:
                    return shlex.split(f"{args}'")
                except Exception:  # should not happen
                    return []

    def parse_args(  # type: ignore[override]
        self,
        args: Optional[Sequence[str]] = None,
        namespace: Optional[argparse.Namespace] = None,
    ) -> argparse.Namespace:
        parsed_args = super().parse_args(args=args, namespace=namespace)
        if parsed_args is None:
            raise SystemExit
        parsed_args.name = parsed_args.name or parsed_args.positional_name
        delattr(parsed_args, 'positional_name')
        return parsed_args

    def parse_args_safe(
        self,
        args: Optional[Sequence[str]] = None,
        namespace: Optional[argparse.Namespace] = None,
    ) -> Optional[argparse.Namespace]:
        try:
            return self.parse_args(args, namespace)
        except SystemExit:
            return None


def get_constraints(
    args: argparse.Namespace,
) -> List[Callable[[Product], bool]]:
    constraints: list[Callable[[Product], bool]] = []
    if args.name is not None:
        constraints.append(
            lambda p: format_str(args.name) in p.name_lowercase_ascii
        )
    if args.category is not None:
        constraints.append(
            lambda p: format_str(args.category) in p.category_lowercase_ascii
        )
    if args.quantity_min is not None:
        constraints.append(lambda p: p.quantity >= args.quantity_min)
    if args.quantity_max is not None:
        constraints.append(lambda p: p.quantity <= args.quantity_max)
    if args.price_min is not None:
        constraints.append(lambda p: p.price_curr >= args.price_min)
    if args.price_max is not None:
        constraints.append(lambda p: p.price_curr <= args.price_max)
    if args.available:
        constraints.append(lambda p: p.is_available)
    if args.sale:
        constraints.append(lambda p: p.is_on_sale)
    if args.glutenfree:
        constraints.append(lambda p: p.is_gluten_free)
    if args.vegetarian:
        constraints.append(lambda p: p.is_vegetarian)
    return constraints
