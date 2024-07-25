#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  Lijiawei
@Date    :  2024/5/10 7:29 PM
@Desc    :  modifybody line.
"""
import re
import typing

from mitmproxy import ctx, exceptions
from mitmproxy.addons.modifyheaders import parse_modify_spec, ModifySpec


class ModifyBodys:
    """
    https://docs.mitmproxy.org/dev/overview-features/#modify-body
    request: |~u url & ~s|.*|replacement
    response: |~u url & ~q|.*|replacement
    """
    def __init__(self):
        self.replacements: typing.List[ModifySpec] = []

    def load(self, loader):
        loader.add_option(
            "modify_bodys", typing.Sequence[str], [],
            """
            使用"|flow-filter|regex|[@]replacement-json"形式的替换模式，@允许提供用于读取替换字符串的文件路径，其中分隔符是|。
            """
        )

    def configure(self, updated):
        if "modify_bodys" in updated:
            self.replacements = []
            for option in ctx.options.modify_body:
                try:
                    spec = parse_modify_spec(option, True)
                except ValueError as e:
                    raise exceptions.OptionsError(f"Cannot parse modify_body option {option}: {e}") from e

                self.replacements.append(spec)

    def request(self, flow):
        if flow.response or flow.error or not flow.live:
            return
        self.run(flow)

    def response(self, flow):
        if flow.error or not flow.live:
            return
        self.run(flow)

    def run(self, flow):
        for spec in self.replacements:
            if spec.matches(flow):
                try:
                    replacement = spec.read_replacement()
                except OSError as e:
                    ctx.log.warn(f"Could not read replacement file: {e}")
                    continue
                if flow.response:
                    flow.response.content = re.sub(spec.subject, replacement, flow.response.content, flags=re.DOTALL)
                else:
                    flow.request.content = re.sub(spec.subject, replacement, flow.request.content, flags=re.DOTALL)
