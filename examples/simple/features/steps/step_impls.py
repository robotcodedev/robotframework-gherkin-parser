from typing import Optional

from robot.api.deco import keyword


@keyword(name="before_feature", tags=["hook:before-feature"])
def before_feature(lang: Optional[str] = None):
    print("I'm doing something in lang")
    #raise Exception("I'm failing")


@keyword(name="Do something in ${lang}")
def do_something_in_python(lang: str):
    print(f"I'm doing something in {lang}")
