import unittest

from birdwatcher.congress.datalog import nonrecursive
from birdwatcher.congress.datalog import compile
from birdwatcher.congress.tests import helper
from birdwatcher.congress.policy_engines import agnostic

class TestSRuntime(unittest.TestCase):

    def check_equal(self, actual_string, correct_string, msg):
        self.assertTrue(helper.datalog_equal(
            actual_string, correct_string, msg))

    def test_theory_inclusion(self):
        """Test evaluation routines when one theory includes another."""
        # spread out across inclusions
        th1 = nonrecursive.NonrecursiveRuleTheory()
        th2 = nonrecursive.NonrecursiveRuleTheory()
        th3 = nonrecursive.NonrecursiveRuleTheory()
        th1.includes.append(th2)
        th2.includes.append(th3)

        th1.insert(helper.str2form('p(x) :- q(x), r(x), s(2)'))
        th2.insert(helper.str2form('q(1)'))
        th1.insert(helper.str2form('r(1)'))
        th3.insert(helper.str2form('s(2)'))

        self.check_equal(
            helper.pol2str(th1.select(helper.str2form('p(x)'))),
            'p(1)', 'Data spread across inclusions')
        
    def test_multi_policy_update(self):
        """Test updates that apply to multiple policies."""
        def check_equal(actual, correct):
            e = helper.datalog_equal(actual, correct)
            self.assertTrue(e)

        run = agnostic.Runtime()
        run.create_policy('th1')
        run.create_policy('th2')

        events1 = [compile.Event(formula=x, insert=True, target='th1')
                   for x in helper.str2pol("p(1) p(2) q(1) q(3)")]
        events2 = [compile.Event(formula=x, insert=True, target='th2')
                   for x in helper.str2pol("r(1) r(2) t(1) t(4)")]
        run.update(events1 + events2)

        check_equal(run.select('p(x)', 'th1'), 'p(1) p(2)')
        check_equal(run.select('q(x)', 'th1'), 'q(1) q(3)')
        check_equal(run.select('r(x)', 'th2'), 'r(1) r(2)')
        check_equal(run.select('t(x)', 'th2'), 't(1) t(4)')

    
