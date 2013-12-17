#!/usr/bin/python

from eucaops import Eucaops
from eutester.eutestcase import EutesterTestCase
from eutester.machine import Machine


class TestEustoreImage(EutesterTestCase):
    def __init__(self):
        self.setuptestcase()
        self.setup_parser()
        self.parser.add_argument("--img-repo")
        self.get_args()
        # Setup basic eutester object
        self.tester = Eucaops( config_file=self.args.config,password=self.args.password)

    def clean_method(self):
        pass
        # This will be the method to delete images after testing

    def InstallEustoreImage(self):
        """
        This test randomly selects an image from the Eustore list of images,
        using the admin credentials on the CLC (passed in self.tester.credpath). 
        """
        clcs = self.tester.get_component_machines("clc")
        if len(clcs) == 0:
            raise Exception("Unable to find a CLC")
        first_clc = clcs[0]
        assert isinstance(first_clc,Machine)

        # Source the credpath on the CLC from the argument provided
        first_clc.sys("source " + self.tester.credpath + "/eucarc")

        # Get the list of eustore images and put into image_list
        image_list = first_clc.sys("/usr/bin/eustore-describe-images")
        for index, image_entry in enumerate(image_list):
            image_list[index] = image_entry.split("\t")

        print image_list
        # TODO:
        # * select a random image and run eustore-install-image
        # * get the EMI from the last line of the output
        # * pass that EMI off for further testing (how?)
        # * once that works, add arguments to the test for:
        #   + testing all images
        #   + testing certain kinds of images

if __name__ == "__main__":
    testcase = TestEustoreImage()
    ### Use the list of tests passed from config/command line to determine what subset of tests to run
    ### or use a predefined list
    # list = testcase.args.tests or ["ConfigureELB"]
    list = testcase.args.tests or ["InstallEustoreImage"]

    ### Convert test suite methods to EutesterUnitTest objects
    unit_list = [ ]
    for test in list:
        unit_list.append( testcase.create_testunit_by_name(test) )

    ### Run the EutesterUnitTest objects
    result = testcase.run_test_case_list(unit_list,clean_on_exit=True)
    exit(result)
