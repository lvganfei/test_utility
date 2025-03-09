import click
import sys

try:
    from press.plaform_test_press import run_press
    from press.calculate import calculate_alg
    from press.assertion import products_assert
except Exception as e:
    print(e)
    if sys.platform == 'linux':
        sys.path.append('./')
        sys.path.append('../')
        from press.plaform_test_press import run_press
        from press.calculate import calculate_alg
        from press.assertion import products_assert


@click.group()
def cli():
    pass


@cli.command()
def run_products_press():
    run_press('products')


@cli.command()
def get_calculate_alg():
    calculate_alg()


@cli.command()
def get_products_logs():
    products_assert()


@cli.command()
def task_top_info():
    from press.background_schedular import run
    run()


@cli.command()
def get_badcase_info():
    from press.coronary.get_badcase_info import run
    run()


if __name__ == '__main__':
    cli()

