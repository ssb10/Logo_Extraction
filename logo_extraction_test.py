import os
import unittest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from logo_extraction import LogoExtraction


class TestLogoExtraction(unittest.TestCase):

    def setUp(self):
        options = Options()
        options.headless = True
        self.driver = webdriver.Firefox(options=options, executable_path=r'geckodriver-v0.24.0-win64\geckodriver')
        self.L = LogoExtraction()

    def test_invalid_urls_in_file(self):
        """
            Checking for invalid urls
        """
        with open("invalid_url.txt", "w") as invalid_input_file:
            invalid_input_file.write('abc.xyz.com')

        self.assertRaises(Exception, self.L.fetch_logos, "invalid_url.txt")

        if os.path.exists("invalid_url.txt"):
            os.remove("invalid_url.txt")

    def test_empty_file(self):
        """
            Checking if program exits for an empty file
        """
        open("empty_file.txt", "w").close()

        self.assertRaises(SystemExit,self.L.get_url_from_file, "empty_file.txt")

        if os.path.exists("empty_file.txt"):
            os.remove("empty_file.txt")

    def test_get_element_by_xpath(self):
        """
            Check if web element is fetched correctly
        """
        self.driver.get("http://python.org")
        images = self.L.get_element_by_xpath(self.driver, '//img')

        assert images[0].get_attribute(
            'src') == 'https://www.python.org/static/img/python-logo.png', "Invalid element fetched!"

    def test_end_to_end(self):
        """
            Checks for end to end system and accuracy analysis
        """
        self.L.fetch_logos("input_logo.txt")

        self.output_logo_urls = []
        with open("output_new.txt") as output_file:
            for line in output_file:
               self.output_logo_urls.append(line.split(",")[1])

        self.input_logo_urls = []
        with open("input_logo.txt") as input_file:
            next(input_file)
            for line in input_file:
                self.input_logo_urls.append(line.split(",")[1])

        matching_url = [i for i, j in zip(self.input_logo_urls, self.output_logo_urls) if i == j]
        # Comparing the count of obtained logo urls and expected logo urls. The current implementation fetches 28 urls correctly.
        assert len(matching_url) >= 28, "Accuracy of system has reduced"
        print("Accuracy Report: %.2f" % matching_url/len(self.output_logo_urls))

    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()