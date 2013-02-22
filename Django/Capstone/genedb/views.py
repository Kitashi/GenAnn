from django.template import RequestContext, loader
from genedb.models import RefGene, LincRNA, LNCRNA, MicroRNA, GeneForm
from django.http import HttpResponse
import json


def index(request):
    t = loader.get_template('test.html')
    form = GeneForm(request.GET)
    c = RequestContext(request, {'form': form})
    return HttpResponse(t.render(c))
    
# using JSON forms
# def result(request):
    # t = loader.get_template('ui.html')
    # data = json.loads(request.GET)
    # # process data
    # for d in data:
        # print(d.name, d.message)
    
# using django's generated forms
def result(request):
    t = loader.get_template('result.html')
    form = GeneForm(request.GET)
    if form.is_valid():
        min = form.cleaned_data['startf']
        max = form.cleaned_data['endf']
        chrom = form.cleaned_data['chrom']
        strand = form.cleaned_data['strand']
    refg = RefGene.objects.all()
    mrna = MicroRNA.objects.all()
    lrna = LNCRNA.objects.all()
    irna = LincRNA.objects.all()
    # todo: What to do if the form is not valid?
    #       Right now, it causes a django error
    refg = formfilter(refg, min, max, chrom, strand)
    mrna = rformfilter(mrna, min, max, chrom, strand)
    lrna = rformfilter(lrna, min, max, chrom, strand)
    irna = rformfilter(irna, min, max, chrom, strand)
    
    c = RequestContext(request, {
        "refgene": refg,
        "microrna": mrna,
        "lncrna": lrna,
        "lincrna": irna
    })
    return HttpResponse(t.render(c))

def formfilter(set, min, max, chromosome, strandside):
    if min == None and max != None:
        set = set.filter(txend__lte=max)
    if min != None and max == None:
        set = set.filter(txstart__gte=min)
    if min != None and max != None:
        set = set.filter(txstart__range=(min, max))
        set = set.filter(txend__range=(min, max))
    if chromosome != "":
        set = set.filter(chrom__exact=chromosome)
    if strandside != "":
        set = set.filter(strand__exact=strandside)
    return set
    
def rformfilter(set, min, max, chromosome, strandside):
    if min == None and max != None:
        set = set.filter(end__lte=max)
    if min != None and max == None:
        set = set.filter(start__gte=min)
    if min != None and max != None:
        set = set.filter(start__range=(min, max))
        set = set.filter(end__range=(min, max))
    if chromosome != "":
        set = set.filter(chrom__exact=chromosome)
    if strandside != "":
        set = set.filter(strand__exact=strandside)
    return set