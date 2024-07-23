from termcolor import colored

def print_tree(node, source_code, indent=0):
    indent_str = " " * indent
    formatted_node = (
        f"{colored(node.type, 'yellow')} "
        f"[grammar_name='{colored(node.grammar_name, 'blue')}', "
        f"grammar_id='{colored(str(node.grammar_id), 'green')}', "
        f"named='{colored(str(node.is_named), 'cyan')}', "
        f"extra='{colored(str(node.is_extra), 'magenta')}'] "
        f"{colored(str(node.start_point), 'red')} - {colored(str(node.end_point), 'red')}"
    )

    print(f"{indent_str}{formatted_node}")

    for child in node.children:
        print_tree(child, source_code, indent + 2)
