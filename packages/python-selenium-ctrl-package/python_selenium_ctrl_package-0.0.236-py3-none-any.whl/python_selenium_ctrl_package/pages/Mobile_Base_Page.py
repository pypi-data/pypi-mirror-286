"""
Page class that all page models can inherit from
There are useful wrappers for common Selenium operations
"""
from datetime import datetime

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest, time, logging, os, inspect
from ..utils.general.Base_Logging import Base_Logging
# from ..utils.general import BrowserStack_Library
from ..drivers.driverfactory import DriverFactory
# from utils.Test_Rail import Test_Rail
# from pages.QCare import PageFactory
from appium.webdriver.appium_service import AppiumService
from ..utils.general.Wrapit import Wrapit
from ..utils.general import Gif_Maker


class Borg:
    # The borg design pattern is to share state
    # Src: http://code.activestate.com/recipes/66531/
    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state

    def is_first_time(self):
        "Has the child class been invoked before?"
        result_flag = False
        if len(self.__dict__) == 0:
            result_flag = True

        return result_flag


class Mobile_Base_Page(Borg, unittest.TestCase):
    "Page class that all page models can inherit from"

    def __init__(self, product):
        "Constructor"
        Borg.__init__(self)
        if self.is_first_time():
            # Do these actions if this the first time this class is initialized
            self.product = product
            self.set_directory_structure()
            self.image_url_list = []
            self.msg_list = []
            self.window_structure = {}
            self.testrail_flag = False
            # self.browserstack_flag = False
            self.test_run_id = None
            self.start_time = None      # pytest have Unresolved attribute reference if not added
            self.exceptions = []
            self.test_env = ""          # pytest have Unresolved attribute reference if not added
            self.rp_logger = None
            self.gif_file_name = ""
            # self.tesults_flag = False
            # self.base64_flag = True
            self.reset()

        self.driver_obj = DriverFactory()
        self.timestr = datetime.now().strftime("%Y%m%d_%H%M%S")
        if self.driver is not None:
            self.start()  # Visit and initialize xpaths for the appropriate page

    def reset(self):
        "Reset the base page object"
        self.driver = None
        self.result_counter = 0  # Increment whenever success or failure are called
        self.pass_counter = 0  # Increment everytime success is called
        self.mini_check_counter = 0  # Increment when conditional_write is called
        self.mini_check_pass_counter = 0  # Increment when conditional_write is called with True
        self.failure_message_list = []
        self.screenshot_counter = 1

    def get_failure_message_list(self):
        "Return the failure message list"
        return self.failure_message_list

    # def mobile_switch_page(self, page_name, product=None):
    #     """Switch the underlying class to the required Page"""
    #     # from pages.QCare import PageFactory as qcare_PageFactory
    #     # from pages.EMR import PageFactory as emr_PageFactory
    #     # from pages.PatientPortal import PageFactory as pp_PageFactory
    #     from pages.Website import PageFactory as web_PageFactory
    #     import conf.product_list as product_list
    #
    #     if product is None:
    #         product = self.product
    #     if product == product_list.Website:
    #         self.__class__ = web_PageFactory.PageFactory.get_page_object(page_name, platform='mobile').__class__
    #     # if product == product_list.PatientPortal:
    #     #     self.__class__ = pp_PageFactory.PageFactory.get_page_object(page_name).__class__

    def start_appium(self, ip='127.0.0.1', port='4723'):
        """Need to install appium with npm first: npm install -g appium"""
        self.appium_service = AppiumService()
        # self.appium_service.start(args=['--address', ip, '-p', port])
        self.appium_service.start()
        # self.set_screenshot_dir()  # Create screenshot directory
        # self.set_log_file()
        self.write('Start Appium server with url: %s:%s' % (self.appium_service._parse_host(self.appium_service._cmd), self.appium_service._parse_port(self.appium_service._cmd)))

    def register_driver(self, mobile_os_name, mobile_os_version, device_name, app_package, app_activity, remote_flag,
                        device_flag, app_name, app_path, ud_id, org_id, signing_id, no_reset_flag, appium_version):
        "Register the mobile driver"
        self.driver = self.driver_obj.run_mobile(mobile_os_name, mobile_os_version, device_name, app_package,
                                                 app_activity, remote_flag, device_flag, app_name, app_path, ud_id,
                                                 org_id, signing_id, no_reset_flag, appium_version)
        self.set_screenshot_dir()  # Create screenshot directory  # Move to start_appium
        self.set_log_file()   # Move to start_appium
        self.start()

    def get_current_driver(self):
        "Return current driver"
        return self.driver

    def get_driver_title(self):
        "Return the title of the current page"
        return self.driver.title

    # def register_testrail(self):
    #     "Register TestRail with Page"
    #     self.testrail_flag = True
    #     self.tr_obj = Test_Rail()
    #     self.write('Automation registered with TestRail', level='debug')

    def set_test_run_id(self, test_run_id):
        "Set TestRail's test run id"
        self.test_run_id = test_run_id

    def register_tesults(self):
        """Register Tesults with Page"""
        self.tesults_flag = True

    def register_tesults(self):
        "Register Tesults with Page"
        self.tesults_flag = True

    def set_calling_module(self, name):
        "Set the test name"
        self.calling_module = name

    # def register_browserstack(self):
    #     "Register Browser Stack with Page"
    #     self.browserstack_flag = True
    #     self.browserstack_obj = BrowserStack_Library()

    def get_calling_module(self):
        "Get the name of the calling module"
        calling_file = inspect.stack()[-1][1]
        if 'runpy' or 'string' in calling_file:
            calling_file = inspect.stack()[4][3]
        calling_filename = calling_file.split(os.sep)
        # This logic bought to you by windows + cygwin + git bash
        if len(calling_filename) == 1:  # Needed for
            calling_filename = calling_file.split('/')

        self.calling_module = calling_filename[-1].split('.')[0]

        return self.calling_module

    def set_directory_structure(self):
        "Setup the required directory structure if it is not already present"
        try:
            self.screenshots_parent_dir = os.path.abspath(
                os.path.join(os.curdir, 'screenshots', self.product))  # Real screencap folder dir
            if not os.path.exists(self.screenshots_parent_dir):
                os.makedirs(self.screenshots_parent_dir)
            self.logs_parent_dir = os.path.abspath(os.path.join(os.curdir, 'log',
                                                                self.product))  # Real log file dir base on Base_Logging.py constructor
            if not os.path.exists(self.logs_parent_dir):
                os.makedirs(self.logs_parent_dir)
        except Exception as e:
            self.write("Exception when trying to set directory structure")
            self.write(str(e))
            self.exceptions.append("Error when setting up the directory structure")

    def set_screenshot_dir(self):
        "Set the screenshot directory"
        try:
            self.screenshot_dir = self.get_screenshot_dir()
            if not os.path.exists(self.screenshot_dir) and self.screenshot != 'off':
                os.makedirs(self.screenshot_dir)

        except Exception as e:
            self.write("Exception when trying to set screenshot directory")
            self.write(str(e))

    def get_screenshot_dir(self):
        "Get the name of the test"
        self.testname = self.get_calling_module()
        self.testname = self.testname.replace('<', '')
        self.testname = self.testname.replace('>', '')
        # self.screenshot_dir = self.screenshots_parent_dir + os.sep + self.testname
        self.screenshot_dir = self.screenshots_parent_dir + os.sep + '[' + self.test_env + ']' + self.testname + '_' + self.timestr  # Real screencap file dir
        if os.path.exists(self.screenshot_dir):
            for i in range(1, 4096):
                if os.path.exists(self.screenshot_dir + '_' + str(i)):
                    continue
                else:
                    os.rename(self.screenshot_dir, self.screenshot_dir + '_' + str(i))
                    break

        return self.screenshot_dir

    def set_log_file(self):
        'set the log file'
        self.log_name = '[' + self.test_env + ']' + self.testname + '_' + self.timestr + '.log'
        self.log_obj = Base_Logging(log_file_name=self.log_name, level=logging.DEBUG, product=self.product)

    def set_rp_logger(self, rp_pytest_service):
            "Set the reportportal logger"
            self.rp_logger = self.log_obj.setup_rp_logging(rp_pytest_service)

    def append_latest_image(self, screenshot_name):
        "Get image url list from Browser Stack"
        screenshot_url = self.browserstack_obj.get_latest_screenshot_url()
        image_dict = {}
        image_dict['name'] = screenshot_name
        image_dict['url'] = screenshot_url
        self.image_url_list.append(image_dict)

    def save_screenshot(self, screenshot_name, pre_format="      #Debug screenshot: "):
        "Take a screenshot"
        # if self.browserstack_flag is True and screenshot_conf.BS_ENABLE_SCREENSHOTS is False:
        #     return
        if os.path.exists(self.screenshot_dir + os.sep + screenshot_name + '.png'):
            for i in range(1, 100):
                if os.path.exists(self.screenshot_dir + os.sep + screenshot_name + '_' + str(i) + '.png'):
                    continue
                else:
                    os.rename(self.screenshot_dir + os.sep + screenshot_name + '.png',
                              self.screenshot_dir + os.sep + screenshot_name + '_' + str(i) + '.png')
                    break
        screenshot_name = self.screenshot_dir + os.sep + screenshot_name + '.png'
        self.driver.get_screenshot_as_file(screenshot_name)
        # self.conditional_write(flag=True,positive= screenshot_name + '.png',negative='', pre_format=pre_format)
        if self.rp_logger:
            self.save_screenshot_reportportal(screenshot_name)
        # if self.browserstack_flag is True:
        #     self.append_latest_image(screenshot_name)
        # if self.tesults_flag is True:
        #     self.images.append(screenshot_name)
        # if self.base64_flag is True:
        #     with open(screenshot_name, "rb") as image_file:
        #         encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        #         self.images.append("data:image/png;base64," + encoded_string)
        #
        # # Add screenshot to HTML
        # # using Jinja2
        # with open('report.html', 'w') as file:
        #     template = Template('''
        #             <html>
        #             <head>
        #                 <title>Test Report</title>
        #             </head>
        #             <body>
        #                 {% for image in images %}
        #                 <img src="{{ image }}" alt="screenshot">
        #                 {% endfor %}
        #             </body>
        #             </html>
        #             ''')
        #     file.write(template.render(images=self.images))


    def save_screenshot_reportportal(self, image_name):
        "Method to save image to ReportPortal"
        try:
            with open(image_name, "rb") as fh:
                image = fh.read()
            screenshot_name = os.path.basename(image_name)
            self.rp_logger.info(
                screenshot_name,
                attachment={
                    "name": screenshot_name,
                    "data": image,
                    "mime": "image/png"
                },
            )
        except Exception as e:
            self.write("Exception when trying to get rplogger")
            self.write(str(e))
            self.exceptions.append("Error when trying to get reportportal logger")

    def open(self, url, wait_time=2):
        "Visit the page base_url + url"
        self.base_url = "https://"
        if self.base_url[-1] != '/' and url[0] != '/':
            url = '/' + url
        if self.base_url[-1] == '/' and url[0] == '/':
            url = url[1:]
        url = self.base_url + url
        if self.driver.current_url != url:
            self.driver.get(url)
        self.wait(wait_time)

    def get_page_paths(self, section):
        "Open configurations file,go to right sections,return section obj"
        pass

    def get_element(self, locator, verbose_flag=True):
        "Return the DOM element of the path or 'None' if the element is not found "
        dom_element = None
        try:
            locator = self.split_locator(locator)
            dom_element = self.driver.find_element(*locator)
        except Exception as e:
            if verbose_flag is True:
                self.write(str(e), 'debug')
                self.write("Check your locator-'%s,%s' in the conf/locators.conf file" % (locator[0], locator[1]))
                # self.get_session_details()

        return dom_element

    def split_locator(self, locator):
        "Split the locator type and locator"
        result = ()
        try:
            result = tuple(locator.split(',', 1))
        except Exception as e:
            self.write(str(e), 'debug')
            self.write("Error while parsing locator")

        return result

    def get_elements(self, locator, msg_flag=True):
        "Return a list of DOM elements that match the locator"
        dom_elements = []
        try:
            locator = self.split_locator(locator)
            dom_elements = self.driver.find_elements(*locator)
        except Exception as e:
            if msg_flag == True:
                self.write(e, 'debug')
                self.write("Check your locator-'%s' in the conf/locators.conf file" % locator)

        return dom_elements

    def click_element(self, locator, wait_time=3):
        "Click the button supplied"
        link = self.get_element(locator)
        if link is not None:
            try:
                link.click()
                self.wait(wait_time)
            except Exception as e:
                self.write('Exception when clicking link with path: %s' % locator)
                self.write(e)
            else:
                return True

        return False

    def set_text(self, locator, value, clear_flag=True):
        "Set the value of the text field"
        text_field = self.get_element(locator)
        try:
            if clear_flag is True:
                text_field.clear()
        except Exception as e:
            self.write('ERROR: Could not clear the text field: %s' % locator, 'debug')

        result_flag = False
        try:
            text_field.send_keys(value)
            result_flag = True
        except Exception as e:
            self.write('Unable to write to text field: %s' % locator, 'debug')
            self.write(str(e), 'debug')

        return result_flag

    def get_text(self, locator):
        "Return the text for a given xpath or the 'None' object if the element is not found"
        text = ''
        try:
            text = self.get_element(locator).text
        except Exception as e:
            self.write(e)
            return None
        else:
            return text.encode('utf-8')

    get_text_by_locator = get_text  # alias the method

    def get_dom_text(self, dom_element):
        "Return the text of a given DOM element or the 'None' object if the element has no attribute called text"
        text = None
        try:
            text = dom_element.text
            text = text.encode('utf-8')
        except Exception as e:
            self.write(e)

        return text

    def select_checkbox(self, locator):
        "Select a checkbox if not already selected"
        checkbox = self.get_element(locator)
        if checkbox.is_selected() is False:
            result_flag = self.toggle_checkbox(locator)
        else:
            result_flag = True

        return result_flag

    def deselect_checkbox(self, locator):
        "Deselect a checkbox if it is not already deselected"
        checkbox = self.get_element(locator)
        if checkbox.is_selected() is True:
            result_flag = self.toggle_checkbox(locator)
        else:
            result_flag = True

        return result_flag

    unselect_checkbox = deselect_checkbox  # alias the method

    def toggle_checkbox(self, locator):
        "Toggle a checkbox"
        return self.click_element(locator)

    def select_dropdown_option(self, locator, option_text):
        "Selects the option in the drop-down"
        result_flag = False
        dropdown = self.get_element(locator)
        for option in dropdown.find_elements_by_tag_name('option'):
            if option.text == option_text:
                option.click()
                result_flag = True
                break

        return result_flag

    def check_element_present(self, locator):
        "This method checks if the web element is present in page or not and returns True or False accordingly"
        result_flag = False
        if self.get_element(locator, verbose_flag=False) is not None:
            result_flag = True

        return result_flag

    def check_element_displayed(self, locator):
        "This method checks if the web element is visible on the page or not and returns True or False accordingly"
        result_flag = False
        if self.get_element(locator) is not None:
            element = self.get_element(locator, verbose_flag=False)
            if element.is_displayed() is True:
                result_flag = True

        return result_flag

    def stop_appium(self):
        if self.appium_service is not None and self.appium_service.is_running is True:
            self.appium_service.stop()
            self.write('Stop Appium server')

    def make_gif(self):
        "Create a gif of all the screenshots within the screenshots directory"
        # Original code, set a checking case for screenshot option
        # self.gif_file_name = Gif_Maker.make_gif(self.screenshot_dir, name=self.calling_module)
        #
        # return self.gif_file_name
        if self.screenshot != 'off':
            self.gif_file_name = Gif_Maker.make_gif(self.screenshot_dir, name=self.calling_module)
            return self.gif_file_name

    def base_make_gif(self):
        gif_file = self.make_gif()
        if self.gif_file_name is not None:
            self.write("Screenshots & GIF created at %s" % self.screenshot_dir)
            self.write('************************')
            return gif_file

    def teardown(self):
        "Tears down the driver"
        self.driver.quit()
        self.stop_appium()
        self.reset()

    def check_alert(self):
        result_flag = False
        try:
            alert = self.driver.switch_to.alert
            result_flag = True
        except:
            pass
        return result_flag

    def write(self, msg, level='info'):
        "Log the message"
        self.msg_list.append('%-8s:  ' % level.upper() + msg)
        # if self.browserstack_flag is True:
        #     if self.browserstack_msg not in msg:
        #         self.msg_list.pop(-1)  # Remove the redundant BrowserStack message
        self.log_obj.write(msg, level)

    # def report_to_testrail(self, case_id, test_run_id, result_flag, msg=''):
    #     "Update Test Rail"
    #     if self.testrail_flag is True:
    #         self.write('Automation is about to update TestRail for case id: %s' % str(case_id), level='debug')
    #         msg += '\n'.join(self.msg_list)
    #         msg = msg + "\n"
    #         if self.browserstack_flag is True:
    #             for image in self.image_url_list:
    #                 msg += '\n' + '[' + image['name'] + '](' + image['url'] + ')'
    #             msg += '\n\n' + '[' + 'Watch Replay On BrowserStack' + '](' + self.session_url + ')'
    #         self.tr_obj.update_testrail(case_id, test_run_id, result_flag, msg=msg)
    #     self.image_url_list = []
    #     self.msg_list = []


    def wait(self, wait_seconds=5, locator=None):
        "Performs wait for time provided"
        if locator is not None:
            self.smart_wait(wait_seconds, locator)
        else:
            time.sleep(wait_seconds)

    def smart_wait(self, wait_seconds, locator):
        "Performs an explicit wait for a particular element"
        result_flag = False
        try:
            path = self.split_locator(locator)
            WebDriverWait(self.driver, wait_seconds).until(EC.presence_of_element_located(path))
            result_flag = True
        except Exception:
            self.conditional_write(result_flag,
                                   positive='Located the element: %s' % locator,
                                   negative='Could not locate the element %s even after %.1f seconds' % (
                                   locator, wait_seconds))

        return result_flag

    def success(self, msg, level='info', pre_format='PASS: '):
        "Write out a success message"
        if level.lower() == 'critical':
            level = 'info'
        self.log_obj.write(pre_format + msg, level)
        self.result_counter += 1
        self.pass_counter += 1

    def failure(self, msg, level='info', pre_format='FAIL: '):
        "Write out a failure message"
        self.log_obj.write(pre_format + msg, level)
        self.result_counter += 1
        self.failure_message_list.append(pre_format + msg)
        if level.lower() == 'critical':
            self.teardown()
            raise Exception("Stopping test because: " + msg)

    def log_result(self, flag, positive, negative, level='info'):
        "Write out the result of the test"
        if flag is True:
            self.success(positive, level=level)
        if flag is False:
            self.failure(negative, level=level)

    def conditional_write(self, flag, positive, negative, level='debug', pre_format="  - "):
        "Write out either the positive or the negative message based on flag"
        if flag is True:
            self.write(pre_format + positive, level)
            self.mini_check_pass_counter += 1
        if flag is False:
            self.write(pre_format + negative, level)
        self.mini_check_counter += 1

    def write_test_summary(self):
        "Print out a useful, human readable summary"
        self.write(
            '\n\n************************\n--------RESULT--------\nTotal number of checks=%d' % self.result_counter)
        self.write(
            'Total number of checks passed=%d\n----------------------\n************************\n\n' % self.pass_counter)
        self.write('Total number of mini-checks=%d' % self.mini_check_counter)
        self.write('Total number of mini-checks passed=%d' % self.mini_check_pass_counter)
        failure_message_list = self.get_failure_message_list()
        if len(failure_message_list) > 0:
            self.write('\n--------FAILURE SUMMARY--------\n')
            for msg in failure_message_list:
                self.write(msg)
        if len(self.exceptions) > 0:
            self.exceptions = list(set(self.exceptions))
            self.write('\n--------USEFUL EXCEPTION--------\n')
            for (i, msg) in enumerate(self.exceptions, start=1):
                self.write(str(i) + "- " + msg)
        return self.base_make_gif()

    def start(self):
        "Dummy method to be over-written by child classes"
        pass

    # def open(self, url, wait_time=2):
    #     self.driver.get(url)
    #     self.wait(wait_time)

    def get_contexts(self):
        contexts = self.driver.contexts
        return contexts

    def switch_webview(self, element):
        self.driver.switch_to.context(element)

    @Wrapit._screenshot
    def take_screenshot(self):
        """Use this function to take screenshot, the screen shot will take only when screenshot option = all"""
        return True

    @Wrapit._screenshot
    def take_force_screenshot(self):
        """Use this function to take screenshot, the screen shot will take even use screenshot option = failonly"""
        return False
