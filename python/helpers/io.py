'''The io module has several helper functions to read and log data'''

import json
import requests
import subprocess

from dotmap import DotMap

import helpers.collections as Collections

# Public methods
def shell(command):
    '''Execute a shell command.

    Args:
        command (striong): The shell command.

    Returns:
        string: The result from the shell command.
    '''
    return subprocess.check_output(command, shell = True).decode('utf-8').strip()

def get_stats_pihole(cfg, log):
    '''Get stats for the Pi-Hole instance.

    Args:
        cfg (DotMap): The configuration.
        log (Logger): The logger.

    Returns:
        tuple: (boolean, string, string, string, string): Success & Clients, ads blocked, ads percentage, dns queries.
    '''
    status = __get_json(cfg, log, 'status')    
    if "FTLnotrunning" in status:
        return (False, 0, 0, 0, 0)
        
    data = __get_json(cfg, log, 'summaryRaw')

    clients        = data['unique_clients']
    ads_blocked    = data['ads_blocked_today']
    ads_percentage = data['ads_percentage_today']
    dns_queries    = data['dns_queries_today']

    return (True, clients, ads_blocked, ads_percentage, dns_queries)

def get_stats_pihole_history(cfg, log):
    '''Get stats for the Pi-Hole instance's history.

    Args:
        cfg (DotMap): The configuration.
        log (Logger): The logger.

    Returns:
        tuple: (boolean, list, list): Success & Data for domains & ads.
    '''
    status = __get_json(cfg, log, 'status')    
    if "FTLnotrunning" in status:
        return (False, 0, 0)
        
    data = __get_json(cfg, log, 'overTimeData10mins')

    domains = Collections.dict_to_columns(cfg, data['domains_over_time'])
    ads     = Collections.dict_to_columns(cfg, data['ads_over_time'])

    return (True, domains, ads)

def read_cfg(module_settings):
    '''Read the configuration from file and store it in `settings`.

    Args:
        module_settings (DotMap): The global settings object the config has to be stored in.
    '''
    with open('config.json') as json_file:
        config = DotMap(json.load(json_file))
    module_settings.cfg = config
    
    with open('api-key.txt') as key_file:
        key = key_file.readline()
    module_settings.cfg.pihole.api_key = key

# Private methods
def __get_json(cfg, log, query):
    '''Get a `dict` from the specified JSON file.

    Args:
        cfg (DotMap): The configuration.
        query (string): The query.

    Returns:
        dict: The parsed JSON file.
    '''
    log.debug.obj(cfg, 'API request:', cfg.pihole.api_url + '?' + query)
    
    response = requests.get(cfg.pihole.api_url + '?' + query + '&auth=' + cfg.pihole.api_key.rstrip())
    
    responseObj = json.loads(response.text);
    
    log.debug.obj(cfg, 'API response:', responseObj)
    
    return responseObj
