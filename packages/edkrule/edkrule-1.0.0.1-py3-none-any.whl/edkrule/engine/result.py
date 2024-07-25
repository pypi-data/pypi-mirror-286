from edkrule.engine.finder.by import By


class Result:
    def __init__(self, expression):
        self._expression = expression

    def get(self, rule_fragment_text: str = None):
        """
        返回表达式的执行结果
        如果 rule_fragment_text 不传，则返回当前Expression 的执行结果
        如果 rule_fragment_text 传入片段，则返回片段的执行结果
        :param rule_fragment_text:
        :type rule_fragment_text:
        :return:
        :rtype:
        """
        if not rule_fragment_text:
            return self._expression.engine.cache.get(self._expression.rid)
        else:
            rid = self._expression.find(rule_fragment_text).rid
            return self._expression.engine.cache.get(rid)

    def track(self):
        """返回执行顺序及对应的结果"""
        return [{
            rid: {"text": self._expression.find(By.Rid, rid).text,
                  "result": self._expression.engine.cache.get(rid)
                  }
        } for rid in self._expression.engine.squeue.data]
