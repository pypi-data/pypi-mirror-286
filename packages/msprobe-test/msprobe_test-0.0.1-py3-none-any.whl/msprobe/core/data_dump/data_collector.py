
import os

from msprobe.core.data_dump.scope import  build_scope, ListScope
from msprobe.core.data_dump.json_writer import DataWriter
from msprobe.core.common.log import logger
from msprobe.core.common.const import Const
from msprobe.core.data_dump.data_processor.factory import DataProcessorFactory


def build_data_collector(config):
    return DataCollector(config)


class DataCollector:
    multi_output_apis = ["_sort_", "npu_flash_attention"]
    tasks_need_tensor_data = [Const.OVERFLOW_CHECK, Const.TENSOR, Const.FREE_BENCHMARK]
    level_without_construct = ["L1", "L2"]

    def __init__(self, config):
        self.config = config
        self.data_writer = DataWriter()
        self.data_processor = DataProcessorFactory.create_processor(self.config, self.data_writer)
        self.module_processor = DataProcessorFactory.get_module_processor(self.config.framework) if self.config.framework == Const.PT_FRAMEWORK else None
        self.module_count = {}
        if self.config.task == Const.FREE_BENCHMARK:
            self.scope = build_scope(ListScope, self.config.scope, self.config.list)
        else:
            self.scope = build_scope(None, self.config.scope, self.config.list)

    @property
    def dump_data_dir(self):
        return self.data_writer.dump_tensor_data_dir

    @property
    def dump_file_path(self):
        return self.data_writer.dump_file_path
    
    @staticmethod
    def check_scope_and_pid(scope, name, pid):
        return (not scope or scope.check(name)) and pid == os.getpid()

    @staticmethod
    def is_inplace(module):
        return getattr(module, "op_is_inplace", False)
    
    def if_return_forward_new_output(self):
        return self.data_processor.if_return_forward_new_output()
    
    def get_forward_new_output(self):
        return self.data_processor.get_forward_new_output()

    def visit_and_clear_overflow_status(self, api_or_module_name):
        self.data_processor.visit_and_clear_overflow_status(api_or_module_name)

    def write_json(self):
        self.data_writer.write_json()

    def update_data(self, data_info, msg=''):
        if self.config.task == Const.OVERFLOW_CHECK:
            if self.data_processor.has_overflow:
                self.data_writer.update_data(data_info)
                msg += "Overflow detected."
            else:
                msg += "No Overflow, OK."
        else:
            self.data_writer.update_data(data_info)
        return msg

    def pre_forward_data_collect(self, name, module, pid, module_input_output):
        backward_name = name.replace(Const.FORWARD, Const.BACKWARD)
        if self.check_scope_and_pid(self.scope, backward_name, pid):
            self.data_processor.analyze_pre_forward(backward_name, module, module_input_output)
        if not self.is_inplace(module):
            return
        logger.info(f"API {name} is inplace.")
        if self.check_scope_and_pid(self.scope, name, pid):
            data_info = self.data_processor.analyze_pre_forward_inplace(name, module_input_output)
            self.update_data(data_info)

    def forward_data_collect(self, name, module, pid, module_input_output):
        self.update_construct(name)
        if not self.check_scope_and_pid(self.scope, name, pid):
            return

        if not self.is_inplace(module):
            data_info = self.data_processor.analyze_forward(name, module, module_input_output)
        else:
            data_info = self.data_processor.analyze_forward_inplace(name, module_input_output)
        if self.config.level == "L2":
            return 
        self.data_writer.update_stack(self.data_processor.analyze_api_call_stack(name))
        self.handle_data(name, data_info)

    def backward_data_collect(self, name, module, pid, module_input_output):
        self.update_construct(name)
        if not self.check_scope_and_pid(self.scope, name, pid):
            return

        data_info = self.data_processor.analyze_backward(name, module, module_input_output)
        self.handle_data(name, data_info)

    def update_construct(self, name):
        if self.config.level not in DataCollector.level_without_construct:
            self.data_writer.update_construct({name: self.module_processor.api_parent_node})
            self.data_writer.update_construct(self.module_processor.module_node)

    def handle_data(self, name, data_info):
        msg = f"msProbe is collecting data on {name}. "
        if data_info:
            msg = self.update_data(data_info, msg)
            logger.info(msg)
        self.data_writer.flush_data_when_buffer_is_full()

    def module_count_func(self, name, name_template):
        module_name = name.split(Const.SEP)[-3]
        if "forward" in name_template:
            if module_name not in self.module_count:
                self.module_count[module_name] = [0, [0]]
            else:
                if self.module_count[module_name][-1] and \
                        self.module_count[module_name][0] != self.module_count[module_name][-1][-1]:
                    self.module_count[module_name][-1].pop()
                self.module_count[module_name][0] += 1
                self.module_count[module_name][-1].append(self.module_count[module_name][0])
            index = self.module_count[module_name][0]
        else:
            backward_stack = self.module_count[module_name][-1] if module_name in self.module_count else []
            if not backward_stack:
                index = "abnormal"
            else:
                index = backward_stack.pop()
        return index

    def update_dump_paths(self, *args):
        self.data_writer.update_dump_paths(*args)
        self.data_writer.initialize_json_file(task=self.config.task, level=self.config.level)
    
    def update_iter(self, current_iter):
        self.data_processor.update_iter(current_iter)
