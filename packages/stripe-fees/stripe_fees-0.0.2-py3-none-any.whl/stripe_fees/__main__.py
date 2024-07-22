#!/usr/bin/env python
import argparse
import locale
import sys

bil_per = 0.8       # percentage
cc_per = 2.9       # percentage
cc_fee = 0.3       # dollars
tax_per = 0.5       # percentage
tax_rate = 14.975    # percentage

combined_per = cc_per + bil_per + tax_per
tax_rate_per = tax_rate/100


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog='Stripe Fees Calculator',
        description='Calculate the amount to charge to make a specific amount after taxes and fees.'
    )
    parser.add_argument('-m', '--make', metavar='AMOUNT', type=float,
                        help='The amount you want to make after taxes and fees.', default=None)
    parser.add_argument('-c', '--charge', metavar='AMOUNT', type=float,
                        help='The amount you want to charge the client.', default=None)

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    return parser.parse_args()


def get_amount_to_charge(amount_to_make):
    amount_to_charge = (amount_to_make + cc_fee) / \
        ((1 + tax_rate_per) * (1 - combined_per/100) - tax_rate_per)

    formatted_amount = locale.currency(amount_to_charge, grouping=True)

    print(f'Amount to charge: {formatted_amount}')


def get_amount_made(amount_charged):
    taxes = amount_charged * tax_rate_per
    amount_made = (amount_charged + taxes) * \
        (1 - (bil_per + cc_per + tax_per)/100) - cc_fee - taxes
    
    formatted_amount = locale.currency(amount_made, grouping=True)

    print(f'Amount made: {formatted_amount}')


def main():
    locale.setlocale(locale.LC_ALL, 'en_CA.UTF-8')

    args = parse_arguments()

    if args.make is not None:
        get_amount_to_charge(args.make)
    elif args.charge is not None:
        get_amount_made(args.charge)


if __name__ == '__main__':
    main()
