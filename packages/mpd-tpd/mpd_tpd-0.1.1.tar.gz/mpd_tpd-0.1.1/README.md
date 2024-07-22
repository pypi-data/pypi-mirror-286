# Money Per Day 'Til PayDay (mpd-tpd)

Python command-line tool for helping conceptualise how much money is left until payday

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

```bash
$ mpd-tpd --help

usage: mpd-tpd [-h] -p NEXT_PAYDAY -m MONEY_REMAINING [-f FIXED_EXPENSES] [-c CURRENCY_FORMAT] [-t]

    +-------------------------------------+
    | Money Per Day 'Til PayDay (mpd-tpd) |
    +-------------------------------------+
    Command-line tool for helping conceptualise how much money is left until payday

    Examples:
        $ mpd-tpd --next_payday '2024-07-24' --money_remaining 100

        # if you still intend to spend money today, then include flag '--include_today':
        $ mpd-tpd --next_payday '2024-07-24' --money_remaining 99.99 --include_today

        # if you have known bills which you want pre-removed before doing the calculation,
        #   use parameter '--fixed_expenses':
        $ mpd-tpd --next_payday '2024-08-01' --money_remaining 80000 --fixed_expenses 25000

        # if you want the numbers formatted with a specific currency, specify the format
        #   using parameter '--currency_format'
        $ mpd-tpd --next_payday '2024-07-24' --money_remaining 50 --currency_format '£x'
        $ mpd-tpd --next_payday '2024-07-24' --money_remaining 99999 --currency_format 'x GBP'
```
