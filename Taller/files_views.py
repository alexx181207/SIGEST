#from io import BytesIO

from django.http import HttpResponse
from django.template.loader import get_template, render_to_string

from django.template.context import Context, make_context
from django.shortcuts import render, get_object_or_404  #, render_to_response 
#from xhtml2pdf import pisa




def render_to_pdf(url_template, contexto={}):
	template = get_template(url_template)
	html=template.render(contexto)
#	result = BytesIO()
#	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
#	if not pdf.err:
#		return HttpResponse(result.getvalue(), content_type="application/pdf")
	return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))







