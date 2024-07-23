from chkw.evaluator import Evaluator
from chkw.tokenizer import Tokenizer
from chkw.transcompiler import TransCompiler


import os
import click


@click.group(invoke_without_command=True)
@click.pass_context
@click.argument('filename', required=False)
@click.option('-trans', 'trans', is_flag=True, help='Process the file with the "trans" action')
def cli(ctx, filename, trans):

    if ctx.invoked_subcommand is None:

        if trans and filename:
            process_trans(filename)
        elif filename:
            process(filename)
        else:
            click.echo('No command specified')

def process(filename):
    with open(filename, "r") as f:
        code = f.read()
    tokenes = Tokenizer(code).tokenize()
    Evaluator(tokenes).eval()

def process_trans(filename):
    click.echo(f'Trans compiling {filename} ...')
    with open(filename, "r") as f:
        code = TransCompiler(f.read()).compile()
    base = os.path.basename(filename)
    name, _ = os.path.splitext(base)
    with open(name + ".chkw", "w") as f:
        f.write(code)

    click.echo(f'Compiled file {name + ".chkw"} is saved')





if __name__ == '__main__':
    cli()



# code = "+++++++++[>++++++++>+++++++++++>+++>+<<<<-]>.>++.+++++++..+++.>+++++.<<+++++++++++++++.>.+++.------.--------.>+.>+."
#
#
# print(TransCompiler(code).compile())
# code = TransCompiler(code).compile()
# tokenes = Tokenizer(code).tokenize()
# Evaluator(tokenes).eval()






