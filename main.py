"""
Expense Tracker
---------------
A simple command-line tool for tracking daily expenses.
Stores everything in a local JSON file, no database needed.

Examples:
    python expense_tracker.py add 45000 food --note "lunch with friends"
    python expense_tracker.py list
    python expense_tracker.py list --category food
    python expense_tracker.py summary
    python expense_tracker.py delete 3
"""

import json
import os
import argparse
from datetime import datetime
from collections import defaultdict

DATA_FILE = "expenses.json"


def load_expenses():
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print("Warning: data file is corrupted, starting fresh.")
            return []


def save_expenses(expenses):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(expenses, f, indent=2, ensure_ascii=False)


def next_id(expenses):
    if not expenses:
        return 1
    return max(e["id"] for e in expenses) + 1


def add_expense(args):
    expenses = load_expenses()

    entry = {
        "id": next_id(expenses),
        "amount": args.amount,
        "category": args.category.lower(),
        "note": args.note or "",
        "date": args.date or datetime.now().strftime("%Y-%m-%d"),
    }

    expenses.append(entry)
    save_expenses(expenses)

    print(f"Added expense #{entry['id']}: {entry['amount']} ({entry['category']})")


def delete_expense(args):
    expenses = load_expenses()
    remaining = [e for e in expenses if e["id"] != args.id]

    if len(remaining) == len(expenses):
        print(f"No expense found with id {args.id}")
        return

    save_expenses(remaining)
    print(f"Deleted expense #{args.id}")


def list_expenses(args):
    expenses = load_expenses()

    if args.category:
        expenses = [e for e in expenses if e["category"] == args.category.lower()]

    if args.month:
        expenses = [e for e in expenses if e["date"].startswith(args.month)]

    if not expenses:
        print("No expenses found.")
        return

    expenses.sort(key=lambda e: e["date"])

    print(f"{'ID':<5}{'Date':<12}{'Category':<15}{'Amount':<12}Note")
    print("-" * 60)

    for e in expenses:
        note = e["note"][:25]
        print(f"{e['id']:<5}{e['date']:<12}{e['category']:<15}{e['amount']:<12}{note}")

    total = sum(e["amount"] for e in expenses)
    print("-" * 60)
    print(f"Total: {total}")


def show_summary(args):
    expenses = load_expenses()

    if not expenses:
        print("No expenses recorded yet.")
        return

    if args.month:
        expenses = [e for e in expenses if e["date"].startswith(args.month)]
        if not expenses:
            print(f"No expenses found for {args.month}")
            return

    by_category = defaultdict(float)
    by_month = defaultdict(float)

    for e in expenses:
        by_category[e["category"]] += e["amount"]
        by_month[e["date"][:7]] += e["amount"]

    total = sum(e["amount"] for e in expenses)

    print("=" * 45)
    print("EXPENSE SUMMARY")
    print("=" * 45)
    print(f"Total spent: {total}")
    print(f"Number of entries: {len(expenses)}")

    print("\nBy category:")
    for category, amount in sorted(by_category.items(), key=lambda x: x[1], reverse=True):
        percentage = (amount / total) * 100
        print(f"  {category:<15}{amount:<12}{percentage:.1f}%")

    if not args.month:
        print("\nBy month:")
        for month, amount in sorted(by_month.items()):
            print(f"  {month:<10}{amount}")

    print("=" * 45)


def build_parser():
    parser = argparse.ArgumentParser(description="A simple CLI expense tracker.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="add a new expense")
    add_parser.add_argument("amount", type=float, help="amount spent")
    add_parser.add_argument("category", help="expense category, e.g. food, transport")
    add_parser.add_argument("--note", help="optional short description")
    add_parser.add_argument("--date", help="date in YYYY-MM-DD format (default: today)")
    add_parser.set_defaults(func=add_expense)

    list_parser = subparsers.add_parser("list", help="list expenses")
    list_parser.add_argument("--category", help="filter by category")
    list_parser.add_argument("--month", help="filter by month, e.g. 2026-08")
    list_parser.set_defaults(func=list_expenses)

    delete_parser = subparsers.add_parser("delete", help="delete an expense by id")
    delete_parser.add_argument("id", type=int, help="id of the expense to delete")
    delete_parser.set_defaults(func=delete_expense)

    summary_parser = subparsers.add_parser("summary", help="show spending summary")
    summary_parser.add_argument("--month", help="limit summary to a specific month")
    summary_parser.set_defaults(func=show_summary)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()