from itertools import chain
from typing import Any, Iterator, List, Tuple, Union

from robot import result, running
from robot.api.deco import keyword, library
from robot.api.interfaces import ListenerV3
from robot.libraries.BuiltIn import EXECUTION_CONTEXTS, BuiltIn
from robot.model import Keyword


@library(
    scope="SUITE",
    version="1.0.0",
)
class Library(ListenerV3):

    def __init__(self) -> None:
        self.ROBOT_LIBRARY_LISTENER = self
        self._in_call_hooks = False

    def call_hooks(self, events: Union[str, Tuple[str, ...]], *args: Any, **kwargs: Any) -> None:
        if self._in_call_hooks:
            return

        errored = False
        self._in_call_hooks = False
        try:
            if isinstance(events, str):
                events = (events,)
            ctx = EXECUTION_CONTEXTS.current
            for name, keyword in chain(
                *([(v.name, l) for l in v.keywords] for v in ctx.namespace._kw_store.resources.values()),
                *([(v.name, l) for l in v.keywords] for v in ctx.namespace._kw_store.libraries.values()),
            ):
                hook_tags = [tag for tag in keyword.tags if tag.startswith(self.prefix)]
                for tag in hook_tags:
                    if tag[len(self.prefix) :] in events:
                        runner = EXECUTION_CONTEXTS.current.get_runner(name + "." + keyword.name)
                        if runner.keyword is keyword:
                            try:
                                BuiltIn().run_keyword(name + "." + keyword.name, *args, **kwargs)
                            except Exception as e:
                                print(e)
                                errored = True
                                raise e
                            finally:
                                break
                if errored:
                    break
        finally:
            self._in_call_hooks = False

    def yield_hooks(self, events: Union[str, Tuple[str, ...]], *args: Any, **kwargs: Any) -> Iterator[str]:
        if isinstance(events, str):
            events = (events,)
        ctx = EXECUTION_CONTEXTS.current
        for name, kw in chain(
            *([(v.name, l) for l in v.keywords] for v in ctx.namespace._kw_store.resources.values()),
            *([(v.name, l) for l in v.keywords] for v in ctx.namespace._kw_store.libraries.values()),
        ):
            hook_tags = [tag for tag in kw.tags if tag.startswith(self.prefix)]
            for tag in hook_tags:
                if tag[len(self.prefix) :] in events:
                    full_name = name + "." + kw.name
                    runner = EXECUTION_CONTEXTS.current.get_runner(full_name)
                    if runner.keyword is kw:
                        yield name + "." + kw.name

    prefix = "hook:"

    def _create_setup_and_teardown(
        self, data: Union[running.TestSuite, running.TestCase], events: Union[str, Tuple[str, ...]]
    ) -> None:
        if isinstance(events, str):
            events = (events,)

        kws: List[str] = []

        for name in self.yield_hooks(events):
            if kws:
                kws.append("AND")
            kws.append(name)

        if kws:
            if data.setup.name:
                data.setup.config(
                    name="BuiltIn.Run Keywords",
                    args=(*kws, "AND", data.setup.name, *data.setup.args),
                )

            else:
                data.setup.config(
                    name="BuiltIn.Run Keywords",
                    args=(*kws,),
                )

        kws = []

        for name in self.yield_hooks(events):
            if kws:
                kws.append("AND")
            kws.append(name)

        if kws:
            if data.teardown.name:
                data.setup.config(
                    name="BuiltIn.Run Keywords",
                    args=(*kws, "AND", data.teardown.name, *data.teardown.args),
                )

            else:
                data.teardown.config(
                    name="BuiltIn.Run Keywords",
                    args=(*kws,),
                )

    def start_suite(self, data: running.TestSuite, result: result.TestSuite) -> None:
        self._create_setup_and_teardown(data, ("before-suite", "before-feature"))

    def start_test(self, data: running.TestCase, result: result.TestCase) -> None:
        self._create_setup_and_teardown(data, ("before-test", "before-test"))

    # def start_keyword(self, data: running.Keyword, result: result.Keyword) -> None:
    #     # self.call_hooks(("before-keyword", "before-step"))
    #     pass

    # def end_keyword(self, data: running.Keyword, result: result.Keyword) -> None:
    #     # self.call_hooks(("after-keyword", "after-step"))
    #     pass
