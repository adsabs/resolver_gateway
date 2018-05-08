
import adsmutils as utils

def log_request(bibcode, user, link_type, url, referrer, client_id, real_ip):
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
        log_request.logger = utils.setup_logging(name_='linkout_clicks', attach_stdout=True)
        # replace the default formatter
        for handler in log_request.logger.handlers:
            formatter = u'%(asctime)s, %(process)d, %(linkout_clicks)s, ' \
                        u'%(user)s, %(link)s, %(bibcode)s, %(service)s, %(referer)s, %(client_id)s %(real_ip)s'
            handler.formatter = utils.get_json_formatter(logfmt=formatter)
    message = {'linkout_clicks':'resolver_linkout_click', 'user':user, 'link':link_type, 'bibcode':bibcode,
               'service':url, 'referer':referrer, 'client_id':client_id, 'real_ip':real_ip}
    log_request.logger.info(message)
