import Variables

class Condition(object):
    _negate: bool

    def __init__(self) -> None:
        super().__init__()

    def _evaluate_impl(self, cmd_context) -> bool:
        return

    def evaluate(self, cmd_context) -> bool:
        value = self._evaluate_impl(cmd_context)

        if self._negate:
            return not value
        else:
            return value

class Equals(Condition):
    _left_operand: str
    _right_operand: str

    def __init__(self, left_operand: str = "", right_operand: str = "", negate: bool = False) -> None:
        self._left_operand = left_operand
        self._right_operand = right_operand
        self._negate = negate

        super().__init__()

    def _evaluate_impl(self, cmd_context) -> bool:
        left_value = Variables.replace_tags_in_string(self._left_operand, cmd_context)
        right_value = Variables.replace_tags_in_string(self._right_operand, cmd_context)
        return left_value == right_value

class ConditionSet(object):
    _conditions: list[Condition]

    def __init__(self, conditions: list[Condition] = []) -> None:
        self._conditions = conditions

        super().__init__()

    def evaluate(self, cmd_context) -> bool:
        all_true = True
        for condition in self._conditions:
            if not condition.evaluate(cmd_context):
                all_true = False
                break

        return all_true

class ConditionEvaluator(object):
    _condition_sets: list[ConditionSet]

    def evaluate(self, cmd_context) -> bool:
        if len(self._condition_sets) == 0:
            return False

        value = False
        for condition_set in self._condition_sets:
            if condition_set.evaluate(cmd_context):
                value = True
                break

        return value