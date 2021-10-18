from Actions.Action import Action
from Actions.Condition import ConditionEvaluator, ConditionSet

class If(Action, ConditionEvaluator):
    _true_actions: list[Action]
    _false_actions: list[Action]
    _negate: bool = False

    def __init__(self, condition_sets: list[ConditionSet] = [], true_actions: list[Action] = [], false_actions: list[Action] = []) -> None:
        self._condition_sets = condition_sets
        self._true_actions = true_actions
        self._false_actions = false_actions

        super().__init__()

    def execute(self, cmd_context) -> None:
        if len(self._condition_sets) == 0:
            return

        actions: list[Action] = []
        if self.evaluate(cmd_context):
            actions = self._true_actions
        else:
            actions = self._false_actions

        for action in actions:
            action.execute(cmd_context)

        return super().execute(cmd_context)