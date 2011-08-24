# -*- coding: utf-8 -*-
import json
import sys,urllib,urllib2
import settings

def servlet_request_real(url,data,dbg=False):
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
    
def servlet_request_fake(url,data,dbg=False):
    print >> sys.stderr, "servlet_request_fake(url,data,dbg=False):"
    out = {'status':'OK',
           'info':[{'full_name':'TestCompany-1',
                    'parameters':{'Evacuator':'on',
                                  'TheEmergencyCommissioner':'on',
                                  'PaymentWithoutInquiries':'on',
                                  'GatheringOfInquiries':'on',
                                  'TheModularInsuranceSum':'on',
                                  'NewForTheOld':'on',
                                  'TheObligatoryFranchize':'on',
                                  'AlternativenessOfFormsOfPayment':'on',
                                  }},
                   {'full_name':'TestCompany-2',
                    'parameters':{'Evacuator':'on',
                                  'TheEmergencyCommissioner':'',
                                  'PaymentWithoutInquiries':'on',
                                  'GatheringOfInquiries':'',
                                  'TheModularInsuranceSum':'on',
                                  'NewForTheOld':'',
                                  'TheObligatoryFranchize':'on',
                                  'AlternativenessOfFormsOfPayment':'',
                                  }},
                   {'full_name':'TestCompany-3',
                    'parameters':{'Evacuator':'',
                                  'TheEmergencyCommissioner':'on',
                                  'PaymentWithoutInquiries':'',
                                  'GatheringOfInquiries':'on',
                                  'TheModularInsuranceSum':'',
                                  'NewForTheOld':'on',
                                  'TheObligatoryFranchize':'',
                                  'AlternativenessOfFormsOfPayment':'on',
                                  }}
                   ]}
    return out

def servlet_request(url,data,dbg=False):
    try:
        settings.SERVLET_FAKE
    except AttributeError:
        settings.SERVLET_FAKE = False

    if not settings.SERVLET_FAKE:
        out = servlet_request_real(url,data,dbg=dbg)
    else:
        out = servlet_request_fake(url,data,dbg=dbg)
    return out
