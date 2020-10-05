from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView, DetailView
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.core.files.storage import FileSystemStorage, default_storage # https://stackoverflow.com/questions/26274021/simply-save-file-to-folder-in-django
from django.core.files import File
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from mysite.settings import EMAIL_HOST_USER 
from decimal import Decimal
from .models import Facture, PrestationDeService
from service.models import Service
from users.models import Psychologue, Client
from paiement.models import Paiement
from io import BytesIO
import os
from reportlab.lib.enums import TA_JUSTIFY  # @UnresolvedImport
from reportlab.lib.pagesizes import A4  # @UnresolvedImport
from reportlab.lib.units import inch  # @UnresolvedImport
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, Flowable  # @UnresolvedImport
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle  # @UnresolvedImport
from bootstrap_datepicker_plus import DatePickerInput  # @UnresolvedImport

# Create your views here.

class FactureCreateView(LoginRequiredMixin, CreateView):
    
    model = Facture
    fields = ('date', )
    
    def get_form(self):
        form = super().get_form()
        form.fields['date'].widget = DatePickerInput()
        return form
    
    def form_valid(self, form):
        psychologue = Psychologue.objects.get(id = self.request.user.id)
        form.instance.psychologue = psychologue
        self.client = Client.objects.get(id = self.kwargs['pk'])
        form.instance.client = self.client
        if not form.instance.is_active:
            form.instance.close_date = timezone.now()
            
        return super(FactureCreateView, self).form_valid(form)
    
    def get_success_url(self):
        #facture=Facture.objects.get(id=self.kwargs['pk'])
        """Detect the submit button used and act accordingly"""
        if 'facture-add' in self.request.POST:
            url = reverse_lazy('facture-add')
        else:
            url = reverse_lazy('clientdetails2', args=(self.client.id,))
        return url

class FactureUpdateView(LoginRequiredMixin, UpdateView):
    # la seule chose qui peut etre faite est de changer le status de la facture
    #devrait pouvoir se faire directement a partir du bouton
    model = Facture
    fields = ('date', 'is_active', )
    success_url = reverse_lazy('facture-list')
    
    def get_form(self):
        form = super().get_form()
        form.fields['date'].widget = DatePickerInput()
        return form
    
    def form_valid(self, form):
        if not form.instance.is_active:
            form.instance.close_date = timezone.now()
            
        return super(FactureUpdateView, self).form_valid(form)
    
class FactureDeleteView(LoginRequiredMixin, DeleteView):
    model = Facture
    context_object_name = 'facture_detail'
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the presation
        context['prestation_list'] = PrestationDeService.objects.filter(facture=self.kwargs['pk'])
        return context
    def get_success_url(self):
        client_id = Facture.objects.get(id = self.kwargs['pk']).client.id
        url = reverse_lazy('clientdetails2', args=(client_id,))
        return url
      
class FactureListView(ListView):
    model = Facture
    context_object_name = 'facture_list'
           
class FactureDetailView(DetailView):
    model = Facture
    context_object_name = 'facture_detail'
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the prestation
        facture_id = self.kwargs['pk']
        montant_details = Paiement.montant_verse.get_pmt_details(facture_id)
        pmt_total = montant_details['total_pmt']
        pmt_list = montant_details['pmt_list']
        if pmt_total is None:
            pmt_total = 0
        service_details = PrestationDeService.sous_total.get_bill_details(facture_id)
        service_list = service_details.pop('service_list')
        
        solde = round(Decimal(service_details['total']) - pmt_total,2)
        
        if solde < 0:
            solde_type = "Crédit"
        else:
            solde_type = "Solde"
        solde_dic = {'type':solde_type, 'montant':abs(solde)}
        context['service_list'] = service_list
        context['service_details'] = service_details
        context['pmt_total']= pmt_total
        context['pmt_list']= pmt_list
        context['solde']= solde_dic
        return context

def fermer_facture_view(request, pk):
    facture = Facture.objects.get(id=pk)
    facture.is_active = False
    facture.close_date = timezone.now()
    facture.save()
    return HttpResponseRedirect(reverse('facture-detail', args=(facture.id,)))
    
############################################################# PDF view ############################################################
# https://simpleisbetterthancomplex.com/tutorial/2016/08/08/how-to-export-to-pdf.html
# https://www.blog.pythonlibrary.org/2010/03/08/a-simple-step-by-step-reportlab-tutorial/
# https://medium.com/@vonkunesnewton/generating-pdfs-with-reportlab-ced3b04aedef
###################################################################################################################################

def pdf_view(request, pdf_file_name):
    fs = FileSystemStorage()
    filename = pdf_file_name
    if fs.exists(filename):
        with fs.open(filename) as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename='+ pdf_file_name
            return response
    else:
        return HttpResponseNotFound('The requested pdf was not found in our server.')

def envoyer_facture_view(request, pk):
    facture = Facture.objects.get(id=pk)
    client_email = facture.client.email
    subject = 'Welcome to DataFlair'
    message = 'Hope you are enjoying your Django Tutorials'
    recepient = str(client_email)
    send_mail(subject, 
        message, EMAIL_HOST_USER, [recepient], fail_silently = False)
    return HttpResponseRedirect(reverse('facture-detail', args=(facture.id, )))

def write_facture_pdf_view(request, pk):
    
    facture = get_object_or_404(Facture, id=pk)
    
    prestations_infos = PrestationDeService.sous_total.get_bill_details(pk)
    prestation_liste = prestations_infos['service_list']
    sous_total = prestations_infos['sous_total']
    montant_tvq = prestations_infos['tvq']
    montant_tps = prestations_infos['tps']
    total = prestations_infos['total']
    
    
#     if facture.is_active:
#         facture.is_active = False
#         facture.close_date = timezone.now()
#         facture.save()
    
    client_name = facture.client.first_name+" "+facture.client.last_name
    
    pdf_file_name = "Facture_"+client_name+"_"+facture.date.strftime('%d_%b_%Y')+".pdf"
    
    psy = get_object_or_404(Psychologue, id=facture.psychologue.id)
    tps = psy.tps
    tvq = psy.tvq
    
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename='+pdf_file_name
    
    pdf_buffer = BytesIO()
    facture_doc = SimpleDocTemplate(pdf_buffer, pagesize=A4,
                        rightMargin=72,leftMargin=72,
                        topMargin=72,bottomMargin=18)
    Story=[]
    logo = "media/media/logo/logo.png"
    full_name = client_name
    address_parts = [str(facture.client.door_number)+" "+facture.client.street_name.title(), 
                    facture.client.city.title()+", "+facture.client.province, 
                    facture.client.postal_code[:3].upper()+" "+facture.client.postal_code[-3:].upper()]
    # logo]
    # logo
    im = Image(logo, 3*inch, 1*inch)
    Story.append(im)
    Story.append(Spacer(1, 20))
    # date
    date_str = "Montreal, le " + facture.date.strftime('%d %b, %Y')
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    ptext = '<font size="10">%s</font>' % date_str
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 20))
    # Client's adress
    ptext = '<font size="10">%s</font>' % full_name
    Story.append(Paragraph(ptext, styles["Normal"]))       
    for part in address_parts:
        ptext = '<font size="10">%s</font>' % part.strip()
        Story.append(Paragraph(ptext, styles["Normal"]))   
    Story.append(Spacer(1, 20))
    
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    ptext = '<font size="10">%s</font>' % "Honoraires professionnels: "
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 10))
    
    # billing details
    data_table = []
    for prestation in prestation_liste:
        data_table.append([str(prestation.date.strftime("%Y-%m-%d")), str(prestation.qte)+" "+prestation.service.unit+" de "+prestation.service.nom
                      + " @ "+str(prestation.prix)+"$ / "+str(prestation.service.unit), str("%.2f" % prestation.montant())+" $"])
    
    data_table.append(['', 'Sous-Total', str("%.2f" % sous_total)+" $"])
    data_table.append(['', 'T.P.S.', str("%.2f" % montant_tps)+" $"])
    data_table.append(['', 'T.V.Q.', str("%.2f" % montant_tvq)+" $"])
    data_table.append(['', 'Total', str("%.2f" % total)+" $"])
    table_rows = len(data_table)
    t=Table(data_table)
    t.setStyle(TableStyle(
        [
            
            ('ALIGN', (-1,-table_rows), (-1,-1), 'RIGHT')]
        ))
    Story.append(t)
    Story.append(Spacer(1, 20))
    
    # tax number info    
    if psy.tps:
        tax_part = ['TPS : '+tps, 'TVQ : '+tvq]
        for part in tax_part:
            ptext = '<font size="10">%s</font>' % part.strip()
            Story.append(Paragraph(ptext, styles["Normal"]))
    facture_doc.build(Story)

    pdf = pdf_buffer.getvalue()
    pdf_buffer.close() 
    response.write(pdf)
    pdf_view(request, pdf_file_name)

    return response

def write_facture_pdf_view2(request, pk):
    facture = get_object_or_404(Facture, id=pk)
    prestations_infos = PrestationDeService.sous_total.get_bill_details(pk)
    prestation_liste = prestations_infos['service_list']
    sous_total = prestations_infos['sous_total']
    montant_tvq = prestations_infos['tvq']
    montant_tps = prestations_infos['tps']
    total = prestations_infos['total']
#     if facture.is_active:
#         facture.is_active = False
#         facture.close_date = timezone.now()
#         facture.save()
    client_name = facture.client.first_name+" "+facture.client.last_name
    
    pdf_file_name = "Facture "+client_name+" "+facture.date.strftime('%d %b %Y')+".pdf"
    
    psy = get_object_or_404(Psychologue, id=facture.psychologue.id)
    tps = psy.tps
    tvq = psy.tvq
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename='+pdf_file_name
    
    pdf_buffer = BytesIO()
    facture_doc = SimpleDocTemplate(pdf_buffer, pagesize=A4,
                        rightMargin=72,leftMargin=72,
                        topMargin=72,bottomMargin=18)
    Story=[]
    logo = "media/media/logo/logo.png"
    full_name = client_name
    address_parts = [str(facture.client.door_number)+" "+facture.client.street_name.title(), 
                    facture.client.city.title()+", "+facture.client.province, 
                    facture.client.postal_code[:3].upper()+" "+facture.client.postal_code[-3:].upper()]
    # logo]
    # logo
    im = Image(logo, 3*inch, 1*inch)
    Story.append(im)
    Story.append(Spacer(1, 20))
    # date
    date_str = "Montreal, le " + facture.date.strftime('%d %b, %Y')
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    ptext = '<font size="10">%s</font>' % date_str
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 20))
    # Client's adress
    ptext = '<font size="10">%s</font>' % full_name
    Story.append(Paragraph(ptext, styles["Normal"]))       
    for part in address_parts:
        ptext = '<font size="10">%s</font>' % part.strip()
        Story.append(Paragraph(ptext, styles["Normal"]))   
    Story.append(Spacer(1, 20))
    
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    ptext = '<font size="10">%s</font>' % "Honoraires professionnels: "
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 10))
    
    # billing details
    data_table = []
    for prestation in prestation_liste:
        data_table.append([str(prestation.date.strftime("%Y-%m-%d")), str(prestation.qte)+" "+prestation.service.unit+" de "+prestation.service.nom
                      + " @ "+str(prestation.prix)+"$ / "+str(prestation.service.unit), str("%.2f" % prestation.montant())+" $"])
    
    data_table.append(['', 'Sous-Total', str("%.2f" % sous_total)+" $"])
    data_table.append(['', 'T.P.S.', str("%.2f" % montant_tps)+" $"])
    data_table.append(['', 'T.V.Q.', str("%.2f" % montant_tvq)+" $"])
    data_table.append(['', 'Total', str("%.2f" % total)+" $"])
    table_rows = len(data_table)
    t=Table(data_table)
    t.setStyle(TableStyle(
        [
            
            ('ALIGN', (-1,-table_rows), (-1,-1), 'RIGHT')]
        ))
    Story.append(t)
    Story.append(Spacer(1, 20))
    
    # tax number info    
    if psy.tps:
        tax_part = ['TPS : '+tps, 'TVQ : '+tvq]
        for part in tax_part:
            ptext = '<font size="10">%s</font>' % part.strip()
            Story.append(Paragraph(ptext, styles["Normal"]))
    facture_doc.build(Story)
    pdf = pdf_buffer.getvalue()
    pdf_buffer.close() 
    response.write(pdf)
    
############     Method 1 saves ###################################
    try:
        os.makedirs(os.path.join(settings.MEDIA_ROOT, "clients", facture.client.username))
    except:
        pass
    
    save_name = os.path.join(settings.MEDIA_ROOT, "clients", facture.client.username, pdf_file_name)
    with open(save_name, "wb") as f:
        f.write(pdf)

######### create email #####################################################    
    if facture.client.is_male:
        titre = "Monsieur"
    else:
        titre = "Madame"
    email = EmailMessage(
    pdf_file_name,
    'Bonjour, '+ titre+ " " + facture.client.last_name + ', vous trouverez si joint votre facture du '+ str(facture.date),
    facture.psychologue.email,
    [facture.client.email],
    [],
    reply_to=[facture.psychologue.email],
    headers={'Message-ID': 'foo'},
    )
    email.attach_file(save_name)    
    email.send(fail_silently=False)
    return response
            
def write_recut_pdf_view(request, pk):
    
    class MCLine(Flowable):
        """
        Line flowable --- draws a line in a flowable
        http://two.pairlist.net/pipermail/reportlab-users/2005-February/003695.html
        
        """

    #----------------------------------------------------------------------
        def __init__(self, width, height=0):
            Flowable.__init__(self)
            self.width = width
            self.height = height
    
        #----------------------------------------------------------------------
        def __repr__(self):
            return "Line(w=%s)" % self.width
    
        #----------------------------------------------------------------------
        def draw(self):
            """
            draw the line
            """
            self.canv.line(450, self.height, self.width, self.height)
    

    facture = get_object_or_404(Facture, id=pk)
    if not facture.is_paid:
        facture.is_paid = True
        facture.paid_date = timezone.now()
    facture.save()
    prestations_infos = PrestationDeService.sous_total.get_bill_details(pk)
    prestation_liste = prestations_infos['service_list']
    sous_total = prestations_infos['sous_total']
    
    
    client_name = facture.client.first_name+" "+facture.client.last_name
    
    pdf_file_name = "Reçu "+client_name+" "+facture.date.strftime('%d %b %Y')+".pdf"
    
   
    
    psychologue_signature = facture.psychologue.first_name + " "+ facture.psychologue.last_name+", "+facture.psychologue.education
    psychologue_permis = facture.psychologue.permis_num
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename='+pdf_file_name
    
    pdf_buffer = BytesIO()
    facture_doc = SimpleDocTemplate(pdf_buffer, pagesize=A4,
                        rightMargin=72,leftMargin=72,
                        topMargin=72,bottomMargin=18)
    Story=[]
    logo = "media/media/logo/logo.png"
    full_name = client_name
    address_parts = [str(facture.client.door_number)+" "+facture.client.street_name.title(), 
                    facture.client.city.title()+", "+facture.client.province, 
                    facture.client.postal_code[:3].upper()+" "+facture.client.postal_code[-3:].upper()]
    # logo]
    # logo
    im = Image(logo, 3*inch, 1*inch)
    Story.append(im)
    Story.append(Spacer(1, 20))
    # date
    date_str = "Montreal, le " + facture.date.strftime('%d %b, %Y')
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    ptext = '<font size="10">%s</font>' % date_str
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 20))
    # Client's adress
    ptext = '<font size="10">%s</font>' % full_name
    Story.append(Paragraph(ptext, styles["Normal"]))       
    for part in address_parts:
        ptext = '<font size="10">%s</font>' % part.strip()
        Story.append(Paragraph(ptext, styles["Normal"]))   
    Story.append(Spacer(1, 20))
    # titre de la section
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    ptext = '<font size="10">%s</font>' % "Reçu pour services en psychologie : "
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 10))
    
    # billing details
    data_table = []
    for prestation in prestation_liste:
        data_table.append([str(prestation.date.strftime("%Y-%m-%d")), str(prestation.qte)+" "+prestation.service.unit+" de "+prestation.service.nom
                      + " @ "+str(prestation.prix)+"$ / "+str(prestation.service.unit), str("%.2f" % prestation.montant())+" $"])
    
    data_table.append(['', 'Montant (excluant taxes)', str("%.2f" % sous_total)+" $"])
    
    table_rows = len(data_table)
    t=Table(data_table)
    # 
    t.setStyle(TableStyle(
        [
            
            ('ALIGN', (-1,-table_rows), (-1,-1), 'RIGHT')]
        ))
    Story.append(t)
    Story.append(Spacer(1, 150))
        
#     if psy.tps:
#         tax_part = ['TPS : '+tps, 'TVQ : '+tvq]
#         for part in tax_part:
#             ptext = '<font size="10">%s</font>' % part.strip()
#             Story.append(Paragraph(ptext, styles["Normal"]))
           
    #signature
#     d = Drawing(100, 1)
#     Story.append(d)
    line = MCLine(315)
#      line.drawOn(self, 3*inch, 10*inch)
    Story.append(line)
#     signature_parts = [psychologue_signature, 'Psychologue,', 'Permis O.P.Q: '+ psychologue_permis]
#     for part in signature_parts:
#             ptext = '<font size="10">%s</font>' % part.strip()
#             
#             Story.append(Paragraph(ptext, styles["Normal"]))

    signature_data_table =[[psychologue_signature],['Psychologue,'],['Permis O.P.Q: '+ psychologue_permis]]
    table_rows = len(signature_data_table)
    t=Table(signature_data_table)
    t.hAlign ='RIGHT'
    Story.append(t)
    
    facture_doc.build(Story)
    pdf = pdf_buffer.getvalue()
    pdf_buffer.close()
    response.write(pdf)
    
    try:
        os.makedirs(os.path.join(settings.MEDIA_ROOT, "clients", facture.client.username))
    except:
        pass
    
    save_name = os.path.join(settings.MEDIA_ROOT, "clients", facture.client.username, pdf_file_name)
    with open(save_name, "wb") as f:
        f.write(pdf)

######### create email #####################################################    
    if facture.client.is_male:
        titre = "Monsieur"
    else:
        titre = "Madame"
    email = EmailMessage(
    pdf_file_name,
    'Bonjour, '+ titre+ " " + facture.client.last_name + ', vous trouverez si joint le reçu pour votre facture du '+ str(facture.date),
    facture.psychologue.email,
    [facture.client.email],
    [],
    reply_to=[facture.psychologue.email],
    headers={'Message-ID': 'foo'},
    )
#     method 1 ##############################################
    email.attach_file(save_name)
#     method 2##################################################
#     email.attach_file(os.path.join(file_url, pdf_file_name))
    
    email.send(fail_silently=False)
    return response
#  
    return response
    
    response.write(facture_doc)
  
    return response
    
#############################################################################################################
#
#Prestation de service
############################################################################################################## 
       
class PrestationDeServiceCreateView(LoginRequiredMixin, CreateView):
    model = PrestationDeService
    fields = ('date', 'service', 'qte', 'prix' )
    
    def get_form(self):
        form = super().get_form()
        form.fields['date'].widget = DatePickerInput()
        return form
    
    def form_valid(self, form):
        facture = Facture.objects.get(id=self.kwargs['pk'])
        form.instance.facture = facture
        return super(PrestationDeServiceCreateView, self).form_valid(form)
    
    def get_success_url(self):
        """Detect the submit button used and act accordingly"""
        if 'prestationdeservice-add' in self.request.POST:
            url = reverse_lazy('prestationdeservice-add', args=[self.kwargs['pk']])
        else:
            url = reverse_lazy('facture-detail', args=[self.kwargs['pk']])
        return url

class PrestationDeServiceUpdateView(LoginRequiredMixin, UpdateView):
    model = PrestationDeService
    fields = ('date', 'service', 'qte', 'prix' )
    def get_form(self):
        form = super().get_form()
        form.fields['date'].widget = DatePickerInput()
        return form
    
    def form_valid(self, form):
        facture = Facture.objects.get(id=self.kwargs['pk'])
        form.instance.facture = facture
        return super(PrestationDeServiceUpdateView, self).form_valid(form)
    
    def get_success_url(self):
        """Detect the submit button used and act accordingly"""
        if 'prestationdeservice-add' in self.request.POST:
            url = reverse_lazy('prestationdeservice-add', args=[self.kwargs['pk']])
        else:
            url = reverse_lazy('prestationdeservice-list',args=[self.kwargs['pk']])
        return url
    
class PrestationDeServiceDeleteView(LoginRequiredMixin, DeleteView):
    model = PrestationDeService
    success_url = reverse_lazy('prestationdeservice-list')
    
class PrestationDeServiceListView(ListView):
    model = PrestationDeService
    context_object_name = 'prestationdeservice_list'
    
class PrestationDeServiceDetailView(DetailView):
    model = PrestationDeService
    context_object_name = 'prestationdeservice_detail'
    
def get_service_attributes(request):
    service_id = request.GET.get('service_id', None)
    service = get_object_or_404(Service, id=service_id)
    prix = service.suggested_price
    data = {
        'prix': prix
    }
    return JsonResponse(data)   
    
