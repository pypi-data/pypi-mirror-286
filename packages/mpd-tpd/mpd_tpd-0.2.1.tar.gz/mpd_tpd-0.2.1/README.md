# Money Per Day 'Til PayDay (mpd-tpd)

Python command-line tool for helping conceptualise how much money is left until payday

[![Downloads](https://static.pepy.tech/badge/mpd-tpd)](https://pepy.tech/project/mpd-tpd)

```bash
pip install mpd-tpd
```

```bash
mpd-tpd --next_payday '2024-07-31' \
  --money_remaining '2806.45' \
  --fixed_expenses '1269.00' \
  --currency_format '£x'

You have 9 days left (excluding today) until payday (Wednesday 2024-07-31).
You have £2,806.45 left to spend and £1,269.00 still to pay in fixed expenses before then.
This means that you have £1,537.45 = (£2,806.45 - £1,269.00) in total to spend until payday.
i.e. you can spend £170.83 per day until you will be paid again.
```

Home Page: <https://github.com/J-sephB-lt-n/mpd-tpd>

```bash
$ mpd-tpd --help

usage: cli.py [-h] -p NEXT_PAYDAY -m MONEY_REMAINING [-f FIXED_EXPENSES] [-n NAMED_FIXED_EXPENSES] [-c CURRENCY_FORMAT] [-t]

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


options:
  -h, --help            show this help message and exit
  -p NEXT_PAYDAY, --next_payday NEXT_PAYDAY
                        Date on which you will next be paid. Required format is YYYY-MM-DD e.g. 2069-07-24
  -m MONEY_REMAINING, --money_remaining MONEY_REMAINING
                        Amount of money remaining (which needs to last you until your next payday)
  -f FIXED_EXPENSES, --fixed_expenses FIXED_EXPENSES
                        Total pending payments (to be paid before your next payday) which are non-negotiable
  -n NAMED_FIXED_EXPENSES, --named_fixed_expenses NAMED_FIXED_EXPENSES
                        You can use this instead of --fixed_expenses if you want a verbose breakdown of your fixed expenses
  -c CURRENCY_FORMAT, --currency_format CURRENCY_FORMAT
                        Show monetary amounts with a specific currency format. Examples: '$x', 'x €', 'xUSD'
  -t, --include_today   I still want to spend money today (i.e. it is the beginning of the day)
```
