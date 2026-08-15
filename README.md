# Expense Tracker

A simple command-line tool for tracking daily expenses. Expenses are stored locally in a JSON file, with no database or external service required.

## Table of Contents

- [Features](#features)
- [Preview](#preview)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Commands](#commands)
- [Examples](#examples)
- [Data Storage](#data-storage)
- [How It Works](#how-it-works)
- [Limitations](#limitations)
- [Roadmap](#roadmap)
- [License](#license)

## Features

- Add expenses with an amount, category, optional note, and date
- List expenses, with optional filtering by category or month
- View a spending summary broken down by category and by month
- Delete an expense by its id
- All data persisted locally in a human-readable JSON file
- Built entirely on Python's standard library, no external dependencies required

## Preview

```
$ python main.py summary
=============================================
EXPENSE SUMMARY
=============================================
Total spent: 195000.0
Number of entries: 3

By category:
  transport      120000.0    61.5%
  food           75000.0     38.5%

By month:
  2026-07   30000.0
  2026-08   165000.0
=============================================
```

## Requirements

- Python 3.7 or newer
- No third-party packages are required; the script relies only on modules included in the Python standard library (`json`, `argparse`, `datetime`, `collections`).

## Installation

Clone the repository:

```bash
git clone https://github.com/<HoneySpider>/<ExpenseTracker>.git
cd <ExpenseTracker>
```

No further installation steps are needed since the script has no external dependencies.

## Usage

The tool is command-based: running the script without a command shows the help message instead of doing anything, since it needs to know which action to perform.

```bash
python main.py <command> [options]
```

To see all available commands and their options at any time:

```bash
python main.py -h
python main.py <command> -h
```

## Commands

| Command | Description |
|---------|-------------|
| `add` | Add a new expense |
| `list` | List recorded expenses, optionally filtered |
| `delete` | Delete an expense by its id |
| `summary` | Show a spending summary |

### add

| Argument | Description | Required |
|----------|-------------|----------|
| `amount` | Amount spent (positional) | Yes |
| `category` | Expense category, e.g. `food`, `transport` (positional) | Yes |
| `--note` | Short description of the expense | No |
| `--date` | Date in `YYYY-MM-DD` format | No (defaults to today) |

### list

| Argument | Description | Required |
|----------|-------------|----------|
| `--category` | Filter results by category | No |
| `--month` | Filter results by month, e.g. `2026-08` | No |

### delete

| Argument | Description | Required |
|----------|-------------|----------|
| `id` | Id of the expense to delete (positional) | Yes |

### summary

| Argument | Description | Required |
|----------|-------------|----------|
| `--month` | Limit the summary to a specific month, e.g. `2026-08` | No |

## Examples

Add a new expense:

```bash
python main.py add 45000 food --note "lunch with friends"
```

Add an expense with a specific date:

```bash
python main.py add 30000 food --date 2026-07-15
```

List all expenses:

```bash
python main.py list
```

List expenses in a specific category:

```bash
python main.py list --category food
```

List expenses from a specific month:

```bash
python main.py list --month 2026-08
```

Show an overall spending summary:

```bash
python main.py summary
```

Show a summary limited to one month:

```bash
python main.py summary --month 2026-08
```

Delete an expense by id:

```bash
python main.py delete 3
```

## Data Storage

All expenses are stored in `expenses.json`, created automatically in the same directory as the script on first use. Each entry contains an id, amount, category, optional note, and date. Since the file is plain JSON, it can be opened, edited, backed up, or version-controlled directly if needed.

## How It Works

1. **Command parsing** — `argparse` subparsers are used to expose `add`, `list`, `delete`, and `summary` as distinct commands, each with its own arguments and validation.
2. **Loading data** — On every run, expenses are loaded from `expenses.json`. If the file does not exist yet, an empty list is used; if the file is corrupted, the script warns the user and starts fresh instead of crashing.
3. **Adding an expense** — A new entry is built with an auto-incremented id (one higher than the current maximum), the given amount and category, an optional note, and either the provided date or today's date.
4. **Listing and filtering** — Expenses can be filtered by category or by month (matched against the start of the date string) before being sorted chronologically and printed in a table.
5. **Summary calculation** — Using `collections.defaultdict`, the script aggregates total spending by category and by month, then prints each category's share of the total as a percentage.
6. **Deleting an expense** — The expense list is rebuilt excluding the given id; if no entry matches, the user is informed instead of the file being silently rewritten.
7. **Saving data** — After any change, the full expense list is written back to `expenses.json` with indentation for readability.

## Limitations

- Designed for single-user, local use; there is no support for multiple concurrent users or devices.
- No currency conversion or multi-currency support; amounts are stored as plain numbers.
- Category names are case-insensitive but not validated against a fixed list, so typos can create duplicate categories (e.g. `food` vs `foods`).
- No built-in editing of existing entries; an expense must be deleted and re-added to correct a mistake.
- Filtering by month relies on the date being stored in `YYYY-MM-DD` format.

## Roadmap

Potential future improvements include:

- An `edit` command to modify existing expenses without deleting them
- Support for setting and tracking monthly budgets per category
- Export of summaries to CSV for use in spreadsheets
- An interactive menu mode for users who prefer not to use command-line flags
- Basic data visualization, such as a bar chart of spending by category

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
