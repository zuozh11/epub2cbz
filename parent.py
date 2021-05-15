"""
    Public dependence
"""

from rich.console import Console
from rich.progress import Progress, TextColumn, BarColumn, TimeRemainingColumn, \
    SpinnerColumn, TimeElapsedColumn
from rich.traceback import install

install()
console = Console()
progress = Progress(
    SpinnerColumn(speed=1.5, finished_text='✔'),
    TextColumn("[bold blue]{task.description}", justify="right"),
    BarColumn(bar_width=40),
    "[progress.percentage]{task.percentage:>3.1f}%",
    "•",
    TimeRemainingColumn(),
    TimeElapsedColumn(),
    refresh_per_second=50,
    console=console
)

help_text = """
    [bold]epub file convert to a cbz file or any zip-like file[/bold]
    
    [bold blue]Usage:[/bold blue] python epub2cbz.py [-options] path
    
    [bold blue]Note:[/bold blue] path can be epubfile path or dir path
    
    [bold blue]The options include:[/bold blue]
      -h --help                    show this help
      -r --rotate                  correct orientation
      -s: --suffix: <value>        specify the output file suffix, default is .cbz
      --folder                     output to a folder instead of the compressed file
"""
