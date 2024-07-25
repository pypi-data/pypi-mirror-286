from edkrule.engine.finder.finder_by_rid import FinderByRid
from edkrule.engine.finder.finder_by_rule_fragment import FinderByRuleFragment
from edkrule.utils.format.blank_formater import BlankFormater


class By:
    Rid = FinderByRid()
    RuleFragment = FinderByRuleFragment(BlankFormater())
