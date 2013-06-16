from django import template

from blog.models import Author


register = template.Library()


@register.inclusion_tag('blog/_authors_list.html')
def authors_list():
    authors = []
    try:
        all_authors = Author.objects.all()
        for a in all_authors:
            if len(a.live_entry_set()) > 0:
                authors.append(a)
    except:
        pass

    return {'authors': authors}
