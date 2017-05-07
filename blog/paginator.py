from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger

def getPages(request, objectlist):
    """get the paginator"""
    currentPage = request.GET.get('page', 1)
    paginator = Paginator(objectlist, 10)

    try:
        objectlist = paginator.page(currentPage)
    except PageNotAnInteger:
    # If page is not an integer, deliver first page.
        objectlist = paginator.page(1)
    except EmptyPage:
    # If page is out of range (e.g. 9999), deliver last page of results.
        objectlist = paginator.page(paginator.num_pages)


    objectlist = paginator.page(currentPage)

    return paginator, objectlist