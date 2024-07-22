[//]: # (Copy of the project README.md file)


# FreshPointCLI
Welcome to FreshPointCLI, your go-to REPL tool for querying *my.freshpoint.cz*
product webpages from your terminal.

FreshPointCLI is based on the [FreshPointSync](https://freshpointsync.readthedocs.io)
project.

## Key Features

🔎 **Continuous Querying**. Effortlessly check product availability, prices,
and more without restarting the application.

🆎 **Query Autocompletion**. Enjoy intelligent completion suggestions and
highlighting for query arguments and product data, like names and categories.

📜 **Search History**. Easily access your previous searches and receive
history-based autocompletion suggestions.

💎 **Rich Formatting**. Receive vibrant and visually appealing query responses
with a retro aesthetic, powered by Rich.

## Installation

### Prerequisites

FreshPointCLI requires Python 3.8 or higher. If you don't have Python installed,
you can download it from the [official website](<https://www.python.org/downloads/>).

### FreshPointCLI Installation

Official library releases can be found on
[📦 PyPI](<https://pypi.org/project/freshpointcli/>). To install
the latest stable version of FreshPointCLI, use the following CLI command:

```console
$ pip install freshpointcli --upgrade
```

To install the latest development version directly from the project's
[📁 GitHub repository](https://github.com/mykhakos/FreshPointCLI>), use
the following CLI command:

```console
$ pip install git+https://github.com/mykhakos/FreshPointCLI
```

## Usage

FreshPointCLI focuses on providing an intuitive and responsive command line
interface, following standard CLI conventions.

### Starting Up the Application

Initialize the application using the following CLI command:

```console
$ freshpoint <location_id>
```

`<location_id>` is the ID of the FreshPoint location to track. It can be deduced
from the page URL. For example, for `https://my.freshpoint.cz/device/product-list/296`,
the location ID is *296*.

The location ID is preserved between the application sessions, so if you intend
to track the same location as the last time, you can omit the location ID argument
and invoke the application without providing it.

Invoke the application with `--help` to receive a usage tutorial:

```console
$ freshpoint --help
```

### Querying the Product Page

Once the application is running, it displays an input prompt, and you can type
in queries to check for products' availability, price, and more.

```console
FreshPoint@LocationName> ... <-- submit your query here
```

> **Note**: `LocationName` is a placeholder for an actual location name.

#### Querying for a Single Product

To query for a single product, type in the product name and press `↵ Enter`.
For example, a query for tiramisu would be:

```console
FreshPoint@LocationName> tiramisu 
```

The product name does not need to be an exact match or include diacritics.
FreshPointCLI uses lowercase ASCII partial matching, meaning the formatted query
string must be a part of the complete formatted product name to qualify as a match.
This method applies to any string matching within the application. If there are
several matches, the application will display a list of all corresponding results.

For example, query "`kolac`" would return products such as
"**Koláč** s náplněmi 100 g" or "Pošírovaná krůtí rolka v bylinkách,
polentový **koláč**ek s variací sýrů, zeleninová caponata".

#### Querying with Product Attribute Options

To query for products with specific attributes, use flags and options starting
with a hyphen, such as `--category`, `--available`, or `--price-max <price>`,
and press `↵ Enter`. For example, to query for all available listings in
the category "Dezerty, snídaně" under 80 CZK, use the following command:

```console
FreshPoint@LocationName> --category dezerty --available --price-max 80
```

Each option has a short form, starting with a single hyphen ('`-`'), and a long
form, starting with a double hyphen ('`--`'). They are equivalent. Some options
require a value. For example, the `--price-max <price>` option requires
a non-negative number.

You can get a list of all supported options and their usage instructions by
invoking the `--help` command in a query.

```console
FreshPoint@LocationName> --help
```

#### Using Autocomplete and Query History

Autocomplete suggestions will be displayed as you type. You can use `Tab ↹` or
the `↑` and `↓` arrow keys to navigate through the suggestions.

Before you start typing, you can use `↑` and `↓` arrow keys to navigate through
the history of commands you have executed previously.

#### Setting a Default Query

If you submit an empty query, all the products on the page are returned by default.
You can change this behavior by using the `--setdefault` flag in a query. Once you
submit a query with `--setdefault`, that query will be used as the default whenever
you submit an empty query.

## Contributing

FreshPointCLI is an open-source project in its early development stages. If you
encounter any issues or have suggestions for improvements, please report them on
the [GitHub Issue tracker](https://github.com/mykhakos/FreshPointCLI/issues).

Contributions to FreshPointCLI are also welcome! If you would like
to contribute, please fork the repository, implement your changes, and open
a Pull Request with a detailed description of your work on the
[GitHub Pull Request page](https://github.com/mykhakos/FreshPointCLI/pulls).

## License

FreshPointCLI is distributed under the MIT License.