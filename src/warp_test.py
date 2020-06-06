import unittest
from console import console
from warp import Warp

class TestBasicFunctionalities(unittest.TestCase):

    def runTest(self):
        self.test = Warp()

        self.assert_console_accepts_markers()
        self.assert_console_accepts_end_tempo()
        self.assert_console_accepts_b2s()
        self.assert_console_accepts_s2b()

        self.assert_expected_s2b_inbetween_the_two_markers()
        self.assert_expected_b2s_inbetween_the_two_markers()
        
        self.assert_expected_s2b_and_b2s_before_the_2markers()
        self.assert_expected_s2b_and_b2s_after_all_2markers()
        self.assert_expected_s2b_and_b2s_if_call_is_on_marker()

        self.assert_s2b_b2s_act_properly_after_third_marker_introduced()
    
    def assert_console_accepts_b2s(self):
        """Checks if the console accepts the b2s command"""
        self.assertFalse(isinstance(type(console(self.test, "b2s 0.5")), type(None)))
    
    def assert_console_accepts_s2b(self):
        """Checks if the console accepts the s2b command"""
        self.assertFalse(isinstance(type(console(self.test, "s2b 2.5")), type(None)))

    def assert_console_accepts_markers(self):
        """Checks if the console accepts the marker command"""
        self.assertEqual(console(self.test, "marker 0.0 0.0"), None)
        self.assertEqual(console(self.test, "marker 1.0 5.0"), None)
    
    def assert_console_accepts_end_tempo(self):
        """Checks if the console accepts end_tempo command"""
        self.assertEqual(console(self.test, "end_tempo 10.0"), None)
    
    def assert_expected_s2b_inbetween_the_two_markers(self):
        """Checks if the seconds to beats function works properly inbetween two markers"""
        self.assertEqual(console(self.test, "s2b 2.5"), 0.5)
    
    def assert_expected_b2s_inbetween_the_two_markers(self):
        """Checks if the beats to second funciton works properly inbetween two markers"""
        self.assertEqual(console(self.test, "b2s 0.5"), 2.5)

    def assert_expected_s2b_and_b2s_before_the_2markers(self):
        """Checks if the b2s and s2b functions work properly before the set of markers"""
        self.assertEqual(console(self.test, "b2s -0.5"), -2.5)
        self.assertEqual(console(self.test, "s2b -2.5"), -0.5)
    
    def assert_expected_s2b_and_b2s_after_all_2markers(self):
        """Checks if the s2b and b2s work properly after the markers (i.e. end_tempo)"""
        self.assertEqual(console(self.test, "s2b 6"), 11)
        self.assertEqual(console(self.test, "b2s 11"), 6)

    def assert_expected_s2b_and_b2s_if_call_is_on_marker(self):
        self.assertEqual(console(self.test, "s2b 1.0"), 5.0)
        self.assertEqual(console(self.test, "b2s 5.0"), 1.0)

    def assert_s2b_b2s_act_properly_after_third_marker_introduced(self):
        r"""
        Checks that if a third marker is introduce inbetween the
        two prior defined markers that the funciton behvaiors are maintained

                                     (NEW / ADDED)                                           v
        i.e.                    0         0.5       1.0
        beat  line        -----*---------*-----------*-------->
        (before all region)    |  section \  section  \   (after all region)
                               |      A    \     B     \ 
        time line        ------*------------*-----------*----->
                                0           4           5
        """
        console(self.test, "marker 0.5 4")
            # this change will add the marker shown in the docstring.
            # Pracitcally, this change should alter the value of the tempo 
            # before all markers, add an internal section for the, and not
            # impact the final section

        # check section A
        self.assertEqual(console(self.test, "s2b 2"), 0.25)
        self.assertEqual(console(self.test, "b2s 0.25"), 2)

        # check section B
        self.assertEqual(console(self.test, "s2b 4.5"), 0.75)
        self.assertEqual(console(self.test, "b2s 0.75"), 4.5)

        # check before all region
        self.assertEqual(console(self.test, "s2b -2"), -0.25)
        self.assertEqual(console(self.test, "b2s -0.25"), -2)

        # check final region
        self.assertEqual(console(self.test, "s2b 6"), 11)
        self.assertEqual(console(self.test, "b2s 11"), 6)

        # check if call is on marker functionality
        self.assertEqual(console(self.test, "s2b 0.5"), 4)
        self.assertEqual(console(self.test, "b2s 4"), 0.5)
    

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(TestBasicFunctionalities())