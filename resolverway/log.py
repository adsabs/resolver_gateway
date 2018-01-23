
import adsputils as utils

def log_request(bibcode, user, link_type, url, referrer):
    """
    log to aws
    :param bibcode: 
    :param user: 
    :param link_type: 
    :param url: 
    :param referrer: 
    """
    # if logger doesn't exist initialize it
    # logger is a static variable
    if not hasattr(log_request, "logger"):
        log_request.logger = utils.setup_logging('linkout_clicks')
        # replace the default formatter
        for handler in log_request.logger.handlers:
            formatter = u'%(asctime)s,%(msecs)03d %(levelname)-8s [%(process)d:%(threadName)s:%(filename)s:%(lineno)d] ' \
                        u'%(user)s %(link)s %(bibcode)s %(service)s %(referer)s'
            handler.formatter = utils.get_json_formatter(logfmt=formatter)
    message = {'user':user, 'link':link_type, 'bibcode':bibcode, 'service':url, 'referer':referrer}
    log_request.logger.info(message)