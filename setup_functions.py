from __future__ import absolute_import

import ast
import io


def get_file_content(filename):
    with io.open(filename, 'r') as file_stream:
        return file_stream.read()


def get_assignment_value(source, target, as_path=False):
    if as_path:
        source = get_file_content(source)

    root_node = ast.parse(source)

    for node in root_node.body:
        if isinstance(node, ast.Assign) and \
                any(expression.id == target for expression in node.targets):
            return ast.literal_eval(node.value)


__all__ = ('get_file_content', 'get_assignment_value',)
