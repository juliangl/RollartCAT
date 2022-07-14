from django.http import HttpResponse
from django.template.loader import get_template
from .models import Value,Eventskater,Score,Scoreia,Event,Level,Levelcomponent
from decimal import Decimal

def render_to_pdf(template_src,context_dict):
    from io import BytesIO,StringIO
    from xhtml2pdf import pisa

    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def search_qoe(id_value,j):
    value=Value.objects.get(id=id_value)
    if j=="+3":
        return value.p3
    if j=="+2":
        return value.p2
    if j=="+1":
        return value.p1
    if j=="-3":
        return value.n3
    if j=="-2":
        return value.n2
    if j=="-1":
        return value.n1

def ScoreET(id_skater):
    total=0
    reg_eventskater=Eventskater.objects.get(skater=id_skater)
    reg_score=Score.objects.filter(event=reg_eventskater.id)
    for reg in reg_score:
        total=total+reg.total
    return total

def ScoreIA(id_skater):
    total=0
    reg_eventskater=Eventskater.objects.get(skater=id_skater)
    reg_score=Scoreia.objects.filter(event=reg_eventskater.id)
    for reg in reg_score:
        total=total+reg.total
    return total


def EnterEvent(request):
    id_event = request.session['idevent']  
    com=cat=lev=pro=None
    if id_event=="...":
        id_event=None
    if id_event:
        event=Event.objects.get(id=id_event)
        com = event.competition
        cat = event.category
        lev = event.level
        pro = event.program
        jud = event.judges
    return com,cat,lev,pro,jud

def CompoIA(request,com,id_events,code):
    HP=request.POST[code].replace(',','.')
    if HP != "...":
        compo=code[:-1]
        j=code[-1]
        if j=="1": 
            reg_scoreia=Scoreia.objects.filter(event=id_events,component=com).update(j1=HP)
        if j=="2": 
            reg_scoreia=Scoreia.objects.filter(event=id_events,component=com).update(j2=HP)
        if j=="3": 
            reg_scoreia=Scoreia.objects.filter(event=id_events,component=com).update(j3=HP)
        HP=Decimal(HP)
        return HP
    return 0        