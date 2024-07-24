"""Main program code"""

import argparse
import datetime
from decimal import Decimal


def valid_date(input_date_str: str) -> datetime.datetime:
    """Date parser used by argparse.ArgumentParser().
    Attempts to parse given date string, otherwise raising an error"""
    try:
        return datetime.datetime.strptime(input_date_str, "%Y-%m-%d").date()
    except ValueError:
        raise argparse.ArgumentTypeError(f"not a valid date: {input_date_str!r}")


def mpd_tpd(
    next_payday: datetime.date,
    money_remaining: Decimal,
    fixed_expenses: Decimal,
    include_today: bool,
) -> tuple[int, Decimal]:
    """Calculates how much money can be spent each day until your next payday, distributing remaining money uniformly (i.e. same spend each day)

    Args:
        next_payday (datetime.date): Date on which you will next be paid
        money_remaining (Decimal): Amount of money remaining (which needs to last you until your next payday)
        fixed_expenses (Decimal): Total pending payments (to be paid before your next payday) which are non-negotiable
        include_today (bool): I still want to spend money today (i.e. it is the beginning of the day)

    Returns:
        tuple[int, Decimal]: Tuple containing (number_of_spending_days_remaining, amount_of_money_can_be_spent_per_day)
    """
    today_date: datetime.date = datetime.date.today()
    if today_date >= next_payday:
        raise ValueError("`next_payday` must be in the future")
    days_til_payday: int = (next_payday - today_date).days
    if not include_today:
        days_til_payday -= 1
    money_can_spend_per_day: Decimal = (
        money_remaining - fixed_expenses
    ) / days_til_payday
    return days_til_payday, money_can_spend_per_day


def format_currency(num: Decimal, output_format: str) -> str:
    """Formats the given decimal number according to the format supplied,
    as well as rounding `num` to 2 decimal places and adding a ,000 separator

    Examples:
        >>> from decimal import Decimal
        >>> format_currency(Decimal("420.69"), output_format="£x")
        '£420.69'
        >>> format_currency(Decimal("420.69"), output_format="x €")
        '420.69 €'
    """
    return output_format.replace("x", str(f"{num:,.2f}"))


def commandline_mpd_tpd():
    """Get user input from command line, pass it to mpd_tpd(), and print user-friendly output"""
    arg_parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""
    +-------------------------------------+
    | Money Per Day 'Til PayDay (mpd-tpd) |
    +-------------------------------------+
    Command-line tool for helping conceptualise how much money is left until payday

    Examples:
        $ mpd-tpd --next_payday '2024-07-24' --money_remaining 100  

        # if you still intend to spend money today, then include flag '--include_today':
        $ mpd-tpd --next_payday '2024-07-24' --money_remaining 99.99 --include_today

        # if you have known compulsory bills which you want pre-removed before doing the calculation, use parameter '--fixed_expenses': 
        $ mpd-tpd --next_payday '2024-08-01' --money_remaining 80000 --fixed_expenses 25000 

        # you can explicitly name your fixed expenses if you want to #
        $ mpd-tpd --next_payday '2024-08-01' --money_remaining 80000 --named_fixed_expenses 'home loan=19500.39,pay off credit card=351.16,netflix=5.41'

        # if you want the numbers formatted with a specific currency, specify the format 
        #   using parameter '--currency_format'
        $ mpd-tpd --next_payday '2024-07-24' --money_remaining 50 --currency_format '£x'
        $ mpd-tpd --next_payday '2024-07-24' --money_remaining 99999 --currency_format 'x GBP'
    """,
    )
    arg_parser.add_argument(
        "-p",
        "--next_payday",
        help="Date on which you will next be paid. Required format is YYYY-MM-DD e.g. 2069-07-24",
        required=True,
        type=valid_date,
    )
    arg_parser.add_argument(
        "-m",
        "--money_remaining",
        help="Amount of money remaining (which needs to last you until your next payday)",
        required=True,
        type=Decimal,
    )
    arg_parser.add_argument(
        "-f",
        "--fixed_expenses",
        help="Total pending payments (to be paid before your next payday) which are non-negotiable",
        type=Decimal,
    )
    arg_parser.add_argument(
        "-n",
        "--named_fixed_expenses",
        help="You can use this instead of --fixed_expenses if you want a verbose breakdown of your fixed expenses",
        type=str,
    )
    arg_parser.add_argument(
        "-c",
        "--currency_format",
        help="Show monetary amounts with a specific currency format. Examples: '$x', 'x €', 'xUSD'",
        default="x",
        type=str,
    )
    arg_parser.add_argument(
        "-t",
        "--include_today",
        help="I still want to spend money today (i.e. it is the beginning of the day)",
        action="store_true",  # set to include_today=True if flag is present
    )
    args = arg_parser.parse_args()

    if args.fixed_expenses and args.named_fixed_expenses:
        raise ValueError(
            "Please specify --fixed_expenses or --named_fixed_expenses, not both"
        )

    if args.named_fixed_expenses:
        args.fixed_expenses = Decimal("0")
        fixed_expenses_summary_string = "-- Summary of Fixed Expenses --"
        for expense in args.named_fixed_expenses.split(","):
            # 'home loan=19500.39,pay off credit card=351.16,netflix=5.41'
            name, amount = expense.split("=")
            name = name.strip()
            amount = Decimal(amount.strip())
            fixed_expenses_summary_string += f'\n * "{name}" {amount:,.2f}'
            args.fixed_expenses += amount
        fixed_expenses_summary_string += f"\n * TOTAL: {args.fixed_expenses:,.2f}"
    else:
        fixed_expenses_summary_string = ""

    if args.fixed_expenses is None:
        args.fixed_expenses = Decimal("0")

    days_til_payday, money_can_spend_per_day = mpd_tpd(
        next_payday=args.next_payday,
        money_remaining=args.money_remaining,
        fixed_expenses=args.fixed_expenses,
        include_today=args.include_today,
    )
    if args.include_today:
        including_today_string = "(including today)"
    else:
        including_today_string = "(excluding today)"
    print(
        f"""
You have {days_til_payday:,} days left {including_today_string} until payday ({args.next_payday.strftime("%A")} {args.next_payday}). 
You have {format_currency(args.money_remaining, args.currency_format)} left to spend and {format_currency(args.fixed_expenses, args.currency_format)} still to pay in fixed expenses before then.
This means that you have {format_currency(args.money_remaining-args.fixed_expenses, args.currency_format)} = ({format_currency(args.money_remaining, args.currency_format)} - {format_currency(args.fixed_expenses, args.currency_format)}) in total to spend until payday.
i.e. you can spend {format_currency(money_can_spend_per_day, args.currency_format)} per day until you will be paid again.
{fixed_expenses_summary_string}
        """
    )


if __name__ == "__main__":
    commandline_mpd_tpd()
