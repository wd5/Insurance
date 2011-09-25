# -*- coding: utf-8 -*-
from django.utils import simplejson
import urllib
import urllib2
from django.conf import settings

import socket


FAKE_RESPONSE = {'status': 'OK', 'info':
    [{'full_name': 'TestCompany-1',
      'alias': 'testcomp1',
      'parameters': {'Evacuator': 'on',
                     'TheEmergencyCommissioner': 'on',
                     'PaymentWithoutInquiries': 'on',
                     'GatheringOfInquiries': 'on',
                     'TheModularInsuranceSum': 'on',
                     'NewForTheOld': 'on',
                     'TheObligatoryFranchize': 'on',
                     'AlternativenessOfFormsOfPayment': 'on',
                     }},
            {'full_name': 'TestCompany-2',
             'alias': 'testcomp2',
             'parameters': {'Evacuator': 'on',
                            'TheEmergencyCommissioner': '',
                            'PaymentWithoutInquiries': 'on',
                            'GatheringOfInquiries': '',
                            'TheModularInsuranceSum': 'on',
                            'NewForTheOld': '',
                            'TheObligatoryFranchize': 'on',
                            'AlternativenessOfFormsOfPayment': '',
                            }},
            {'full_name': 'TestCompany-3',
             'alias': 'testcomp3',
             'parameters': {'Evacuator': '',
                            'TheEmergencyCommissioner': 'on',
                            'PaymentWithoutInquiries': '',
                            'GatheringOfInquiries': 'on',
                            'TheModularInsuranceSum': '',
                            'NewForTheOld': 'on',
                            'TheObligatoryFranchize': '',
                            'AlternativenessOfFormsOfPayment': 'on',
                            }}]
}


def servlet_request(data):
    result = None
    if not settings.SERVLET_FAKE:
        encoded_data = urllib.urlencode(data)
        print "REQUEST:", encoded_data
        req = urllib2.Request(settings.SERVLET_URL, encoded_data)
        print "REQUEST:", req
        try:
            result = urllib2.urlopen(req).read()
            print "RESULT: ", result
        except socket.timeout:
            pass
    else:
        result = simplejson.dumps(FAKE_RESPONSE)
    return result

