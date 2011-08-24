# -*- coding: utf-8 -*-
import json
import sys,urllib,urllib2



def servlet_request(url,data,dbg=False):
    """
    Arguments:
    - `url`:
    - `data`:
    """
    if dbg:
        print >> sys.stderr, "url =", url
        print >> sys.stderr, "data =", data
    servlet_request_data = data
    form_data = urllib.urlencode(servlet_request_data)
    req = urllib2.Request(url, form_data)
    response = urllib2.urlopen(req)
    result_json = response.read()
    if dbg:
        print >> sys.stderr, "result_json =", result_json
    try:
        result = json.loads(result_json)
    except ValueError:
        print >> sys.stderr, "Servlet error. Status NOK: result_json =", result_json
        return {'status':'NOK','info':[]}
    return result
