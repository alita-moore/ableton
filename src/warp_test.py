import unittest
from utils import console
from warp import Warp

class TestWarp(unittest.TestCase):
    """
    A test that validates basic functionality,
    excpetion handlin, main s2b and b2s funcitons,
    and performance.
    """

    def runTest(self):
        self.test = Warp()

        # validate basic functionality
        self.assert_console_accepts_markers()
        self.assert_accepts_end_tempo()
        self.assert_console_accepts_b2s()
        self.assert_console_accepts_s2b()
        self.assert_expected_s2b_and_b2s_if_only_1_marker()

        # validate basic exceptions
        self.assert_warp_filters_invalid_markers_properly()
        self.assert_warp_filters_invalid_b2s_and_s2p_ie_no_end_tempo()
        self.assert_end_tempo_doesnt_accept_negatives()

        # validate the s2b and b2s functionalities at edge points
        self.assert_expected_s2b_inbetween_the_two_markers()
        self.assert_expected_b2s_inbetween_the_two_markers()
        self.assert_expected_s2b_and_b2s_before_the_2markers()
        self.assert_expected_s2b_and_b2s_after_all_2markers()
        self.assert_expected_s2b_and_b2s_if_call_is_on_marker()
        self.assert_s2b_b2s_act_properly_after_third_marker_introduced()

        # validate performance
        self.check_if_solution_is_optimal()
    
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
    
    def assert_accepts_end_tempo(self):
        """Checks if the console accepts end_tempo command"""
        self.assertEqual(console(self.test, "end_tempo 10.0"), None)
        self.assertEqual(self.test.end_tempo, 10)

    def assert_warp_filters_invalid_markers_properly(self):
        """
        Verifies that the object's marker values do not change / update
        when fed an invalid object. There are two invalid possibilities:
        1) the marker is already defined
        2) there is an intersection with another marker
        """
        markers = self.test.markers.copy()

        # already defined points
        console(self.test, "marker 0.0 1.0")
        console(self.test, "marker 1.0 0.0")
        self.assertEqual(markers, self.test.markers)

        # interceting vertices
        console(self.test, "marker 0.5 6.0")
        self.assertEqual(markers, self.test.markers)

    def assert_warp_filters_invalid_b2s_and_s2p_ie_no_end_tempo(self):
        """
        Verifies that if a end_tempo is not given, the b2s and s2b
        methods will have no output
        """
        self.test.set_end_tempo(None)
        self.assertEqual(console(self.test, "b2s 2.0"), None)
        self.assertEqual(console(self.test, "s2b 6.0"), None)
        self.test.set_end_tempo(10.0)

    def assert_end_tempo_doesnt_accept_negatives(self):
        """
        Verifies that if a negative values is provided to end_tempo
        that nothing changes.
        """
        end_tempo = self.test.end_tempo
        self.assertEqual(console(self.test, "end_tempo -10"), None)
        self.assertEqual(end_tempo, self.test.end_tempo)

    def assert_expected_s2b_and_b2s_if_only_1_marker(self):
        warp_test = Warp()
        warp_test.set_marker(0,0)
        warp_test.set_end_tempo(10)

        # after marker
        self.assertEqual(console(warp_test, "s2b 1"), 10)
        self.assertEqual(console(warp_test, "b2s 10"), 1)

        # before marker
        self.assertEqual(console(warp_test, "s2b -1"), -10)
        self.assertEqual(console(warp_test, "b2s -10"), -1)

        # on marker
        self.assertEqual(console(warp_test, "s2b 0"), 0)
        self.assertEqual(console(warp_test, "b2s 0"), 0)

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
        """verify that if b2s and s2b are called on their respective markers, the result
        is consistent with their defintions. Notably, (0,0) is easy to cause errors."""
        self.assertEqual(console(self.test, "b2s 1.0"), 5.0)
        self.assertEqual(console(self.test, "s2b 5.0"), 1.0)
        self.assertEqual(console(self.test, "s2b 0"), 0)
        self.assertEqual(console(self.test, "b2s 0"), 0)
    
    def assert_that_order_of_marker_vs_end_tempo_setting_doesnt_matter(self):
        """Verify that the end_tempo can be set before the markers are set"""
        self.test = Warp()

        self.assert_accepts_end_tempo()
        self.assert_console_accepts_markers()
        self.assert_console_accepts_b2s()
        self.assert_console_accepts_s2b()

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
        self.assertEqual(console(self.test, "b2s 0.5"), 4)
        self.assertEqual(console(self.test, "s2b 4"), 0.5)
    
    def check_if_solution_is_optimal(self):
        """Verifies that the main pull-function has complexity O(log(n)) or better"""
        import timeit
        import math
        import statistics as stats

        avg_log = []
        test_ns = [2**i for i in range(4, 10)]
        
        for n in test_ns:
            test_warp = Warp()
            avg_exc = 0
            avg_exc_ref = 0

            for marker in range(1, n):
                console(test_warp, "marker " + str(float(marker)) + ' ' + str(float(marker)))
            
            repeats = 25
            for _ in range(repeats):
                execution = timeit.timeit(lambda: [console(test_warp, 'b2s ' + str(n-0.1)), console(test_warp, 's2b ' + str(n//2-0.1))], number=400)
                avg_exc += execution / repeats
                execution = timeit.timeit(lambda: [ord(x) for x in "aasdfadgasdfwr22"], number = 1000)
                avg_exc_ref += execution / repeats

            avg_log.append(avg_exc / avg_exc_ref)
            print("(raw time, for 400 requests, and n-markers = %d)"
                    "mean: %f, theoretical frequency: %f" 
                    % (n, avg_exc, 2*400/avg_exc))  # 2 * because s2b and b2s in conjunction
        
        avg_log = [math.log2(avg_log[i+1]/avg_log[i]) for i in range(len(avg_log)-1)]
        print("(logarithm) mean: %f, std: %f, adjusted mean: %f" % (stats.mean(avg_log), stats.stdev(avg_log), stats.mean(avg_log) + 2*stats.stdev(avg_log)))
        self.assertTrue(stats.mean(avg_log) < 0.15)  # O(log(n))
        

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(TestWarp())