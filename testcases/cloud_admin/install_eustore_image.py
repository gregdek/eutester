#!/usr/bin/python

from eucaops import Eucaops
from eutester.eutestcase import EutesterTestCase
from eutester.machine import Machine
import random
import time

class TestEustoreImages(EutesterTestCase):
    def __init__(self):
        self.setuptestcase()
        self.setup_parser()
        self.get_args()
        # Setup unique bucket name to epoch time.
        self.bucketname='test'+str(int(time.time()))
        # Setup basic eutester object. Password, config file, and credpath 
        # are passed from MicroQA (or elsewhere.)
        self.tester = Eucaops( config_file=self.args.config,password=self.args.password,credpath=self.args.credpath)

    def clean_method(self):
        pass
        # TODO: we'll put image deletion in here.

    def InstallEustoreImages(self):
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

        # OK, now we have a list. Get a random element from it.
        image_id = image_list[random.randint(0,len(image_list)-1)][0]
 
        # Now install that image, into the test bucket.
        # Note the very long timeout! 15 minutes in this case.
        image_install_output = first_clc.sys( "/usr/bin/eustore-install-image -b " + self.bucketname + " -i " + image_id, timeout=1800 )

        # NOTE: NEED TO EXTEND SSH TIMEOUT HERE!

        print image_install_output

        # Be sure to set the image to be installable by all.
        # TODO:
        # * get the EMI from the last line of the output
        # * pass that EMI off for further testing (how?)
        # * once that works, add arguments to the test for:
        #   + testing all images
        #   + testing certain kinds of images

if __name__ == "__main__":
    testcase = TestEustoreImages()
    ### Use the list of tests passed from config/command line to determine what subset of tests to run
    ### or use a predefined list
    # list = testcase.args.tests or ["ConfigureELB"]
    list = testcase.args.tests or ["InstallEustoreImages"]

    ### Convert test suite methods to EutesterUnitTest objects
    unit_list = [ ]
    for test in list:
        unit_list.append( testcase.create_testunit_by_name(test) )

    ### Run the EutesterUnitTest objects
    result = testcase.run_test_case_list(unit_list,clean_on_exit=True)
    exit(result)
