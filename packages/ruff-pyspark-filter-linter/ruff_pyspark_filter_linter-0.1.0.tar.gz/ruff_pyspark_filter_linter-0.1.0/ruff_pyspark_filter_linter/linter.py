import ast
import json
from datetime import datetime
import astunparse
import logging
from ruff_pyspark_filter_linter.log_utils import get_console_handler

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(get_console_handler())
LOGGER.setLevel(logging.INFO)

LOGGER_PREFIX = "Ruff PySpark Filter Linter: "


class DataFrameFilterVisitor(ast.NodeVisitor):
    def __init__(self, required_filters):
        self.errors = []
        self.required_filters = required_filters
        self.dataframe_vars = set()
        self.filtered_vars = set()

    def visit_Assign(self, node):
        LOGGER.debug(f"{LOGGER_PREFIX}visit_Assign ENTERED")
        if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Attribute):
            if node.value.func.attr == 'createDataFrame':
                LOGGER.debug(f"{LOGGER_PREFIX} Found createDataFrame at line {node.lineno}")
                if isinstance(node.targets[0], ast.Name):
                    self.dataframe_vars.add(node.targets[0].id)
                    LOGGER.debug(f"{LOGGER_PREFIX} Added {node.targets[0].id} to dataframe_vars")
            elif node.value.func.attr == 'filter':
                LOGGER.debug(f"{LOGGER_PREFIX} Found filter at line {node.lineno}")
                if isinstance(node.value.func.value, ast.Name) and node.value.func.value.id in self.dataframe_vars:
                    filter_code = astunparse.unparse(node.value)
                    if any(field in filter_code for field in self.required_filters):
                        self.filtered_vars.add(node.targets[0].id)
                        LOGGER.debug(
                            f"{LOGGER_PREFIX} Filtered DataFrame {node.targets[0].id} contains required filter")

        self.generic_visit(node)

    def visit_Module(self, node):
        self.generic_visit(node)
        for var in self.dataframe_vars:
            if var not in self.filtered_vars:
                self.errors.append((0, 0, 'Missing filter'))
                LOGGER.warning(f"{LOGGER_PREFIX} DataFrame {var} is missing required filter")


def add_parent_references(node, parent=None):
    node.parent = parent
    for child in ast.iter_child_nodes(node):
        add_parent_references(child, node)


def check_file(filename, required_filters):
    LOGGER.info(f"{LOGGER_PREFIX} Checking file: {filename}")
    with open(filename, "r") as file:
        tree = ast.parse(file.read())
    add_parent_references(tree)
    visitor = DataFrameFilterVisitor(required_filters)
    visitor.visit(tree)
    return visitor.errors


def create_warning_file(warnings, filename):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    readme_filename = f"README_Rust_{timestamp}.md"
    with open(readme_filename, "w") as file:
        file.write("# PySpark DataFrame Required Filters Warnings\n\n")
        file.write(f"File: {filename}\n\n")
        for lineno, col_offset, func in warnings:
            file.write(f"- Warning: Missing required filter for DataFrame\n")
    LOGGER.info(f"{LOGGER_PREFIX} Warnings written to {readme_filename}")


def lint_files(filenames, config_file="ruff_pyspark_filter_linter.json"):
    LOGGER.info(f"{LOGGER_PREFIX} Loading configuration from {config_file}")
    with open(config_file, "r") as file:
        config = json.load(file)

    required_filters = config.get("required_filters", [])
    if not required_filters:
        LOGGER.error(f"{LOGGER_PREFIX} No required filters specified in the configuration.")
        return

    for filename in filenames:
        warnings = check_file(filename, required_filters)
        if warnings:
            for lineno, col_offset, func in warnings:
                LOGGER.warning(f"{LOGGER_PREFIX} Missing required filter for DataFrame")
            create_warning_file(warnings, filename)
        else:
            LOGGER.info(f"{LOGGER_PREFIX} All DataFrames in {filename} have the required filters.")
