# Buffer Upload

Python script to easily download and add an Instagram image to Buffer queue

## Prerequisites

Clone the repository and enter it

    git clone https://github.com/benvoe/buffer-upload.git
    cd ./buffer-upload/

Create a virtual environment and enter it

    virtualenv venv --python=python3
    source venv/bin/activate

Install all required dependencies

    pip install -r requirements.txt

Per default, Buffer-Upload uses the Firefox WebDriver (geckodriver). (You need to have Firefox installed)
Download the latest webdriver version [here](https://github.com/mozilla/geckodriver/releases), unzip it and place it in the selenium folder

    utils/selenium/

## Getting Started

### Script Execution

You can run the script in two ways

    python buffer-upload.py ...

or

    ./buffer-upload.py ...

### Script Help

Find the script parameters by executing

    python buffer-upload.py --help

or 

    python buffer-upload.py <command> --help

### Initialization

You can initialize the script for your instagram account (multiple accounts are possible) with

    python3 buffer-upload.py init <ig_username>

Follow the instructions and insert the required information.
The initialization creates several files

    config/<ig_username>/config.yaml    # The configuration for buffer login and script execution
    config/<ig_username>/template.txt   # The template that is used as you post caption (Tags: $username, $hashtags)
    config/<ig_username>/hashtags.txt   # A list of your default hashtags (one hashtag per line)
    config/<ig_username>/blacklist.txt  # A list of hashtags that you want to exclude (one hashtag per line)

Do not hesitate to update these according to your wish.

## Usage

To now use the script

* Find a post on instagram, that you want to repost
* Click on "..." and then "Copy link"
* Execute the script as follows

    python buffer-upload.py repost <ig_username> <ig_post_link>

Follow the instructions and see the magic happening.

### Stay tidy: CleanUp

You can cleanup the `temp` directory with

    python buffer-upload.py cleanup

To also erase all posts from the `posts` directory, run

    python buffer-upload.py cleanup --all

## FAQ

### Can I use another Browser instead of Firefox?

Yes you can. You can also use webdrivers for Chrome, Edge, IE, Opera or Safari. 
Just download the respective webdriver [here](https://www.selenium.dev/documentation/en/getting_started_with_webdriver/browsers/) and place it in the selenium folder

    utils/selenium/

then specify the driver you want to use in your `config.yaml`.

    DRIVER: <your_driver>

NOTE: By using another webdriver you may encounter issues. (e.g. chromedriver does not support emojis in the caption)

### I have errors with webdrivers on MacOS. Shat should I do?

On MacOS you may have to execute 

    xattr -r -d com.apple.quarantine utils/selenium/<driver_name>

to be able to use the webdrivers.

