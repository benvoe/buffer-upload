import sys, yaml, shutil
from pathlib import Path
from random import shuffle
from getpass import getpass
from string import Template
from instaloader import Instaloader, Post

from .disk import load_config, load_hashtags, load_template
from .buffer import submit_to_buffer
from .insta import post_id_from_link

def initialize(basedir, username):
    template_dir = Path(__file__).parent / 'templates'
    default_template = (template_dir / 'caption.txt').open('r').read()

    config_dir = basedir / 'config' / username
    if config_dir.is_dir():
        raise FileExistsError('A configuration directory for "{}" already exists. Delete it and try again.'.format(username))

    # Build configuration
    conf_temp = load_template(template_dir / 'config.txt')

    conf_dict = dict()
    conf_dict['username'] = username

    print('Buffer login email:', end=' ')
    conf_dict['email'] = input()

    print('Buffer login password:', end=' ')
    conf_dict['password'] = getpass()

    print('Include hashtags from reposted image caption (Y/n):', end=' ')
    conf_dict['include'] = input() == 'Y'

    print('Maximum number of hashtags:', end=' ')
    hashtag_limit = int(input())
    conf_dict['limit'] = hashtag_limit if hashtag_limit > 0 and hashtag_limit < 30 else 30

    print('Hashtag separator (Default: " "):', end=' ')
    separator = input()
    conf_dict['separator'] = "'{}'".format(separator if separator is not '' else ' ')

    # Autoselect geckodriver
    #print('Select a driver for selenium:\n1: Firefox (geckodriver)\n2: Chrome/Chromium (chromedriver)\nChoice:', end=' ')
    driver_select = 1 #int(input())
    if driver_select is 1:
        driver = 'geckodriver'
    elif driver_select is 2:
        driver = 'chromedriver'
    else:
        raise AttributeError('Invalid choice for selenium webdriver.')
    conf_dict['driver'] = driver

    config_dir.mkdir(parents=True, exist_ok=False)

    (config_dir / 'blacklist.txt').open('w').write('instagood\nphotooftheday')
    (config_dir / 'hashtags.txt').open('w').write('photography\nnature')
    (config_dir / 'template.txt').open('w').write(default_template)
    (config_dir / 'config.yaml').open('w').write(conf_temp.substitute(**conf_dict))


def repost(basedir, username, ig_link):
    conf_dir = basedir / 'config' / username
    
    # Load configuration
    conf = load_config(conf_dir / 'config.yaml')
    hashtags = load_hashtags(conf_dir / 'hashtags.txt')
    blacklist = load_hashtags(conf_dir / 'blacklist.txt')
    caption = load_template(conf_dir / 'template.txt')

    # Get Instagram postId
    postId = post_id_from_link(ig_link)
    print('ImageId:', postId)

    # Download image with instaloader
    L = Instaloader(request_timeout=2, max_connection_attempts=3, quiet=True)
    P = Post.from_shortcode(L.context, postId)
    profile = P.profile
    post_hashtags = P.caption_hashtags
    print('Profile:', profile)

    if not L.download_post(P, basedir / 'temp'):
        print('Download of image failed! Please try again.')
        cleanup(basedir)
        sys.exit()

    # Select image and copy to post folder
    images = list(sorted((basedir / 'temp').glob('*.jpg')))
    images_len = len(images)
    
    if images_len > 1:
        print('Which image would you like to repost? (1-{}):'.format(images_len), end=' ')
        choice = int(input())
        assert 1 <= choice and choice <= images_len
        image = images[choice-1]
    else:
        image = images[0]
    
    post_dir = basedir / 'posts' / username
    post_dir.mkdir(parents=True, exist_ok=True)
    
    name = image.name.split('.')[0]
    target = post_dir / '{}.jpg'.format(name)
    shutil.copy(image, target)

    # Create caption and hashtags
    if conf['HASHTAG_INCLUDE']:
        post_hashtags = ['#' + hashtag for hashtag in post_hashtags if hashtag not in blacklist and hashtag not in hashtags]
        shuffle(post_hashtags)
        post_hashtags = post_hashtags
    else:
        post_hashtags = list()
    
    hashtags = ['#' + hashtag for hashtag in hashtags] + post_hashtags
    hashtags = hashtags[:conf['HASHTAG_LIMIT']]
    hashtags_str = conf['HASHTAG_SEPARATOR'].join(hashtags)

    caption_str = caption.substitute(username='@{}'.format(profile), hashtags=hashtags_str)

    open(post_dir / '{}.txt'.format(name), 'w').write(caption_str)

    print('Please enter location (or leave blank):', end=' ')
    location = input()

    submit_to_buffer(conf['IG_USER'], post_dir / '{}.txt'.format(name), post_dir / '{}.jpg'.format(name), location, conf['BUFFER_MAIL'], conf['BUFFER_PASS'], driver=conf['DRIVER'])

    cleanup(basedir)

def cleanup(basedir, all=False):
    if (basedir / 'temp').is_dir():
        shutil.rmtree(basedir / 'temp')
    if all:
        for d in list((basedir / 'posts').glob('*')):
            for f in list((basedir / 'posts' / d).glob('*')):
                f.unlink()
    