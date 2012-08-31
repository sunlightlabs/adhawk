from django.conf.urls.defaults import *

from haystack.forms import FacetedSearchForm
from haystack.query import SearchQuerySet
from haystack.views import FacetedSearchView

sqs =SearchQuerySet().facet(
                      'funder_name'
                    ).facet(
                      'funder_party'
                    ).facet(
                      'funder_committee_type'
                    )

urlpatterns = patterns('haystack.views',
        url(r'^', FacetedSearchView(form_class=FacetedSearchForm,
                                        template='search/search.html',
                                        searchqueryset=sqs,
                                        results_per_page=15),
                                        name='haystack_search'),
        )
