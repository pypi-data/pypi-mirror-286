import argparse
import os
from tree_sitter import Language, Parser

from .node_map import get_node_types, print_node, print_node_type_mapping
from .node_printer import print_tree

def guess_language(file_path):
    _, extension = os.path.splitext(file_path)
    extension = extension.lstrip('.')
    
    if extension == 'rs':
        import tree_sitter_rust as tsrust
        return Language(tsrust.language())
    elif extension == 'py':
        import tree_sitter_python as tspython
        return Language(tspython.language())
    else:
        raise ValueError(f"Unsupported file extension: {extension}")

def main():
    parser = argparse.ArgumentParser(description="Syntax tree printer utility")
    parser.add_argument("file_path", help="Path to the source code file")
    parser.add_argument("--highlight", action="store_true", help="Print syntax tree with highlighting")
    parser.add_argument("--list-ids", action="store_true", help="List all node IDs and their corresponding names")
    
    args = parser.parse_args()

    try:
        language = guess_language(args.file_path)
    except ValueError as e:
        print(str(e))
        return

    if args.list_ids:
        print_node_type_mapping(language)
        return

    with open(args.file_path, 'r') as file:
        source_code = file.read()

    parser = Parser()
    parser.set_language(language)

    tree = parser.parse(bytes(source_code, "utf8"))
    root_node = tree.root_node

    if args.highlight:
        node_types = get_node_types(language)
        print_node(root_node, source_code, node_types)
    else:
        print_tree(root_node, source_code, 0)
