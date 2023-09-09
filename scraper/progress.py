import sys


class Progress:
    def __init__(self, current, total) -> None:
        self.current = current
        self.total = total
        pass

    def print_progress(self, current) -> None:
        self.current = current
        progress = current / self.total
        bar_length = 40
        progress_bar = (
            "["
            + "=" * int(bar_length * progress)
            + "-" * (bar_length - int(bar_length * progress))
            + "]"
        )
        sys.stdout.write(
            "\rProgress: [{:<40}] {:.2%} {} of {}".format(
                progress_bar, progress, current, self.total
            )
        )
        sys.stdout.flush()
