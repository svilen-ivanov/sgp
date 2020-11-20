import logging
import sys
from logging.config import dictConfig
import copy

from ep2.coin_change import min_coin_change


# dictConfig(dict(
#     version=1,
#     formatters={'f': {'format': '%(asctime)s [%(threadName)s] %(name)-12s %(levelname)-8s %(message)s'}},
#     handlers={'h': {'class': 'logging.StreamHandler', 'formatter': 'f', 'level': logging.DEBUG, 'stream': sys.stdout}},
#     root={'handlers': ['h'], 'level': logging.DEBUG},
# ))


class Frame:
    def __init__(self, rel_line, abs_line, local_vars, file_name):
        self.rel_line = rel_line
        self.file_name = file_name
        self.abs_line = abs_line
        self.local_vars = copy.deepcopy(local_vars)
        self.frame_no = None

    def __str__(self):
        line = f"Frame {self.frame_no}, line {self.rel_line} ({self.file_name}:{self.abs_line})\n"
        for var_name, var_value in self.local_vars.items():
            line += f"    {var_name} = {var_value}\n"
        return line


class CollectedTrace():
    def __init__(self):
        self.frames = []
        self.current_frame = 0

    def append(self, frame):
        frame.frame_no = len(self.frames)
        self.frames.append(frame)

    def step(self, num_step=1):
        last_frame = len(self.frames) - 1
        if self.current_frame == last_frame:
            return None
        if self.current_frame + num_step < last_frame:
            self.current_frame += num_step
        else:
            self.current_frame = last_frame
        return self.current()

    def current(self):
        return self.frames[self.current_frame]

    def at_the_end(self):
        return self.current_frame == len(self.frames) - 1

    def step_to_rel_line(self, rel_line):
        while True:
            current = self.step()
            if current is None:
                return None
            if rel_line == current.rel_line:
                return current

    def step_to_abs_line(self, abs_line):
        while True:
            current = self.step()
            if current is None:
                return None
            if abs_line == current.abs_line:
                return current


class ScriptedInspector():
    DIVIDER = "-" * 78

    def __init__(self, func_to_inspect, args):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
        self.break_at_line = None
        self.func_to_inspect = func_to_inspect
        self.args = args
        self.enabled = True
        self.collected_trace = None

    def collect_trace(self):
        self.collected_trace = CollectedTrace()
        sys.settrace(self.trace_calls)
        self.func_to_inspect(*self.args)
        sys.settrace(None)
        return self.collected_trace

    def trace_calls(self, frame, event, arg):
        if event != 'call':
            return
        co = frame.f_code
        func_name = co.co_name
        if func_name == self.func_to_inspect.__name__:
            rel_line = frame.f_lineno - frame.f_code.co_firstlineno
            frame = Frame(rel_line, frame.f_lineno, frame.f_locals, frame.f_code.co_filename)
            self.trace_start(frame)
            return self.trace_func
        return

    def trace_func(self, frame, event, arg):
        rel_line = frame.f_lineno - frame.f_code.co_firstlineno
        frame = Frame(rel_line, frame.f_lineno, frame.f_locals, frame.f_code.co_filename)
        self.trace_step(frame)
        if event == 'return':
            self.trace_end(frame)
        return

    def trace_start(self, frame):
        self.logger.debug("-- TRACE START --")
        self.logger.debug(f"{frame}")
        self.collected_trace.append(frame)
        self.logger.debug(self.DIVIDER)

    def trace_end(self, frame):
        self.logger.debug("-- TRACE END --")
        self.collected_trace.append(frame)
        self.logger.debug(f"{frame}")
        self.logger.debug(self.DIVIDER)

    def trace_step(self, frame):
        self.logger.debug(f"{frame}")
        self.collected_trace.append(frame)
        self.logger.debug(self.DIVIDER)


if __name__ == '__main__':
    coins = [1, 2, 5]
    amount = 13

    inspector = ScriptedInspector(func_to_inspect=min_coin_change, args=(coins, amount))
    trace = inspector.collect_trace()
    amount_loop_begin = 20
    coin_loop_begin = 24
    while not trace.at_the_end():
        frame = trace.step_to_abs_line(amount_loop_begin)
        print(frame)
        frame = trace.step_to_abs_line(coin_loop_begin)
        print(frame)
