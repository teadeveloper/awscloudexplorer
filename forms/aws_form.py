""" AWS Form

This file contains classes and methods for showing the (TUI) text user interface for EC2, S3 etc.


This file contains the following classes & methods:

* AwsTableWidget - inherited class to show a grid with wows a columns. (GridColTitles widget)
* AwsServiceWidget - inherited class to show the AWS servicies such as EC3, S3, VPCs, etc. (Multiline widget)
* AwsInformationWidget - inherited class to show the information for the service choosen in AwsTableWidget
 (Multiline widget)

* BoxAwsTableWidgetBox - The box widget contains AwsTableWidget widget of another class.
* BoxAwsServiceWidget -  The box widget contains AwsServiceWidget widget of another class.
* BoxAwsDetailWidget -  The box widget contains AwsInformationWidget widget of another class.

* AwsMeanForm - A FormBaseNew that contains all the widgets to create the MAIN form.
* SELECT_REGION - A popup form to select the AWS region.


"""

import curses
import os
import time
import npyscreen
import yaml

from providers.aws.ec2 import AwsEc2
from providers.aws.s3 import AwsS3
from providers.aws.network import AwsNetwork
from providers.aws.security import AwsSecurity
from functools import partial


class AwsRegionWidget(npyscreen.MultiLineAction):
    pass


class AwsTableWidget(npyscreen.SimpleGrid):
    pass


class AwsServiceWidget(npyscreen.MultiLineAction):
    def actionHighlighted(self, act_on_this, keypress):
        self.parent.parentApp.getForm('MAIN').act_service_selected_action(act_on_this)


class AwsInformationWidget(npyscreen.MultiLine):
    pass


class BoxAwsRegionWidgetBox(npyscreen.BoxTitle):
    _contained_widget = AwsRegionWidget


class BoxAwsTableWidgetBox(npyscreen.BoxTitle):
    _contained_widget = AwsTableWidget


class BoxAwsServiceWidget(npyscreen.BoxTitle):
    _contained_widget = AwsServiceWidget


class BoxAwsDetailWidget(npyscreen.BoxTitle):
    _contained_widget = AwsInformationWidget


class AwsMeanForm(npyscreen.FormBaseNewWithMenus):
    with open("forms/aws_form.yml") as f:
        configuration = yaml.load(f, Loader=yaml.FullLoader)

    # General variables
    service_selected = ""

    aws_region = configuration["aws_region"]
    aws_end_end_point = configuration["aws_end_end_point"]

    ec2 = AwsEc2(aws_end_end_point, aws_region)
    s3 = AwsS3(aws_end_end_point, aws_region)
    network = AwsNetwork(aws_end_end_point, aws_region)
    Security = AwsSecurity(aws_end_end_point, aws_region)

    def create(self):  # override the Form’s create() method, which is called whenever a Form is created

        npyscreen.setTheme(npyscreen.Themes.ColorfulTheme)

        self.aws_ec2_menu = self.add_menu(name="Instances EC2")
        self.aws_s3_menu = self.add_menu(name="S3 Buckets")
        self.aws_network_menu = self.add_menu(name="Network")
        self.aws_security_menu = self.add_menu(name="Security")

        self.aws_ec2_menu.addItemsFromList([
            ("Export instances", self.ec2_export_to),
            ("Export with all columns", self.ec2_all_keys_export_to),
        ])

        self.aws_s3_menu.addItemsFromList([
            ("Export Buckets", self.s3_export_to),
        ])

        self.aws_network_menu.addItemsFromList([
            ("Export VPCs", self.vpc_export_to),
            ("Export Subnets", self.subnets_export_to),
            ("Export ACLS", self.acls_export_to),
        ])

        self.aws_security_menu.addItemsFromList([
            ("Export Security Groups", self.security_group_export_to),
        ])

        self.tw_aws_region = self.add(
            BoxAwsRegionWidgetBox,
            name="Region:",
            relx=self.configuration["tw_region_relx"],
            rely=self.configuration["tw_region_rely"],
            width=self.configuration["tw_region_width"],
            height=self.configuration["tw_region_height"],
            scroll_exit=True,
            contained_widget_arguments={
                'color': "WARNING",
                'widgets_inherit_color': True,
                'edit': False,
                'values': [os.getenv('AWS_DEFAULT_REGION')], }, )

        self.tw_aws_service = self.add(
            BoxAwsServiceWidget,
            name="Service:",
            relx=self.configuration["tw_service_relx"],
            rely=self.configuration["tw_service_rely"],
            width=self.configuration["tw_service_width"],
            scroll_exit=True,
            contained_widget_arguments={
                'color': "WARNING",
                'widgets_inherit_color': True,
                'name': "",
                'values': ["EC2", "Buckets", "VPC", "Subnets", "ACLs Network", "Security Groups", "EFS", "IAM"]})

        self.tw_aws_grid = self.add(
            BoxAwsTableWidgetBox,
            relx=self.configuration["tw_grid_relx"],
            rely=self.configuration["tw_grid_rely"],
            height=self.configuration["tw_grid_height"],
            width=self.configuration["tw_grid_width"],
            name="Select Service in the left menu",
            contained_widget_arguments={
                'color': "DEFAULT",
                # 'widgets_inherit_color': True,
                'select_whole_line': "True",
                'column_width': 20,
                'always_show_cursor': False,
            })

        self.tw_information = self.add(
            BoxAwsDetailWidget,
            name="Information:",
            relx=self.configuration["tw_information_relx"],
            rely=self.configuration["tw_information_rely"],
            width=self.configuration["tw_information_width"],

            scroll_exit=True,
            contained_widget_arguments={
                'color': "WARNING",
                'widgets_inherit_color': True,
            })

        # DEFAULT VALUES STARTING THE FORM

        self.add_handlers({"^O": self.get_instance_information})
        # Add actions to GRID
        self.tw_aws_grid.add_handlers(
            {curses.ascii.NL: self.act_on_enter_in_grid_widget})
        self.tw_aws_grid.add_handlers(
            {"^A": self.from_custom_actions_for_grid})
        self.tw_aws_grid.add_handlers({"^E": self.export_selected_row_grid})
        self.tw_aws_grid.add_handlers({"^F": self.form_custom_filter})
        self.tw_aws_grid.add_handlers({"^O": self.test})

        self.tw_aws_service.value = 0

    def test(self, info):
        bucket_id = self.tw_aws_grid.entry_widget.selected_row()
        text_to_show = self.s3.get_number_of_objets_size(bucket_id[0])
        npyscreen.notify_wait(message=text_to_show)

    def act_service_selected_action(self, act_on_this):

        self.service_selected = act_on_this
        self.tw_information.values = None
        self.tw_information.update()
        self.tw_information.display()

        npyscreen.notify_wait("Working. .", form_color='GOOD')

        if act_on_this == "Buckets":
            self.tw_aws_service.value = 1
            self.tw_aws_grid.name = act_on_this
            self.buckets_list = self.s3.get_buckets()
            self.tw_aws_grid.values = self.buckets_list
            self.tw_aws_grid.update(clear=True)
            self.tw_aws_grid.display()
        elif act_on_this == "EC2":
            self.tw_aws_service.value = 0
            self.tw_aws_grid.name = act_on_this
            self.ec2_list = self.ec2.get_instances()
            self.tw_aws_grid.values = self.ec2_list
            self.tw_aws_grid.update(clear=True)
            self.tw_aws_grid.display()
        elif act_on_this == "VPC":
            self.tw_aws_service.value = 2
            self.tw_aws_grid.name = act_on_this
            self.vpc_list = self.network.get_vpcs()
            self.tw_aws_grid.values = self.vpc_list
            self.tw_aws_grid.update(clear=True)
            self.tw_aws_grid.display()
        elif act_on_this == "Subnets":
            self.tw_aws_service.value = 3
            self.tw_aws_grid.name = act_on_this
            self.subnet_list = self.network.get_subnets()
            self.tw_aws_grid.values = self.subnet_list
            self.tw_aws_grid.update(clear=True)
            self.tw_aws_grid.display()
        elif act_on_this == "ACLs Network":
            self.tw_aws_service.value = 4
            self.tw_aws_grid.name = act_on_this
            self.acl_list = self.network.get_acl_network()
            self.tw_aws_grid.values = self.acl_list
            self.tw_aws_grid.update(clear=True)
            self.tw_aws_grid.display()
        elif act_on_this == "Security Groups":
            self.tw_aws_service.value = 5
            self.tw_aws_grid.name = act_on_this
            self.securitygroups_list = self.Security.get_security_groups()
            self.tw_aws_grid.values = self.securitygroups_list
            self.tw_aws_grid.update(clear=True)
            self.tw_aws_grid.display()

    def ec2_export_to(self):

        def info_message():
            npyscreen.notify_wait("Working...", form_color='GOOD')

        user_options_chosen = self.form_export_to()
        self.ec2.export_to(user_options_chosen[0], user_options_chosen[1])

    def s3_export_to(self):

        def info_message():
            npyscreen.notify_wait("Working...", form_color='GOOD')

        user_options_chosen = self.form_export_to()
        self.s3.export_to(user_options_chosen[0], user_options_chosen[1])

    def vpc_export_to(self):

        def info_message():
            npyscreen.notify_wait("Working...", form_color='GOOD')

        user_options_chosen = self.form_export_to()
        self.network.export_vpc_to(user_options_chosen[0], user_options_chosen[1])

    def security_group_export_to(self):

        def info_message():
            npyscreen.notify_wait("Working...", form_color='GOOD')

        user_options_chosen = self.form_export_to()
        self.Security.export_to(user_options_chosen[0], user_options_chosen[1])

    def subnets_export_to(self):

        def info_message():
            npyscreen.notify_wait("Working...", form_color='GOOD')

        user_options_chosen = self.form_export_to()
        self.network.export_subnet_to(user_options_chosen[0], user_options_chosen[1])

    def acls_export_to(self):

        def info_message():
            npyscreen.notify_wait("Working...", form_color='GOOD')

        user_options_chosen = self.form_export_to()
        self.network.export_acl_to(user_options_chosen[0], user_options_chosen[1])

    def ec2_all_keys_export_to(self):

        def info_message():
            npyscreen.notify_wait("Working...", form_color='GOOD')

        user_options_chosen = self.form_export_to()
        info_message()
        self.ec2.all_keys_export_to(user_options_chosen[0], user_options_chosen[1])

    def update_data_widgets(self):

        self.tw_aws_region.values = [os.getenv('AWS_DEFAULT_REGION'), ]
        self.tw_aws_region.update()

    def get_instance_information(self, *args, **keywords):
        npyscreen.notify("Reading Information from AWS API",
                         title="Information")

    def act_on_enter_in_grid_widget(self, info):
        """
        This function updates the widget tw_information using the variable service_selected (EC2, VPC, S3 etc.) and
        use the variable ec2_what_to_show_in_formation_box that contains the AWS method name to be invoked, for example
        method "describe_instances"

        """

        if self.service_selected == "EC2":
            npyscreen.notify("Reading Information for EC2 Instance",
                             title="Information")
            # get the value in row selected
            ec2id = self.tw_aws_grid.entry_widget.selected_row()

            ec2_instance_result = self.ec2.get_ec2_yml_properties(ec2id[1])
            self.tw_information.values = ec2_instance_result
            self.tw_information.update()

        elif self.service_selected == "Buckets":
            npyscreen.notify("Reading Information for Bucket",
                             title="Information")
            # get the value in row selected
            bucket_id = self.tw_aws_grid.entry_widget.selected_row()
            bucket_objects_result = self.s3.get_bucket_yml_properties(bucket_id[0])
            self.tw_information.values = bucket_objects_result
            self.tw_information.update()

        elif self.service_selected == "VPC":
            npyscreen.notify("Reading Information for VPC",
                             title="Information")
            # get the value in row selected
            vpc_id = self.tw_aws_grid.entry_widget.selected_row()
            vpc_config_result = self.network.get_vpc_yml_properties(vpc_id[0])
            self.tw_information.values = vpc_config_result
            self.tw_information.update()

        elif self.service_selected == "Subnets":
            npyscreen.notify("Reading Information for Subnet",
                             title="Information")
            # get the value in row selected
            subnet_id = self.tw_aws_grid.entry_widget.selected_row()
            subnet_config_result = self.network.get_subnet_yml_properties(subnet_id[0])
            self.tw_information.values = subnet_config_result
            self.tw_information.update()

        elif self.service_selected == "ACLs Network":
            npyscreen.notify("Reading Information for ACLs",
                             title="Information")
            # get the value in row selected
            acl_id = self.tw_aws_grid.entry_widget.selected_row()
            subnet_config_result = self.network.get_acl_yml_network_properties(acl_id[0])
            self.tw_information.values = subnet_config_result
            self.tw_information.update()

        elif self.service_selected == "Security Groups":
            npyscreen.notify("Reading Information for Security Groups",
                             title="Information")
            # get the value in row selected
            security_group_id = self.tw_aws_grid.entry_widget.selected_row()
            security_group_result = self.Security.get_security_groups_yml_properties(security_group_id[0])
            self.tw_information.values = security_group_result
            self.tw_information.update()

    def form_export_to(self):
        """Show the form to select the export_format and the file name

        :returns
        A export_format file and the name of the file.

        """

        export_form = npyscreen.ActionPopup(name="Export to")

        format_to = export_form.add(
            npyscreen.TitleSelectOne, max_height=4, value=[
                1, ], name="Select export_format", values=[
                "excel", "csv", "string", "markdown", "HTML"], scroll_exit=True)
        file_name_path = export_form.add(
            npyscreen.TitleText, name="File and name path:", )

        file_name_path.value = "type_filename.ext"

        export_form.edit()

        return format_to.value[0], file_name_path.value

    def form_custom_filter(self, info):
        """
        Show a form to select a filter (Filter to be used in the BOTO3 method), the filters to be showed in the form
        are in the file forms/aws_form.yml.

        :param info: NPYSCREEN Variable

        :return:
        """

        label_name = "Select filter"

        with open("forms/aws_form.yml") as f:
            configuration = yaml.load(f, Loader=yaml.FullLoader)

        if self.service_selected == "EC2":
            values_filter = configuration["ec2_filters"]
        elif self.service_selected == "Security Groups":
            values_filter = configuration["security_groups_filters"]
        elif self.service_selected == "VPC":
            values_filter = configuration["vpc_filters"]
        elif self.service_selected == "Subnets":
            values_filter = configuration["subnets_filters"]
        else:
            values_filter = None
            label_name = "Feature not supported yet for " + self.service_selected

        filter_form = npyscreen.ActionPopupWide(name="Custom filter")

        custom_filter = filter_form.add(
            npyscreen.TitleSelectOne,
            max_height=4,
            value=[
                0,
            ],
            name=label_name,
            values=values_filter,
            scroll_exit=True)

        # Override a NPYSCREEN method on_ok at instance level
        def new_on_ok_action(info):

            if self.service_selected == "EC2":
                value_selected = custom_filter.value[0]
                self.ec2.ec2_filter = custom_filter.values[value_selected]
                data = self.ec2.get_instances()
                self.tw_aws_grid.values = data
                self.tw_aws_grid.update(clear=True)
            elif self.service_selected == "Security Groups":
                value_selected = custom_filter.value[0]
                self.Security.security_groups_filters = custom_filter.values[value_selected]
                data = self.Security.get_security_groups()
                self.tw_aws_grid.values = data
                self.tw_aws_grid.update(clear=True)
            elif self.service_selected == "VPC":
                value_selected = custom_filter.value[0]
                self.network.vpc_filters = custom_filter.values[value_selected]
                data = self.network.get_vpcs()
                self.tw_aws_grid.values = data
                self.tw_aws_grid.update(clear=True)
            elif self.service_selected == "Subnets":
                value_selected = custom_filter.value[0]
                self.network.subnets_filters = custom_filter.values[value_selected]
                data = self.network.get_subnets()
                self.tw_aws_grid.values = data
                self.tw_aws_grid.update(clear=True)
            else:
                pass

        filter_form.on_ok = partial(new_on_ok_action, filter_form)
        filter_form.edit()

    def from_custom_actions_for_grid(self, info):
        """
        Show a form to choose the boto3 custom method to be called when the user press enter in the grid widget.

        Depends on the value of the variable  service_selected to select the actions to do.

        The methods name are saved in the file forms/aws_form.yml, it changes the variable "_info_methods"
        for the service selected.

        :param info: NPYSCREEN variable
        :return: list_method_selected
        """

        self.tw_information.values = None
        self.tw_information.update()

        methods_list = None

        action_form = npyscreen.ActionPopup(name="Actions to")

        if self.service_selected == "Buckets":
            methods_list = self.configuration["s3_info_methods"]
        elif self.service_selected == "EC2":
            methods_list = self.configuration["ec2_info_methods"]

        get_info = action_form.add(
            npyscreen.TitleSelectOne,
            value=[
                0,
            ],
            name="Select what to show in information box",
            values=methods_list,
            scroll_exit=True)

        # Override a method at instance level
        def new_on_ok_action(info):

            if self.service_selected == "Buckets":
                self.s3_what_to_show_information_box = get_info.get_selected_objects()[
                    0]
            elif self.service_selected == "EC2":
                self.ec2_what_to_show_in_formation_box = get_info.get_selected_objects()[
                    0]

        action_form.on_ok = partial(new_on_ok_action, action_form)

        action_form.edit()

        list_method_selected = get_info.get_selected_objects()[0]

        return list_method_selected

    def export_selected_row_grid(self, info):
        """
        Export to a yml file the instance selected in the grid, its use the variable service_selected to evaluate the
        actions to do.

        :param info:
        :return:
        """

        if self.service_selected == "EC2":
            ec2id = self.tw_aws_grid.entry_widget.selected_row()
            npyscreen.notify("Exporting data to " + ec2id[1] + ".yml",
                             title="Information")
            time.sleep(2)

            # get the value in row selected
            self.ec2.export_instance_yaml(ec2id[1])

        elif self.service_selected == "Buckets":
            s3_id = self.tw_aws_grid.entry_widget.selected_row()
            npyscreen.notify("Exporting data to " + s3_id[0] + ".yml",
                             title="Information")
            time.sleep(2)
            self.s3.export_s3_yaml(s3_id[0])

        elif self.service_selected == "VPC":
            vpc_id = self.tw_aws_grid.entry_widget.selected_row()
            npyscreen.notify("Exporting data to " + vpc_id[0] + ".yml",
                             title="Information")
            time.sleep(2)
            self.network.export_vpc_yaml(vpc_id[0])

        elif self.service_selected == "Subnets":
            subnet_id = self.tw_aws_grid.entry_widget.selected_row()
            npyscreen.notify("Exporting data to " + subnet_id[0] + ".yml",
                             title="Information")
            time.sleep(2)
            self.network.export_subnets_yaml(subnet_id[0])

        elif self.service_selected == "ACLs Network":
            acl_id = self.tw_aws_grid.entry_widget.selected_row()
            npyscreen.notify("Exporting data to " + acl_id[0] + ".yml",
                             title="Information")
            time.sleep(2)
            self.network.export_acls_yaml(acl_id[0])
        elif self.service_selected == "Security Groups":
            security_group_id = self.tw_aws_grid.entry_widget.selected_row()
            npyscreen.notify("Exporting data to " + security_group_id[0] + ".yml",
                             title="Information")
            time.sleep(2)
            self.Security.export_security_group_yaml(security_group_id[0])
