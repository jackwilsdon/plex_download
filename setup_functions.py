import io as _io
import ast as _ast


def get_file_content(filename):
    with _io.open(filename, 'r') as file_stream:
        return file_stream.read()


def get_assignment_value(source, target, as_path=False):
    if as_path:
        source = get_file_content(source)

    root_node = _ast.parse(source)

    for node in root_node.body:
        if isinstance(node, _ast.Assign) and \
                any(expression.id == target for expression in node.targets):
            return _ast.literal_eval(node.value)


__all__ = ('get_file_content', 'get_assignment_value',)
