import click

from templatepy.fib import fib


@click.command()
@click.argument("n", type=int)
def main(n: int):
    print(fib(n))


if __name__ == "__main__":
    main()
