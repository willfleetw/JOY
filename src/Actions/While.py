from Actions.Action import Action
from Actions.Condition import ConditionEvaluator, ConditionSet

class While(Action, ConditionEvaluator):
    _actions: list[Action]

    def __init__(self, condition_sets: list[ConditionSet] = [], actions: list[Action] = []) -> None:
        self._condition_sets = condition_sets
        self._actions = actions

        super().__init__()

    def execute(self, cmd_context) -> None:
        while self.evaluate(cmd_context):
            for action in self._actions:
                action.execute(cmd_context)

        return super().execute(cmd_context)