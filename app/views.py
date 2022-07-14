from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib  import messages
from .models import Competition,Category,Level,Program,Eventskater,Skater,Event,Type,Element,Value,Score,Bonus,Bonusspin,Levelcomponent,Component,Scoreia,Actual
import random
from django.http import HttpResponse,HttpResponseRedirect
from django.views.generic import View, DetailView
from .utils import render_to_pdf,search_qoe,ScoreET,ScoreIA,EnterEvent,CompoIA
from decimal import Decimal



def handler500(request):
    return render(request, '500.html', status=500)

def handler404(request,exception):
    return render(request, '404.html', status=404)

#########################################################################################

def index (request):
    return render(request,'index.html')

def Login(request):
    if request.user.is_authenticated:
        return render(request,"index.html")
    else:
        messages.info(request,"Please login to acces.")
        return HttpResponseRedirect('/')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user != None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.error(request,"Enter your data correctly")
            return HttpResponseRedirect('/')
    return HttpResponseRedirect('/')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

#########################################################################################
################### Enter data
@login_required(login_url="/login")
def enter(request,next=None):
    if 'idcompetition' in request.session:
        del request.session['idcompetition']        
    if request.method == 'POST':
        idcom = request.POST.get('idcom')
        idlev = request.POST.get('idlev')
        idpro = request.POST.get('idpro')
        idcat = request.POST.get('idcat')
        reg_com = Competition.objects.get(id=idcom)
        reg_cat = Category.objects.get(id=idcat)
        reg_lev = Level.objects.get(id=idlev)
        reg_pro = Program.objects.get(id=idpro)      
        request.session['idcompetition'] = reg_com.id
        request.session['competition'] = reg_com.description
        request.session['idcategory'] = reg_cat.id
        request.session['category'] = reg_cat.description
        request.session['idlevel'] = reg_lev.id
        request.session['level'] = reg_lev.description
        request.session['idprogram'] = reg_pro.id
        request.session['program'] = reg_pro.description
        next_url = next
        if next_url:
            return redirect(next_url)
        else:
            return redirect('index')
    
    reg_com = Competition.objects.all()
    reg_cat = Category.objects.all()
    reg_lev = Level.objects.all()
    reg_pro = Program.objects.all()
    context = {'coms': reg_com,
               'cats':reg_cat,
               'pros':reg_pro,
               'levs':reg_lev}
    return render(request, "enter.html", context)


@login_required(login_url="/login")
def triaevent(request,next=None):
    if 'idevent' in request.session:
        del request.session['idevent']
    if 'skater' in request.session:
        del request.session['skater']
    if request.method == 'POST':
        id_event = request.POST['id_event']  
        if id_event!="...":
            request.session['idevent'] = id_event
            reg = Event.objects.get(id=id_event)
            request.session['idcompetition'] = reg.competition.id
            request.session['competition'] = reg.competition.description
            request.session['idcategory'] = reg.category.id
            request.session['category'] = reg.category.description
            request.session['idlevel'] = reg.level.id
            request.session['level'] = reg.level.description
            request.session['idprogram'] = reg.program.id
            request.session['program'] = reg.program.description
            next_url = next
            if next_url:
                return redirect(next_url)
            else:
                return redirect('index')
 
    reg_eve = Event.objects.all()
    context = {'events': reg_eve,
                'next':next}
    return render(request, "triaevent.html", context)

#########################################################################################
###################  Skater
@login_required(login_url='/login/')
def addskater(request):
    if 'idcompetition' in request.session:
        id_competition=request.session['idcompetition']
        id_level=request.session['idlevel']
        id_program=request.session['idprogram']
        id_category=request.session['idcategory']

        message=''
        if request.method == 'POST':
            id_skater = request.POST['id_skater']
            com=Competition.objects.get(id=id_competition)
            cat=Category.objects.get(id=id_category)
            lev=Level.objects.get(id=id_level)
            pro=Program.objects.get(id=id_program)
            ska=Skater.objects.get(id=id_skater)
            try:
                find=Eventskater.objects.get(competition=com,skater=ska)
                message='Skater: '+str(ska.name)+' already added on: '+str(com.description)
            except Exception as _:
                instance=Eventskater.objects.create(competition=com,category=cat,level=lev,program=pro,skater=ska,et=0,ia=0,deduction=0,total=0)
                component=Levelcomponent.objects.filter(level=lev.id)
                for compo in component:
                    instanceScoreIA=Scoreia.objects.create(event=instance,component=compo,total=0,j1=0,j2=0,j3=0)
        all_skater = Skater.objects.all()
        all_event = Eventskater.objects.filter(competition=id_competition,category=id_category,level=id_level,program=id_program)
        context = {'skas': all_skater,
                   'eves':all_event,
                   'message':message}
        return render(request,'addskater.html',context)
    else:
        return redirect('enter',next="addskater")

@login_required(login_url='/login/')
def delskater(request,event_id=None):
    reg = Eventskater.objects.get(id=event_id)
    reg.delete()
    return redirect(addskater)

#########################################################################################
###################  Skater music
@login_required(login_url='/login/')
def playmusic(request):
    if 'idevent' in request.session:
        com,cat,lev,pro,jud=EnterEvent(request)    
        if com!=None:             
            all_event = Eventskater.objects.filter(competition=com,category=cat,level=lev,program=pro).order_by('order')
            message=""
            context = {'eves':all_event,
                   'message':message}
            return render(request,'playmusic.html',context)
    else:
        return redirect('triaevent',next="playmusic")

#########################################################################################
################### Ordre of event
@login_required(login_url='/login/')
def genorder(request):
    if 'idcompetition' in request.session:
        del request.session['idcompetition']
    id_competition=None
    progress=None
    message=""
    if request.method == 'POST':
        id_competition = request.POST['id_competition']
        all_competition = Eventskater.objects.filter(competition=id_competition).values('competition','category','level','program').distinct()
        for reg in all_competition:
            id_category=reg['category']
            id_level=reg['level']
            id_program=reg['program'] 
                
            com=Competition.objects.get(id=id_competition)
            cat=Category.objects.get(id=id_category)
            lev=Level.objects.get(id=id_level)
            pro=Program.objects.get(id=id_program)
            try:
                find=Event.objects.get(competition=com,category=cat,level=lev,program=pro)
                message=message+" Order of "+str(com.description)+" "+str(cat.description)+" "+str(lev.description)+" "+str(pro.description)+" already generated"
            except Exception as _:
                add_eve=Event(competition=com,category=cat,level=lev,program=pro,judges=lev.judges)
                add_eve.save()

            all_event = Eventskater.objects.filter(competition=id_competition,category=id_category,level=id_level,program=id_program)
            total=all_event.count()
            lista=random.sample(range(total),total)
            i=0
            for ord in all_event:
                ord.order=lista[i]+1
                ord.save(update_fields=['order'])
                i=i+1

        progress="Update"

    reg_com = Competition.objects.all()   
    context = {'coms':reg_com,
               'id_competition_id':id_competition,
               'message':message,
               'progress':progress}
    return render(request,'genorder.html',context)

@login_required(login_url='/login/')
def pdforder(request):
    if 'idcompetition' in request.session:
        del request.session['idcompetition']
    if 'idevent' in request.session:
        id_event = request.session['idevent']  
        if id_event!="...":
            com = Event.objects.get(id=id_event).competition
            cat = Event.objects.get(id=id_event).category
            lev = Event.objects.get(id=id_event).level
            pro = Event.objects.get(id=id_event).program
            
            all_event = Eventskater.objects.filter(competition=com,category=cat,level=lev,program=pro).order_by('order')
            context={'eves':all_event,
                     'competition':com,
                     'category':cat,
                     'level':lev,
                     'program':pro,
            }
            pdf = render_to_pdf('ordre_pdf.html',context_dict=context)
            return HttpResponse(pdf, content_type='application/pdf')
    else:
        return redirect('triaevent',next="pdforder")

#########################################################################################
###################  Enter judges of event
@login_required(login_url='/login/')
def judges(request):
    all_event=None
    all_competition=Competition.objects.all()
    id_competition=None
    if request.method == 'POST':
        id_competition = request.POST['id_competition']  
        if id_competition=="...":
            id_competition=None
        if id_competition:
            com=Competition.objects.get(id=id_competition)   
            all_event=Event.objects.filter(competition=com) 
        if 'confirm' in request.POST:
            judges=request.POST.getlist('judges')
            i=0
            for eve in all_event:
                if judges[i]>'3':
                    judges[i]='3'
                eve.judges=judges[i]
                eve.save(update_fields=['judges'])
                i=i+1
    context = {'allcompetition':all_competition,
               'id_competition':id_competition,
               'eves':all_event}
    return render(request,'judges.html',context)

#########################################################################################
###################  Technical Panel
@login_required(login_url='/login/')
def technical(request):
    if 'idevent' in request.session:
        com,cat,lev,pro,jud=EnterEvent(request)    
        if com!=None: 

            factor=lev.factor
            judges=int(jud)
        
            all_component=Levelcomponent.objects.filter(level=lev)
            if int(lev.id)>1:
                val_component=((4),(4.5),(5),(5.5),(6))
            if int(lev.id)>4:
                val_component=((4),(4.5),(5),(5.5),(6),(6.5),(7))
            if int(lev.id)>7:
                val_component=((3),(3.5),(4),(4.5),(5),(5.5),(6),(6.5),(7),(7.5),(8))
            
            id_skater=None
            id_type=None
            id_element=None
            all_skater = Eventskater.objects.filter(competition=com,category=cat,level=lev,program=pro).order_by('order')
            all_type = Type.objects.all().order_by('description')
            all_element=None
            reg_skater=None
            reg_score=None
            reg_value=None
            reg_bonus=None
            reg_scoreia=None
            reg_event=None

            if 'skater' in request.session:
                id_skater=request.session['skater']
                reg_skater= Skater.objects.get(id=id_skater)
                reg_event = Eventskater.objects.get(competition=com,category=cat,level=lev,program=pro,skater=reg_skater.id)
                reg_score = Score.objects.filter(event=reg_event.id)
                reg_scoreia = Scoreia.objects.filter(event=reg_event.id)

            
            if request.method == 'POST':
                id_skater = request.POST['id_skater']
                request.session['skater'] = id_skater
                reg_skater= Skater.objects.get(id=id_skater)
                reg_event = Eventskater.objects.get(competition=com,category=cat,level=lev,program=pro,skater=reg_skater.id)
                reg_act=Actual.objects.all().delete()
                reg_act=Actual.objects.create(event=reg_event)
                reg_score = Score.objects.filter(event=reg_event.id)
                reg_scoreia = Scoreia.objects.filter(event=reg_event.id)
                request.session['regevent'] = reg_event.id
                if request.POST['id_type']!="...":
                    id_type = request.POST['id_type']
                    reg_type=Type.objects.get(id=id_type)
                    all_element = Value.objects.filter(type=id_type).order_by('element')
                    id_element=None
                if request.POST['id_element']!="...":
                    id_element = request.POST['id_element']
                    reg_element = Element.objects.get(id=id_element)
                    reg_value = Value.objects.get(type=reg_type.id,element=reg_element.id)
                    if id_type=="SSp" or id_type=="CoSP":
                        reg_bonus = Bonusspin.objects.filter(spin=id_element)
                    id_element=None
                    request.session['regvalue'] = reg_value.id
    
        context = {'alltype': all_type,
                   'allelement': all_element,
                   'allskater': all_skater,
                   'skater': reg_skater,
                   'eventskater': reg_event,
                   'scoreia': reg_scoreia,
                   'score': reg_score,
                   'value': reg_value,
                   'bonus': reg_bonus,
                   'id_skater': id_skater,
                   'id_element': id_element,
                   'id_type': id_type,
                   'factor': factor,
                   'judges': judges,
                   'valcomponent':val_component}
        return render(request,'technical.html',context)
    else:
        return redirect('triaevent',next="technical")


@login_required(login_url='/login/')
def contechnical(request):
    if request.method == 'POST':
        id_events = request.session['regevent']
        id_value  = request.session['regvalue']
        id_event  = request.session['idevent']
        event=Event.objects.get(id=id_event)
        judges=int(event.judges)
        bonus=0
        if 'id_bonus' in request.POST:
            id_bonus = request.POST['id_bonus']
            if id_bonus!="...":
                bonus=Bonusspin.objects.get(id=id_bonus).value
        comment = request.POST['comment']
        value=Value.objects.get(id=id_value)
        base=value.base
        tech=base+bonus
        j1=0
        j2=0
        j3=0
        jj3=""    
        if 'j1' in request.POST:
            jj1 = request.POST['j1']
            if jj1!='0':
                j1=search_qoe(id_value,jj1)
        if 'j2' in request.POST:
            jj2 = request.POST['j2']
            if jj2!='0':
                j2=search_qoe(id_value,jj2)
        if 'j3' in request.POST:
            jj3 = request.POST['j3']
            if jj3!='0':
                j3=search_qoe(id_value,jj3)
        qoe=Decimal((j1+j2+j3)/judges)
        total=tech+qoe
        add_con = Score(event=Eventskater.objects.get(id=id_events),element=Value.objects.get(id=id_value),comment=comment,base=base,bonus=bonus,tech=tech,qoe=qoe,j1=jj1,j2=jj2,j3=jj3,total=total)
        add_con.save()
    return redirect(technical)

@login_required(login_url='/login/')
def deltechnical(request,resultat_id=None):
    reg = Score.objects.get(id=resultat_id)
    reg.delete()
    return redirect(technical)

@login_required(login_url='/login/')
def conartistic(request):
    if request.method == 'POST':
        id_event  = request.session['idevent']
        event=Event.objects.get(id=id_event)
        judges=int(event.judges)
        id_events = request.session['regevent']
        reg_event=Eventskater.objects.get(id=id_events)
        factor=Decimal(float(reg_event.level.factor))
        level=Level.objects.get(id=reg_event.level.id)

        total=Decimal("0.0")
        com=Levelcomponent.objects.get(component='HP',level=level)
        if 'HP1' in request.POST:
            total=total+CompoIA(request,com,id_events,'HP1')
        if 'HP2' in request.POST:
            total=total+CompoIA(request,com,id_events,'HP2')
        if 'HP3' in request.POST:
            total=total+CompoIA(request,com,id_events,'HP3')
        total=(total/judges)*factor
        total=Decimal(total).quantize(Decimal("1.00"))
        reg_scoreia=Scoreia.objects.filter(event=id_events,component=com).update(total=total)

        total=Decimal("0.0")
        com=Levelcomponent.objects.get(component='P',level=level)
        if 'P1' in request.POST:
            total=total+CompoIA(request,com,id_events,'P1')
        if 'P2' in request.POST:
            total=total+CompoIA(request,com,id_events,'P2')
        if 'P3' in request.POST:
            total=total+CompoIA(request,com,id_events,'P3')
        total=(total/judges)*factor
        total=Decimal(total).quantize(Decimal("1.00"))
        reg_scoreia=Scoreia.objects.filter(event=id_events,component=com).update(total=total)

        total=Decimal("0.0")
        try:
            com=Levelcomponent.objects.get(component='C',level=level)
            if 'C1' in request.POST:
                total=total+CompoIA(request,com,id_events,'C1')
            if 'C2' in request.POST:
                total=total+CompoIA(request,com,id_events,'C2')
            if 'C3' in request.POST:
                total=total+CompoIA(request,com,id_events,'C3')
            total=(total/judges)*factor
            total=Decimal(total).quantize(Decimal("1.00"))
            reg_scoreia=Scoreia.objects.filter(event=id_events,component=com).update(total=total)
        except:
            pass

        total=Decimal("0.0")
        try:
            com=Levelcomponent.objects.get(component='T',level=level)
            if 'T1' in request.POST:
                total=total+CompoIA(request,com,id_events,'T1')
            if 'T2' in request.POST:
                total=total+CompoIA(request,com,id_events,'T2')
            if 'T3' in request.POST:
                total=total+CompoIA(request,com,id_events,'T3')
            total=(total/judges)*factor
            total=Decimal(total).quantize(Decimal("1.00"))
            reg_scoreia=Scoreia.objects.filter(event=id_events,component=com).update(total=total)
        except:
            pass

    return redirect(technical)


@login_required(login_url='/login/')
def condeduction(request):
    if request.method == 'POST':
        deduction = request.POST['deduction'].replace(",",".")
        id_event = request.session['regevent']
        id_skater = request.session['skater']
        reg_event=Eventskater.objects.filter(id=id_event)
        et=ScoreET(id_skater)
        ia=ScoreIA(id_skater)
        total=et+ia-Decimal(deduction)
        reg_event.update(deduction=deduction,et=et,ia=ia,total=total)

    return redirect(technical)

#########################################################################################
###################  PDF's for skater's
@login_required(login_url='/login/')
def result(request):
    from io import BytesIO,StringIO
    from xhtml2pdf import pisa
    from PyPDF2 import PdfFileMerger
    from django.template.loader import get_template
    from django.db.models import Sum
    
    if 'idevent' in request.session:
        com,cat,lev,pro,jud=EnterEvent(request)    
        if com!=None:    
            factor=lev.factor
            
            merger = PdfFileMerger()
            all_event = Eventskater.objects.filter(competition=com,category=cat,level=lev,program=pro)
            for skater in all_event:
                score=Score.objects.filter(event=skater.id)
                sumscore=Score.objects.filter(event=skater.id).aggregate(Sum('base'),Sum('bonus'),Sum('qoe'),Sum('total'))
                scoreia=Scoreia.objects.filter(event=skater.id)
                sumscoreia=Scoreia.objects.filter(event=skater.id).aggregate(Sum('total'))
                context={'row':skater,
                         'score':score,
                         's':sumscore,
                         'sia':sumscoreia,
                         'scoreia':scoreia,
                        'competition':com,
                        'category':cat,
                        'level':lev,
                        'factor':factor,
                        'program':pro,
                }
                template = get_template("resultat_pdf.html")
                html  = template.render(context)
                result = BytesIO()
                pdf = pisa.pisaDocument(
                    BytesIO(html.encode("UTF-8")), 
                    result,
                    encoding='UTF-8')
                if not pdf.err:
                    merger.append(result)
            output = BytesIO()
            merger.write(output)
            return HttpResponse(output.getvalue(), content_type='application/pdf')
    else:
        return redirect('triaevent',next="result")

#########################################################################################
###################  Punctuation Event Manager
@login_required(login_url='/login/')
def punctuation(request):
    reg_event=Actual.objects.all()[:1].get()
    skater = Eventskater.objects.filter(id=reg_event.event.id)
    context = {'skater': skater}
    return render(request,'punctuation.html',context)

#########################################################################################
###################  Classification of event
@login_required(login_url='/login/')
def classification(request):
    if 'idevent' in request.session:
        com,cat,lev,pro,jud=EnterEvent(request)    
        if com!=None:    
            all_event = Eventskater.objects.filter(competition=com,category=cat,level=lev,program=pro).order_by('-total')
            i=1
            for eve in all_event:
                Eventskater.objects.filter(id=eve.id).update(place=i)
                i=i+1
            context={'eves':all_event,
                     'competition':com,
                     'category':cat,
                     'level':lev,
                     'program':pro,
                    }
            pdf = render_to_pdf('classification_pdf.html',context_dict=context)
            return HttpResponse(pdf, content_type='application/pdf')    
    else:
        return redirect('triaevent',next="classification")

class modal(DetailView):
    model = Skater
    template_name = 'modal.html'