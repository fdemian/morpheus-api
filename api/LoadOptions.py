from tornado.options import define, options


def load_options(config_file):

    # Blog options
    define('blog_name', type=str, group='application', help='Name of the blog.')

    # General application settings
    define('port', type=int, group='application', help='Port to run the application from.')
    define('compress_response', type=bool, group='application', help='Whether or not to compress the response.')
    define('notifications_enabled', type=bool, group='application', help='Whether or not to enable notifications.')

    # Security options
    define('serve_https', type=bool, group='application', help='Whether to serve the application via HTTPS or not.')
    define('ssl_cert', type=str, group='application', help='Path to the SSL certificate.')
    define('ssl_key', type=str, group='application', help='Path to the SSL key.')
    define('cookie_secret', type=str, group='application', help='Cookie signing secret.')
    define('validate_user_email', type=bool, group='application', help='Whether to validate the user provided email.')

    define('max_login_tries', type=int, group='application', help='Maximum number of login tries.')
    define('login_delay_time_step', type=int, group='application', help='Delay time between logins.')
    define('lockout_time_window', type=int, group='application', help='Time window to lock the user out.')

    # Mail settings
    define('from_address', type=str, group='application', help='Address to send the confirmation mail from.')
    define('mail_template', type=str, group='application', help='Location of the mail template (relative to /static).')
    define('mail_subject', type=str, group='application', help='Subject of the confirmation mail.')
    define('mail_host', type=str, group='application', help='Host used to send emails.')
    define('mail_port', type=int, group='application', help='Port used to send emails.')

    # JWT settings.
    define('jwt_secret', type=str, group='application', help='Secret to use when encoding JWT Token.')
    define('jwt_algorithm', type=str, group='application', help='Algorithm to use when encoding JWT Token.')
    define('jwt_expiration_seconds', type=int, group='application', help='Time before the JWT token expires (seconds).')

    # Oauth settings
    define('facebook_api_key', type=str, group='application', help='Facebook API key.')
    define('facebook_api_secret', type=str, group='application', help='Facebook API key.')
    define('facebook_redirect_url', type=str, group='application', help='Facebook redirect URL.')
    define('facebook_icon_url', type=str, group='application', help='Icon URL.')

    define('google_oauth_key', type=str, group='application', help='Google Access Token.')
    define('google_oauth_secret', type=str, group='application', help='Google secret.')
    define('google_discovery_url', type=str, group='application', help='Discovery document for google.')
    define('google_redirect_url', type=str, group='application', help='Facebook redirect URL.')

    define('twitter_oauth_key', type=str, group='application', help='Twitter Access Token.')
    define('twitter_oauth_secret', type=str, group='application', help='Twitter secret.')

    define('github_client_id', type=str, group='application', help='Github client.')
    define('github_client_secret', type=str, group='application', help='Github secrets.')
    define('github_redirect_url', type=str, group='application', help='Facebook redirect URL.')
    define('github_icon_url', type=str, group='application', help='Icon URL.')

    define('yahoo_client_id', type=str, group='application', help='Facebook redirect URL.')
    define('yahoo_client_secret', type=str, group='application', help='Facebook redirect URL.')
    define('yahoo_redirect_url', type=str, group='application', help='Facebook redirect URL.')
    define('yahoo_icon_url', type=str, group='application', help='Icon URL.')

    define('database_user', type=str, group='application', help='Database user.')
    define('database_name', type=str, group='application', help='Database name.')
    define('database_port', type=str, group='application', help='Database port.')
    define('database_password', type=str, group='application', help='Database password.')

    options.parse_config_file(config_file)

    base_options = options.group_dict('application')
    google_oauth = dict(key=base_options['google_oauth_key'], secret=base_options['google_oauth_secret'])
    #google_oauth = { "key": base_options['google_oauth_key'], "secret": base_options['google_oauth_secret'] }
    base_options['google_oauth'] = google_oauth

    return base_options
