# -*- coding: utf-8 -*-
from django.utils import simplejson
import urllib
import urllib2
from django.conf import settings

import socket


FAKE_RESPONSE = {'status': 'OK', 'info':
    [{'full_name': 'АльфаСтрахование',
      'company_comment': 'testComment-1',
      'alias': 'alfa',
      'score': '12345',
      'ourscore': '12333',
      'parameters': {'Evacuator': 'on',
                     'TheEmergencyCommissioner': 'on',
                     'PaymentWithoutInquiries': 'on',
                     'GatheringOfInquiries': 'on',
                     'TheModularInsuranceSum': 'on',
                     'NewForTheOld': 'on',
                     'TheObligatoryFranchize': 'on',
                     'AlternativenessOfFormsOfPayment': 'on',
                     }},
            {'full_name': 'Ингосстрах',
             'company_comment': 'testComment-2',
             'alias': 'ingos',
             'score': '12222',
             'ourscore': '12220',
             'parameters': {'Evacuator': 'on',
                            'TheEmergencyCommissioner': '',
                            'PaymentWithoutInquiries': 'on',
                            'GatheringOfInquiries': 'on',
                            'TheModularInsuranceSum': '',
                            'NewForTheOld': 'on',
                            'TheObligatoryFranchize': '',
                            'AlternativenessOfFormsOfPayment': 'on',
                            }},
            {'full_name': 'ГУТА-Страхование',
             'company_comment': 'testComment-3',
             'alias': 'guta',
             'score': '12345',
             'ourscore': '12333',
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


def servlet_request(data, servlet_type="kasko"):
    if servlet_type not in settings.SERVLET_URL:
        raise Exception("Unknown servlet type")
    url = settings.SERVLET_URL[servlet_type]
    result = None
    if not settings.SERVLET_FAKE:
        encoded_data = urllib.urlencode(data)
        if settings.DEBUG:
            print "REQUEST:", encoded_data
        print "URL:", url
        req = urllib2.Request(url, encoded_data)
        try:
            result = urllib2.urlopen(req).read()
            if settings.DEBUG:
                print "RESULT:", result
        except urllib2.URLError:
            return None
    else:
        result = simplejson.dumps(FAKE_RESPONSE)
    return result

