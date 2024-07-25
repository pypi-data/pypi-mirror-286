import libcst as cst
from colorama import Fore, Back, Style
from enum import Enum

VERBOSE = False


def set_verbose(value=True):
    global VERBOSE
    VERBOSE = value


class Usage(Enum):
    SET = 1
    MODIFY = 2
    CALL = 3
    PASS = 4

    def __gt__(self, other):
        return self.value > other.value


def eval_assignment(node, parents):
    if isinstance(parents[node], cst.AugAssign):
        return Usage.MODIFY
    return Usage.SET


def eval_access(node, parents):
    while not isinstance(node, (cst.SimpleStatementLine, cst.BaseCompoundStatement)):
        if isinstance(node, cst.Call):
            return Usage.CALL
        if isinstance(node, cst.Arg):
            return Usage.PASS
        node = parents[node]
    return Usage.PASS


def get_occurrences(source: str | cst.Module | cst.metadata.MetadataWrapper, return_usage = False, return_node = False, only_strongest_usage = False, prepend_name = False, global_scope_only = True):
    flags = [prepend_name, True, return_usage, return_node, not global_scope_only]
    potential_indices = list(range(len(flags)))
    indices = tuple([(potential_indices.pop(0) if flags[i] else None) for i in range(len(flags))])
    name_index, line_index, usage_index, node_index, scope_index = indices
    occurrences = {}

    if isinstance(source, str):
        source = cst.parse_module(source)
    if isinstance(source, cst.Module):
        wrapper = cst.metadata.MetadataWrapper(source)
    else:
        wrapper = source

    ranges = wrapper.resolve(cst.metadata.PositionProvider)
    parents = wrapper.resolve(cst.metadata.ParentNodeProvider)
    scopes = set(wrapper.resolve(cst.metadata.ScopeProvider).values())
    for scope in scopes:
        if global_scope_only and not isinstance(scope, cst.metadata.GlobalScope):
            continue
        for assignment in scope.assignments:
            node = assignment.node
            location = ranges[node].start
            if assignment.name not in occurrences:
                occurrences[assignment.name] = []
            occurrence = (location.line,)
            if prepend_name:
                occurrence = (assignment.name,) + occurrence
            if return_usage:
                occurrence = occurrence + (eval_assignment(node, parents),)
            if return_node :
                occurrence = occurrence + (node,)
            if not global_scope_only:
                occurrence = occurrence + (scope,)
            occurrences[assignment.name].append(occurrence)

        for access in scope.accesses:
            referent_list = list(access.referents)
            if len(referent_list) != 0 and isinstance(referent_list[-1], cst.metadata.BuiltinAssignment):
                continue
            node = access.node
            location = ranges[node].start
            if node.value not in occurrences:
                occurrences[node.value] = []
            occurrence = (location.line,)
            if prepend_name:
                occurrence = (node.value,) + occurrence
            if return_usage:
                occurrence = occurrence + (eval_access(node, parents),)
            if return_node :
                occurrence = occurrence + (node,)
            if not global_scope_only:
                occurrence = occurrence + (scope,)
            occurrences[node.value].append(occurrence)
            #print(f'{access.node.value} @ {location.line} : {[f"{type(parents[ref.node])} @ {ranges[ref.node].start.line}" for ref in access.referents]}')

    for name in occurrences:
        occurrences[name].sort(key=lambda e: e[line_index])
        if only_strongest_usage:
            index = 1
            while index < len(occurrences[name]):
                if occurrences[name][index][line_index] > occurrences[name][index-1][line_index]:
                    index += 1
                else:
                    if usage_index is None or occurrences[name][index][usage_index] > occurrences[name][index-1][usage_index]:
                        occurrences[name].pop(index)
                    else:
                        occurrences[name].pop(index-1)


    return indices, occurrences


class Extractor(cst.CSTTransformer):
    METADATA_DEPENDENCIES = (cst.metadata.PositionProvider, cst.metadata.ScopeProvider, cst.metadata.ParentNodeProvider, cst.metadata.AccessorProvider)
    relevant_statements = []
    keep = []
    name = None
    inputs = []
    outputs = []

    def __init__(self, relevant_statements, name, inputs, outputs):
        self.relevant_statements = relevant_statements
        self.name = name
        self.inputs = inputs
        self.outputs = outputs

    def leave_Module(self, original_node, updated_node):
        function = cst.FunctionDef(
            name=cst.Name(self.name),
            params=cst.Parameters([cst.Param(name=cst.Name(input)) for input in self.inputs]),
            body=cst.IndentedBlock(
                body=tuple(updated_node.body)
                    + (cst.SimpleStatementLine(
                        body=[cst.Return(
                            value=cst.Tuple(elements=[cst.Element(cst.Name(output)) for output in self.outputs])
                        )]
                    ),)
            )
        )

        module = cst.Module([function])
        return module

    def visit_SimpleStatementLine(self, node: cst.Name) -> None:
        if node in self.relevant_statements:
            self.keep.append(node)
            while not isinstance(node, cst.Module):
                node = self.get_metadata(cst.metadata.ParentNodeProvider, node)
                self.keep.append(node)

    def leave_SimpleStatementLine(self, original_node, updated_node):
        if original_node in self.keep:
            return updated_node
        else:
            return cst.RemoveFromParent()

    def visit_ClassDef(self, node: cst.Name) -> None:
        if node in self.relevant_statements:
            self.keep.append(node)
            while not isinstance(node, cst.Module):
                node = self.get_metadata(cst.metadata.ParentNodeProvider, node)
                self.keep.append(node)

    def leave_ClassDef(self, original_node, updated_node):
        if original_node in self.keep:
            return updated_node
        else:
            return cst.RemoveFromParent()

    def visit_FunctionDef(self, node: cst.Name) -> None:
        if node in self.relevant_statements:
            self.keep.append(node)
            while not isinstance(node, cst.Module):
                node = self.get_metadata(cst.metadata.ParentNodeProvider, node)
                self.keep.append(node)

    def leave_FunctionDef(self, original_node, updated_node):
        if original_node in self.keep:
            return updated_node
        else:
            return cst.RemoveFromParent()

    def visit_Try(self, node: cst.Name) -> None:
        if node in self.relevant_statements:
            self.keep.append(node)
            while not isinstance(node, cst.Module):
                node = self.get_metadata(cst.metadata.ParentNodeProvider, node)
                self.keep.append(node)

    def leave_Try(self, original_node, updated_node):
        if original_node in self.keep:
            return updated_node
        else:
            return cst.RemoveFromParent()

    def visit_TryStar(self, node: cst.Name) -> None:
        if node in self.relevant_statements:
            self.keep.append(node)
            while not isinstance(node, cst.Module):
                node = self.get_metadata(cst.metadata.ParentNodeProvider, node)
                self.keep.append(node)

    def leave_TryStar(self, original_node, updated_node):
        if original_node in self.keep:
            return updated_node
        else:
            return cst.RemoveFromParent()

    def visit_If(self, node: cst.Name) -> None:
        if node in self.relevant_statements:
            self.keep.append(node)
            while not isinstance(node, cst.Module):
                node = self.get_metadata(cst.metadata.ParentNodeProvider, node)
                self.keep.append(node)

    def leave_If(self, original_node, updated_node):
        if original_node in self.keep:
            return updated_node
        else:
            return cst.RemoveFromParent()

    def visit_With(self, node: cst.Name) -> None:
        if node in self.relevant_statements:
            self.keep.append(node)
            while not isinstance(node, cst.Module):
                node = self.get_metadata(cst.metadata.ParentNodeProvider, node)
                self.keep.append(node)

    def leave_With(self, original_node, updated_node):
        if original_node in self.keep:
            return updated_node
        else:
            return cst.RemoveFromParent()

    def visit_While(self, node: cst.Name) -> None:
        if node in self.relevant_statements:
            self.keep.append(node)
            while not isinstance(node, cst.Module):
                node = self.get_metadata(cst.metadata.ParentNodeProvider, node)
                self.keep.append(node)

    def leave_While(self, original_node, updated_node):
        if original_node in self.keep:
            return updated_node
        else:
            return cst.RemoveFromParent()

    def visit_For(self, node: cst.Name) -> None:
        if node in self.relevant_statements:
            self.keep.append(node)
            while not isinstance(node, cst.Module):
                node = self.get_metadata(cst.metadata.ParentNodeProvider, node)
                self.keep.append(node)

    def leave_For(self, original_node, updated_node):
        if original_node in self.keep:
            return updated_node
        else:
            return cst.RemoveFromParent()

    def visit_Match(self, node: cst.Name) -> None:
        if node in self.relevant_statements:
            self.keep.append(node)
            while not isinstance(node, cst.Module):
                node = self.get_metadata(cst.metadata.ParentNodeProvider, node)
                self.keep.append(node)

    def leave_Match(self, original_node, updated_node):
        if original_node in self.keep:
            return updated_node
        else:
            return cst.RemoveFromParent()


def extract_function(code, function_name, inputs, outputs, try_optimize=True):
    inputs = set(inputs)
    # Get all occurrences of names defined in the global space
    code_cst = cst.parse_module(code)
    wrapper = cst.metadata.MetadataWrapper(code_cst)
    (name_index, line_index, usage_index, node_index, scope_index), occurrences_by_name = get_occurrences(wrapper, return_usage=True, return_node=True, prepend_name=True, global_scope_only=False)
    # Sort the list of occurrences by line number
    occurrences = []
    for name in occurrences_by_name:
        occurrences.extend(occurrences_by_name[name])

    occurrences.sort(key=lambda occurrence: occurrence[line_index])
    # Add the outputs to the relevant occurrences
    relevant_occurrences = set([occurrence if not try_optimize or occurrence[usage_index] != Usage.PASS
                                else get_previous_occurrence(occurrences_by_name, occurrence,
                                                             name_index, usage_index, try_optimize)
                                for occurrence in occurrences if occurrence[:2] in outputs])
    relevant_statements = set()
    # Get accessor for parent nodes
    parents = wrapper.resolve(cst.metadata.ParentNodeProvider)
    # Get accessor for a position information
    ranges = wrapper.resolve(cst.metadata.PositionProvider)
    # Until relevant occurrences stop growing:
    proccessed_relevant_occurrences = set()
    proccessed_relevant_statements = set()
    step = 0
    while len(relevant_occurrences - proccessed_relevant_occurrences) > 0:
        if VERBOSE:
            print(f'Step: {Fore.LIGHTMAGENTA_EX}{step}{Fore.RESET}\nRelevant Occurrances: {Fore.LIGHTBLUE_EX}{[o[:3] for o in relevant_occurrences - proccessed_relevant_occurrences]}{Fore.RESET}')
        # For each relevant occurrence get the related line statement and add them to the relevant statements
        for occurrence in relevant_occurrences - proccessed_relevant_occurrences:
            node = get_statement(occurrence[node_index], parents)
            if node not in relevant_statements:
                relevant_statements.add(node)

            if isinstance(node, cst.Module):
                print(f'{Fore.RED}Module was reached for:{Fore.RESET} {occurrence[:node_index] + (type(occurrence[node_index]),)}')

        proccessed_relevant_occurrences.update(relevant_occurrences)

        if VERBOSE:
            print(f'Relevant Statments: {Fore.LIGHTBLACK_EX}{[(ranges[s].start.line, "to", ranges[s].end.line) for s in relevant_statements - proccessed_relevant_statements]}{Fore.RESET}')
        # For each relevant statement:
        for statement in relevant_statements - proccessed_relevant_statements:
            # Get all contained occurrences
            contained_occurrences = set()
            statment_range = ranges[statement];
            for occurrence in occurrences:
                if occurrence[line_index] < statment_range.start.line:
                    continue
                elif occurrence[line_index] > statment_range.end.line:
                    break

                occurrence_range = ranges[occurrence[node_index]]
                if occurrence_range.start.line == statment_range.start.line and occurrence_range.start.column >= statment_range.start.column \
                        or occurrence_range.start.line > statment_range.start.line and occurrence_range.end.line < statment_range.end.line \
                    or occurrence_range.end.line == statment_range.end.line and occurrence_range.end.column <= statment_range.end.column:
                    contained_occurrences.add(occurrence)

            # For each contained occurrence:
            new_relevant_occurrences = set()
            new_inputs = set()
            for contained_occurrence in contained_occurrences:
                # Check if the contained occurrence is contained in inputs or the occurrence is of usage type set + global -> if not:
                if contained_occurrence[:2] not in inputs and not (contained_occurrence[usage_index] == Usage.SET and isinstance(parents[statement], cst.Module)):
                    # Get the most recent previous occurrence and add it to the relevant occurrences
                    occurrence = get_previous_occurrence(occurrences_by_name, contained_occurrence, name_index,
                                                         usage_index, try_optimize)

                    if occurrence is not None:
                        if occurrence[:2] not in inputs:
                            new_relevant_occurrences.add(occurrence)
                    else:
                        new_inputs.add((contained_occurrence[name_index], 0))

            if VERBOSE:
                print(f'From: {Fore.LIGHTBLUE_EX}{[o[:2] for o in contained_occurrences if o in relevant_occurrences]}{Fore.RESET}\nAdd: {Fore.CYAN}{[o[:2] for o in new_relevant_occurrences]}{Fore.RESET}')

            relevant_occurrences.update(new_relevant_occurrences)
            inputs.update(new_inputs)

        proccessed_relevant_statements.update(relevant_statements)

        step += 1

    # Make bodies of relevant functions and classes relevant
    for occurrence in occurrences:
        if not isinstance(occurrence[scope_index], cst.metadata.GlobalScope):
            node = get_statement(occurrence[node_index], parents, outermost=True)
            if node in relevant_statements:
                relevant_statements.add(get_statement(occurrence[node_index], parents))


    extracted = wrapper.visit(Extractor(relevant_statements, function_name, [input[name_index] for input in inputs], [output[name_index] for output in outputs]))

    return inputs, extracted.code


def get_previous_occurrence(occurrences_by_name, occurrence, name_index, usage_index, try_optimize):
    previous_occurrence = None
    for occurrence_2 in occurrences_by_name[occurrence[name_index]]:
        if occurrence_2 == occurrence:
            break
        else:
            if try_optimize and occurrence_2[usage_index] == Usage.PASS:
                continue
            previous_occurrence = occurrence_2
    return previous_occurrence


def get_statement(node, parents, outermost = False):
    ret = None
    while not isinstance(node, cst.Module):
        if isinstance(node, (cst.SimpleStatementLine, cst.BaseCompoundStatement)):
            ret = node
            if not outermost:
                break
        node = parents[node]
    return ret

