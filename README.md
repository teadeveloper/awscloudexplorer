[![CodeFactor](https://www.codefactor.io/repository/github/teadeveloper/awscloudexplorer/badge?s=e65ddad85c3e993c6ec4a68e3fe046d32e67e472)](https://www.codefactor.io/repository/github/teadeveloper/awscloudexplorer)


<p align="center">
<img src="images/logo.png" width="750" height="250">
</p> 

[![asciicast](https://asciinema.org/a/1IkBGa3DB0xKuhCmWtOjeoYSx.svg)](https://asciinema.org/a/1IkBGa3DB0xKuhCmWtOjeoYSx)


### About The Project & Motivation

Updated:

Cloud Explorer was created as a proof of concept with the goal of learning AWS Boto and Python.

It is a tool for TUI lovers to explore the resources in AWS Cloud using a TUI (terminal user interface) instead of a GUI or AWS web console, 
Inspired in legacy tools like Norton Commander,  who were programming in the 80s or 90s are going to have a TUI experience using the
last technology in cloud.

This is the first MVP of Cloud Explorer, numerous things to be improved, new features etc… This MVP is stable, and you can use in your daily activities as a SysDev os Sysadmins, but don't forget it is a Proof of concept.

**Main features:**

**TUI:**

* Explore the AWS resources quickly from your terminal in Linux, Mac or Windows (CMD & WLS) using your console accounts or programmatic accounts.
* Get quickly the resource configuration.
* EC2 instances could be exported using customs keys.
* Support filters (if supported by AWS API).
* Export the configuration of a resource to YML. For example, save ec2 instance config to a yml.
* Export all resources VPCs, EC2s, Buckets etc. to YML, Excel, CSV, Markdown, HTML and String.

**AWS Services currently supported:**

- EC2
- VPC
- Subnets
- ACL Network
- Security groups
- Network Interfaces
- Buckets
- EBS
- EFS
- IAM
    - Users
    - Groups
    - Roles
    - Policies
    
* Lambda functions

**Pipeline Integration:**

If cloud explorer runs in some sort of automation (Jenkins, Rundeck, Git Hub actions etc.) there is a command to
export AWS services to a YML,Excel, CSV, Markdown, HTML and String.
  

<!-- GETTING STARTED -->
## Getting Started

Cloud Explorer is written in Python, and it works in Python 3.x and the current tests are running using Python 3.8.

### Prerequisites

1) Your terminal Width must be **140** otherwise you got this error:

```shell
.NotEnoughSpaceForWidget: Not enough space: max y and x = 58 , 117. Height and Width = 18 
```
To fix it, you have to resize your terminal in Linux, OSX or windows using your mouse :unamused:

2) Set your AWS credentials:

```shell
export AWS_ACCESS_KEY_ID="XXXXXXXXX"
export AWS_SECRET_ACCESS_KEY="XXXXXXXXX"
export AWS_SESSION_TOKEN="XXXXXXXXX"
```

### Installation

Using virtual environment:

```shell
# clone the repo
git clone https://github.com/teadeveloper/awscloudexplorer.git
cd awscloudexplorer/
# Create virtual environment
python3 -m venv ./venv && source venv/bin/activate
# Install pre-reqs for 
pip install -r requirements.txt
#Run cloud explorer
python cloudexplorer.py
```
<!-- USAGE EXAMPLES -->
## Usage

**Keyboard shortcuts**

1) Export menu: CRTL + ![image info](images/x.png) :  it opens the export menu to export.

![image info](images/exportall.png)

It opens the export menu to export all the resources to a file.



2) Export a resource to a YAML file, for example a EC2 configuration:

![image info](images/exporte.png)
It creates a file in YML format into the folder you are running the app. 
The file name is the name_of_the_resource.yml



3) Filters:

    - Select in the TUI any resource
    - CRTL + ![image info](images/f.png) to select a filter or custom filter (if suported). By dafult for example you
    can filter EC2 instances by its status.


**Pipeline Mode**

Find the python called exportall.py to export from command line or in a pipeline the AWS services to a file.

1. To export all ec2 instances to an excel file with all keys:

 ```shell
python exportall.py --ec2_all_keys --filename="ec2_all_keys.csv" --format=0
 ```
2. To export all ec2 instances to an excel file with basic keys:
```shell
Shellpython exportall.py --ec2ins --filename="ec2.csv" --format=0
```
3. To export all users to CSV:
```shell
python exportall.py --user --filename="users.csv" --format=1
```
   
4. To export all policies to HTML:

```shell
python exportall.py --policy --filename="policies.csv" --format=4
```

<!-- ROADMAP -->
## Roadmap

Python and Boto. If I have a new requirement, I will code it.

Things I would have like to add:

* Add pytest/testinfra to automatize tests.
* Add test to check the app works fine in several Python versions.
* Support new AWS services.


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<!-- LICENSE -->
## License

Distributed under Open Source (GPL-3.0)

## If you like it & Feedback

Feel free to send me an email with your feedback or open an issue. Feature requests are always welcome.

This personal project is open source (GPL-3.0), and I took me (and take me.) some time and efforts to design, to code, to make some researches and to test it in my personal AWS account. 

<!-- CONTACT -->
## Contact

Teadeveloper
:email: teadeveloper75@gmail.com

Images in this readme:

Keys from wikimedia: 
- https://commons.wikimedia.org/wiki/File:Preferences-desktop-keyboard-shortcuts.svg
- https://commons.wikimedia.org/wiki/Category:Keyboard_key_icons



