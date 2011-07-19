from django.views.generic.simple import direct_to_template
from calc.forms import ServletTestForm
import sys,urllib,urllib2

def servlet_test(request):
    result = ''
    servlet_test_form = ServletTestForm(request.POST or None)
    form_fields = {}
    if servlet_test_form.is_valid():
        for k,v in servlet_test_form.cleaned_data.items():
            print >> sys.stderr, k, "=> ", v
            if v == True:
                #form_fields[k] = '1'
                #form_fields[k] = 'yes'
                form_fields[k] = 'on'
            elif v == False:
                #form_fields[k] = '0'
                #form_fields[k] = 'no'
                form_fields[k] = ''
            else:
                form_fields[k] = v

        print >> sys.stderr, "----------------------------------------"
        for k,v in form_fields.items():
            strpr = "%-28s%s" % (k,v)
            print >> sys.stderr, strpr
            #print >> sys.stderr, "key =", k, "\tval = ", v
        print >> sys.stderr, "----------------------------------------"

        url = 'http://localhost:8080/ServerIF/MatrixIF'
        #form_fields = servlet_test_form.cleaned_data
        form_data = urllib.urlencode(form_fields)
        req = urllib2.Request(url, form_data)
        response = urllib2.urlopen(req)
        result = response.read()
        # print >> sys.stderr, "result =", result
    extra_content = {'servlet_test_form':servlet_test_form,
                     'result':result}
    return direct_to_template(request, 'servlet_test.html',extra_content)




