from termcolor import colored

def get_node_types(language):
    return [language.node_kind_for_id(i) for i in range(language.node_kind_count)]

def print_node(node, source_code, node_types):
    node_kind_id = node.kind_id
    node_type = node_types[node_kind_id]
    node_text = source_code[node.start_byte:node.end_byte]
    
    print(f"{node_type}: {colored(node_text, 'green')}")

    for child in node.children:
        print_node(child, source_code, node_types)

def print_node_type_mapping(language):
    for i in range(language.node_kind_count):
        node_type = language.node_kind_for_id(i)
        is_named = language.node_kind_is_named(i)
        is_visible = language.node_kind_is_visible(i)
        is_hidden = node_type.startswith('_')
        
        print(f"{i}: kind={colored(node_type, 'green')}, named={is_named}, hidden={is_hidden}, visible={is_visible}")
