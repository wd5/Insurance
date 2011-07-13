from django.views.generic.simple import direct_to_template
from calc.forms import ServletTestForm
import sys,urllib,urllib2

def servlet_test(request):
    result = ''
    servlet_test_form = ServletTestForm(request.POST or None)
    if servlet_test_form.is_valid():
        url = 'http://localhost:8080/ServerIF/MatrixIF'
        form_fields = servlet_test_form.cleaned_data
        form_data = urllib.urlencode(form_fields)
        req = urllib2.Request(url, form_data)
        response = urllib2.urlopen(req)
        result = response.read()
        print >> sys.stderr, "result =", result
    extra_content = {'servlet_test_form':servlet_test_form,
                     'result':result}
    return direct_to_template(request, 'servlet_test.html',extra_content)




