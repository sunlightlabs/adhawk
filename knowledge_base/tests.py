"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from datetime import date

from django.test import TestCase
from django.db import IntegrityError
from django.db.models import ProtectedError
from django.utils import timezone

from knowledge_base.models import Ad,AdToCandidate,Author,Candidate,CandidateStatus,CommitteeDesignation,CommitteeType,ConnectedOrganization,Coverage,CoverageType,BroadcastType,Funder,FunderToCandidate,IncumbentChallengerStatus,InterestGroupCategory,Issue,IssueCategory,Market,Media,MediaProfile,MediaType,Source,Stance,Tag

class AdModelTest(TestCase):
    fixtures = [
            'tag.json',
            'market.json',
            'broadcasttype.json',
            'stance.json',
            'issue.json',
            'funder.json',
            'committeedesignation.json',
            'committeetype.json',
            'interestgroupcategory.json',
            'connectedorganization.json',
            ]

    def test_creating_a_new_Ad_and_saving_it_to_the_database(self):
        # get dependencies
        # media = Media.objects.all()[0]
        market = Market.objects.all()[0]
        broadcast_type = BroadcastType.objects.all()[0]
        stance = Stance.objects.all()[0]

        # Create a new Ad object 
        ad = Ad()
        ad.title = '"Spending" MO'
        
        # Add OTO relation
        #ad.media = media

        # save it
        ad.save()

        # make sure we can find it
        all_ads_in_database = Ad.objects.all()
        self.assertEquals(len(all_ads_in_database),1)
        only_ad_in_database = all_ads_in_database[0]
        self.assertEquals(only_ad_in_database,ad)

        # and check to make sure it saved its attributes
        self.assertEquals(only_ad_in_database.title,'"Spending" MO')
        self.assertEquals(only_ad_in_database.ingested,False)
        #self.assertEquals(only_ad_in_database.media,media)

        # add optional MTM fields
        ad.markets.add(market)
        ad.broadcast_types.add(broadcast_type)
        ad.stances.add(stance)

        # save it
        ad.save()

        # make sure we can still find it
        all_ads_in_database = Ad.objects.all()
        self.assertEquals(len(all_ads_in_database),1)
        only_ad_in_database = all_ads_in_database[0]
        self.assertEquals(only_ad_in_database, ad)

        # check that its MTM have been saved
        all_stances_for_only_ad_in_database = only_ad_in_database.stances.all()
        self.assertEquals(len(all_stances_for_only_ad_in_database),1)
        only_stance_for_only_ad_in_database = all_stances_for_only_ad_in_database[0]
        self.assertEquals(only_stance_for_only_ad_in_database,
                stance)

        all_markets_for_only_ad_in_database = only_ad_in_database.markets.all()
        self.assertEquals(len(all_markets_for_only_ad_in_database),1)
        only_market_for_only_ad_in_database = all_markets_for_only_ad_in_database[0]
        self.assertEquals(only_market_for_only_ad_in_database,
                market)

        all_broadcast_types_for_only_ad_in_database = only_ad_in_database.broadcast_types.all()
        self.assertEquals(len(all_broadcast_types_for_only_ad_in_database),1)
        only_broadcast_type_for_only_ad_in_database = all_broadcast_types_for_only_ad_in_database[0]
        self.assertEquals(only_broadcast_type_for_only_ad_in_database,
                broadcast_type)

        # make sure deleting the stance doesn't delete the ad
        stance.delete()
        all_ads_in_database = Ad.objects.all()
        self.assertEquals(len(all_ads_in_database),1)
        only_ad_in_database = all_ads_in_database[0]
        self.assertEquals(only_ad_in_database, ad)

        self.assertEquals(len(only_ad_in_database.stances.all()),0)

        # make sure deleting the market doesn't delete the ad
        market.delete()
        all_ads_in_database = Ad.objects.all()
        self.assertEquals(len(all_ads_in_database),1)
        only_ad_in_database = all_ads_in_database[0]
        self.assertEquals(only_ad_in_database, ad)

        self.assertEquals(len(only_ad_in_database.markets.all()),0)

        # make sure deleting the broadcast_type doesn't delete the ad
        broadcast_type.delete()
        all_ads_in_database = Ad.objects.all()
        self.assertEquals(len(all_ads_in_database),1)
        only_ad_in_database = all_ads_in_database[0]
        self.assertEquals(only_ad_in_database, ad)

        self.assertEquals(len(only_ad_in_database.broadcast_types.all()),0)
    
class AdToCandidateModelTest(TestCase):
    fixtures = ['ad.json',
            'media.json',
            'mediaprofile.json',
            'mediatype.json',
            'tag.json',
            'market.json',
            'broadcasttype.json',
            'stance.json',
            'issue.json',
            'funder.json',
            'committeedesignation.json',
            'committeetype.json',
            'candidates.json',
            'interestgroupcategory.json',
            'connectedorganization.json',
            'incumbentchallengerstatus.json',
            'candidatestatus.json'
            ]
    def test_creating_a_new_AdToCandidate_relation_and_saving_it(self):
        #get related objects
        ad = Ad.objects.all()[0]
        candidate = Candidate.objects.all()[0]

        # make a new AdToCandidate relation
        ad_to_candidate = AdToCandidate()
        ad_to_candidate.ad = ad
        ad_to_candidate.candidate = candidate
        ad_to_candidate.portrayal = 'NEG'

        # save it
        ad_to_candidate.save()
        
        # make sure we can find it
        all_ad_to_candidates_in_database = AdToCandidate.objects.all()
        self.assertEquals(len(all_ad_to_candidates_in_database),1)
        only_ad_to_candidate_in_database = all_ad_to_candidates_in_database[0]
        self.assertEquals(only_ad_to_candidate_in_database, ad_to_candidate)

        # check that its attributes have been saved
        self.assertEquals(only_ad_to_candidate_in_database.candidate,
                candidate)
        self.assertEquals(only_ad_to_candidate_in_database.ad,
                ad)

class AuthorModelTest(TestCase):
    def test_creating_a_new_Author_and_saving_it_to_the_database(self):
        # Create a new Author object 
        author = Author()
        author.name = "Joel Duffman"
        author.profile_page_url = "http://www.newslytimes.com/people/duffman"

        # Save it
        author.save()

        # make sure we can find it
        all_authors_in_database = Author.objects.all()
        self.assertEquals(len(all_authors_in_database),1)
        only_author_in_database = all_authors_in_database[0]
        self.assertEquals(only_author_in_database,author)

        # and check to make sure it saved its attributes
        self.assertEquals(only_author_in_database.name,'Joel Duffman')
        self.assertEquals(only_author_in_database.profile_page_url,"http://www.newslytimes.com/people/duffman")
    def test_verbose_name_for_profile_page_url_field(self):
        for field in Author._meta.fields:
            if field.name ==  'profile_page_url':
                self.assertEquals(field.verbose_name,'Profile page URL')

    def test_object_is_named_after_author(self):
        author = Author()
        author.name = "Joel Duffman"
        self.assertEquals(unicode(author),"Joel Duffman")

class BroadcastTypeModelTest(TestCase):
    def test_creating_a_new_BroadcastType_and_saving_it_to_the_database(self):
        # create a new BroadcastType object
        broadcast_type = BroadcastType()
        broadcast_type.name = "Television"

        # make sure we can save it
        broadcast_type.save()

        # make sure we can find it
        all_broadcast_types_in_database = BroadcastType.objects.all()
        self.assertEquals(len(all_broadcast_types_in_database),1)
        only_broadcast_type_in_database = all_broadcast_types_in_database[0]
        self.assertEquals(only_broadcast_type_in_database,broadcast_type)

        # and check to make sure it saved its attributes
        self.assertEquals(only_broadcast_type_in_database.name,"Television")

        
#
class CandidateModelTest(TestCase):
    fixtures = ['incumbentchallengerstatus.json',
                'candidatestatus.json',
                'issue.json',
                'stance.json']
    def test_creating_a_new_Candidate_and_saving_it_to_the_database(self):
        incumbent_challenger_status = IncumbentChallengerStatus.objects.all()[0]
        candidate_status = CandidateStatus.objects.all()[0]

        # Create a new Candidate object 
        candidate = Candidate()
        # add attibute values
        candidate.FEC_id = "J0EA00042"
        candidate.name = "JACK JOHNSON"
        candidate.party = "DEM"
        candidate.year_of_election = 2010
        candidate.street_one = "123 Fake Street"
        candidate.street_two = "Apt. 3"
        candidate.city = "New New York"
        candidate.state = "New York"
        candidate.zip_code = 90210
        # add foreign key relations
        candidate.incumbent_challenger_status = incumbent_challenger_status
        candidate.candidate_status = candidate_status

        # save it
        candidate.save()

        # check that we can find it
        all_candidates_in_database = Candidate.objects.all()
        self.assertEquals(len(all_candidates_in_database),1)
        only_candidate_in_database = all_candidates_in_database[0]
        self.assertEquals(only_candidate_in_database, candidate)

        # check that its attributes have been saved
        self.assertEquals(only_candidate_in_database.FEC_id,"J0EA00042")
        self.assertEquals(only_candidate_in_database.name,"JACK JOHNSON")
        self.assertEquals(only_candidate_in_database.party,"DEM")
        self.assertEquals(only_candidate_in_database.year_of_election,2010)
        self.assertEquals(only_candidate_in_database.street_one, 
                "123 Fake Street")
        self.assertEquals(only_candidate_in_database.street_two,"Apt. 3")
        self.assertEquals(only_candidate_in_database.city,"New New York")
        self.assertEquals(only_candidate_in_database.state,"New York")
        self.assertEquals(only_candidate_in_database.zip_code,90210)
        self.assertEquals(
                only_candidate_in_database.incumbent_challenger_status, 
                incumbent_challenger_status)
        self.assertEquals(only_candidate_in_database.candidate_status, 
                candidate_status)        

    def test_add_candidate_with_stance_and_coverage(self):
        # Create a basic candidate object
        # create IncumbentChallengerStatus object
        incumbent_challenger_status = IncumbentChallengerStatus()
        incumbent_challenger_status.code = 'O'
        incumbent_challenger_status.value = 'Open Seat'
        DESCRIPTION = "Open seats are defined as seats where the incumbent never sought re-election. There can be cases where an incumbent is defeated in the primary election. In these cases there will be two or more challengers in the general election."
        incumbent_challenger_status.description = DESCRIPTION
        #save it
        incumbent_challenger_status.save()

        # create CandidateStatus object
        candidate_status = CandidateStatus()
        candidate_status.code = 'C'
        candidate_status.value = 'Statutory candidate'
        DESCRIPTION = "The description of what the hell a statutory candidate is."
        candidate_status.description = DESCRIPTION
        # save it
        candidate_status.save()

        # Create a new Candidate object 
        candidate = Candidate()
        
        # add attibute values
        candidate.FEC_id = "J0EA00042"
        candidate.name = "JACK JOHNSON"
        candidate.party = "DEM"
        candidate.year_of_election = 2010
        candidate.street_one = "123 Fake Street"
        candidate.street_two = "Apt. 3"
        candidate.city = "New New York"
        candidate.state = "New York"
        candidate.zip_code = 90210
        
        # add foreign key relations
        candidate.incumbent_challenger_status = incumbent_challenger_status
        candidate.candidate_status = candidate_status

        # create a new Issue object
        issue = Issue.objects.all()[0]
        stance = Stance.objects.all()[0]

        # save it
        candidate.save()
        
        # add many-to-many relations
        candidate.stances.add(stance)
        
        # check that we can find it
        all_candidates_in_database = Candidate.objects.all()
        self.assertEquals(len(all_candidates_in_database),1)
        only_candidate_in_database = all_candidates_in_database[0]
        self.assertEquals(only_candidate_in_database, candidate)

        # check that stances have been saved
        all_stances_for_candidate_in_database = only_candidate_in_database.stances.all()
        self.assertEquals(len(all_stances_for_candidate_in_database),1)
        only_stance_for_candidate_in_database = all_stances_for_candidate_in_database[0]
        self.assertEquals(only_stance_for_candidate_in_database,stance)

class CandidateStatusModelTest(TestCase):
    def test_creating_a_new_CandidateStatus_and_saving_it_to_the_database(self):
        # Create a new CandidateStatus object 
        candidate_status = CandidateStatus()
        candidate_status.code = 'C'
        candidate_status.value = 'Statutory candidate'
        DESCRIPTION = "The description of what the hell a statutory candidate is."
        candidate_status.description = DESCRIPTION
        # check that we can save it
        candidate_status.save()

        # check that we can find it
        all_candidate_statuses_in_database = CandidateStatus.objects.all()
        self.assertEquals(len(all_candidate_statuses_in_database),1)
        only_candidate_status_in_database = all_candidate_statuses_in_database[0]
        self.assertEquals(only_candidate_status_in_database, candidate_status)

        # check that its attributes have been saved
        self.assertEquals(only_candidate_status_in_database.code,"C")
        self.assertEquals(only_candidate_status_in_database.value,
                "Statutory candidate")
        self.assertEquals(only_candidate_status_in_database.description, 
                DESCRIPTION)

class CommitteeDesignationModelTest(TestCase):
    def test_creating_a_new_CommitteeDesignation_and_saving_it_to_the_database(self):
        # create a new CommitteeDesignation object
        committee_designation = CommitteeDesignation()
        committee_designation.code = 'D'
        committee_designation.name = 'LEADERSHIP PAC'
        DESCRIPTION = "A PAC formed by a candidate. Leadership PACs help fund other candidates' campaigns in order to gain clout for that candidate. They are often used in bids for leadership posts or committee chairmanship."
        committee_designation.description = DESCRIPTION
        # check that we can save it
        committee_designation.save()

        # check that we can find it
        all_committee_designations_in_database = CommitteeDesignation.objects.all()
        self.assertEquals(len(all_committee_designations_in_database),1)
        only_committee_designation_in_database = all_committee_designations_in_database[0]
        self.assertEquals(only_committee_designation_in_database, committee_designation)

        # check that its attributes have been saved
        self.assertEquals(only_committee_designation_in_database.code,"D")
        self.assertEquals(only_committee_designation_in_database.name,
                "LEADERSHIP PAC")
        self.assertEquals(only_committee_designation_in_database.description, 
                DESCRIPTION)
#
class CommitteeTypeModelTest(TestCase):
    def test_creating_a_new_CommitteeType_and_saving_it_to_the_database(self):
        # create a new CommitteeType object
        committee_type = CommitteeType()
        committee_type.code = 'C'
        committee_type.name = 'Communication Cost'
        DESCRIPTION = "Organizations like corporations or unions may prepare communications for their employees or members that advocate the election of specific candidates and they must disclose them under certain circumstances. These are usually paid with direct corporate or union funds rather than from PACs."
        committee_type.description = DESCRIPTION
        # check that we can save it
        committee_type.save()

        # check that we can find it
        all_committee_types_in_database = CommitteeType.objects.all()
        self.assertEquals(len(all_committee_types_in_database),1)
        only_committee_type_in_database = all_committee_types_in_database[0]
        self.assertEquals(only_committee_type_in_database, committee_type)

        # check that its attributes have been saved
        self.assertEquals(only_committee_type_in_database.code,"C")
        self.assertEquals(only_committee_type_in_database.name,
                "Communication Cost")
        self.assertEquals(only_committee_type_in_database.description, 
                DESCRIPTION)
     
class ConnectedOrganizationModelTest(TestCase):
    def test_creating_a_new_ConnectedOrganization_and_saving_it_to_the_database(self):
        # Create a new ConnectedOrganization object 
        connected_organization = ConnectedOrganization()
        connected_organization.name = "NATIONAL ASSOCIATION OF HOME BUILDERS"
        DESCRIPTION = """One of the largest trade associations in the United States. Headquartered in Washington, DC, NAHB's mission is "to enhance the climate for housing and the building industry. Chief among NAHB's goals is providing and expanding opportunities for all consumers to have safe, decent and affordable housing."""
        connected_organization.description = DESCRIPTION 

        # make sure we can save it
        connected_organization.save()

        # make sure we can find it
        all_connected_organizations_in_database = ConnectedOrganization.objects.all()
        self.assertEquals(len(all_connected_organizations_in_database),1)
        only_connected_organization_in_database = all_connected_organizations_in_database[0]
        self.assertEquals(only_connected_organization_in_database,connected_organization)
        
        # and check to make sure it saved its attributes
        self.assertEquals(only_connected_organization_in_database.name, 
                "NATIONAL ASSOCIATION OF HOME BUILDERS")
        self.assertEquals(only_connected_organization_in_database.description,
                DESCRIPTION)

class CoverageModelTest(TestCase):
    fixtures = ['ad.json',
            'media.json',
            'mediaprofile.json',
            'mediatype.json',
            'market.json',
            'broadcasttype.json',
            'stance.json',
            'source.json',
            'author.json',
            'issue.json',
            'issuecategory.json',
            'candidates.json',
            'incumbentchallengerstatus.json',
            'candidatestatus.json',
            'funder.json',
            'committeedesignation.json',
            'committeetype.json',
            'interestgroupcategory.json',
            'connectedorganization.json',
            'tag.json',
            'coveragetype.json']

    def test_creating_a_new_Coverage_and_saving_it_to_the_database(self):
        # get related objects
        candidate1 = Candidate.objects.all()[0]
        candidate2 = Candidate.objects.all()[1]
        ad = Ad.objects.all()[0]
        author = Author.objects.all()[0]
        issue = Issue.objects.all()[0]
        stance = Stance.objects.all()[0]
        tag = Tag.objects.all()[0]
        source = Source.objects.all()[0]
        funder = Funder.objects.all()[0]
        coverage_type = CoverageType.objects.all()[0]

        # Create a new Coverage object
        coverage = Coverage()
        coverage.url = 'http://www.newslytimes.com/article/1045'
        coverage.headline = 'Clash of the titanium taxes'
        TEXT = """
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras
        pellentesque, augue nec aliquet iaculis, ligula lacus dictum dui, nec
        tincidunt mauris erat ut sapien. Quisque vulputate dolor est.
        Pellentesque habitant morbi tristique senectus et netus et malesuada
        fames ac turpis egestas. Aenean a diam sit amet purus auctor malesuada.
        Duis aliquam, orci quis tristique egestas, urna risus vestibulum odio,
        at vulputate quam orci feugiat diam. Aenean porttitor accumsan tortor,
        sed ornare erat iaculis in. Aliquam erat volutpat. Maecenas at accumsan
        tortor.

        Nunc pharetra semper convallis. Sed nulla risus, molestie vitae mollis
        non, ornare vel massa. Class aptent taciti sociosqu ad litora torquent
        per conubia nostra, per inceptos himenaeos. Vestibulum consequat
        pulvinar ipsum at aliquet. Morbi sem lectus, ultricies laoreet iaculis
        quis, consectetur dictum orci. Sed blandit viverra tempus. Etiam
        lobortis ornare risus in vestibulum. Fusce hendrerit tellus ut nibh
        facilisis vehicula. Duis placerat, neque ut luctus ornare, nisl eros
        volutpat nulla, in suscipit est mi eget nulla. Donec eu eros in odio
        consectetur volutpat quis ac felis. Sed dignissim nulla vel justo
        accumsan eu aliquam justo consectetur. Curabitur scelerisque ornare
        purus, eget auctor tellus convallis at. Duis arcu elit, placerat sit
        amet ultricies nec, sodales vel tortor. Cum sociis natoque penatibus et
        magnis dis parturient montes, nascetur ridiculus mus. Nulla dapibus
        libero vel nunc egestas sed luctus lacus malesuada. In hac habitasse
        platea dictumst.

        Suspendisse nec nisl nec erat dapibus interdum eget a risus. Integer
        gravida pulvinar ultricies. Class aptent taciti sociosqu ad litora
        torquent per conubia nostra, per inceptos himenaeos. Nulla ultrices orci
        sed mi ullamcorper euismod iaculis in sem. Nullam tempor, felis sit amet
        laoreet varius, lectus arcu dictum arcu, eu adipiscing mauris justo et
        leo. Pellentesque habitant morbi tristique senectus et netus et
        malesuada fames ac turpis egestas. Phasellus tristique ligula ac magna
        venenatis adipiscing vel at ante. Proin sit amet dignissim lacus. Cras
        condimentum mauris faucibus velit porttitor non pulvinar felis blandit.
        Aliquam lacinia quam vitae nibh vulputate rutrum. Sed quis purus ut odio
        vulputate sodales. Morbi at hendrerit orci. Curabitur urna mi, tristique
        et vehicula eget, dapibus ac felis.

        Praesent auctor semper arcu, ut porta neque imperdiet eget. Pellentesque
        nec lacinia nisi. Aenean mollis laoreet ligula, eu viverra quam
        tincidunt nec. In tempor urna ac dolor faucibus mattis. Nam sit amet
        nulla erat, quis accumsan arcu. In porta mattis magna, quis dapibus
        metus venenatis vel. In semper, nunc at pretium mollis, erat urna
        volutpat est, in pellentesque dui lacus et massa. Nullam sit amet dui
        vitae urna accumsan pharetra posuere auctor felis. Cras sed hendrerit
        enim. Curabitur bibendum lorem sit amet tellus interdum eu tincidunt
        massa auctor. Nam vitae risus purus, eget sollicitudin urna.
        Pellentesque et consequat orci.

        Mauris ultricies metus non arcu pharetra at accumsan ligula tincidunt.
        Maecenas iaculis, nisi a convallis suscipit, nisi ligula sollicitudin
        enim, quis tincidunt sem nisl eget tellus. Nullam euismod arcu sit amet
        tellus tempus a elementum sapien venenatis. Etiam a mi ut nunc gravida
        scelerisque. Sed id imperdiet odio. Ut feugiat interdum nulla non
        iaculis. Mauris pharetra odio eu risus porttitor rutrum. Vestibulum ante
        ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae;
        Fusce rutrum tempus quam, eget posuere neque imperdiet non. Aliquam at
        tellus mauris, ut eleifend enim. Quisque eu libero arcu, at gravida
        massa. In hendrerit, neque vitae tincidunt convallis, felis elit auctor
        arcu, adipiscing dapibus leo nisi euismod purus. Nam ornare interdum
        ipsum, eget laoreet risus pellentesque et. """
        coverage.text = TEXT
        DATE = date.today()
        coverage.date = DATE

        # add FK relations
        coverage.source = source
        coverage.coverage_type = coverage_type

        # save it
        coverage.save()

        # make sure we can find it
        all_coverages_in_database = Coverage.objects.all()
        self.assertEquals(len(all_coverages_in_database),1)
        only_coverage_in_database = all_coverages_in_database[0]
        self.assertEquals(only_coverage_in_database,coverage)
        
        # and check to make sure it saved its attributes
        self.assertEquals(only_coverage_in_database.url,
                'http://www.newslytimes.com/article/1045')
        self.assertEquals(only_coverage_in_database.headline,
                'Clash of the titanium taxes')
        self.assertEquals(only_coverage_in_database.text,TEXT)
        self.assertEquals(only_coverage_in_database.date,DATE)
        self.assertEquals(only_coverage_in_database.source,source)
        self.assertEquals(only_coverage_in_database.coverage_type,coverage_type)

        # make sure deleting the source raises an error
        self.assertRaises(ProtectedError,source.delete)

        # add MTM relations
        coverage.authors.add(author)
        coverage.ads.add(ad)
        coverage.candidates.add(candidate1)
        coverage.candidates.add(candidate2)
        coverage.funders.add(funder)
        coverage.tags.add(tag)
        coverage.issues.add(issue)
        coverage.stances.add(stance)

        # save it
        coverage.save()

        # check that we can find it
        all_coverages_in_database = Coverage.objects.all()
        self.assertEquals(len(all_coverages_in_database),1)
        only_coverage_in_database = all_coverages_in_database[0]
        self.assertEquals(only_coverage_in_database, coverage)

        # check that authors have been saved
        all_authors_for_coverage_in_database = only_coverage_in_database.authors.all()
        self.assertEquals(len(all_authors_for_coverage_in_database),1)
        only_author_for_coverage_in_database = all_authors_for_coverage_in_database[0]
        self.assertEquals(only_author_for_coverage_in_database,author)
        
        # check that candidates have been saved
        all_candidates_for_coverage_in_database = only_coverage_in_database.candidates.all()
        self.assertEquals(len(all_candidates_for_coverage_in_database),2)
        self.assertIn(candidate1,all_candidates_for_coverage_in_database)
        self.assertIn(candidate2,all_candidates_for_coverage_in_database)
        
        # check that funders have been saved
        all_funders_for_coverage_in_database = only_coverage_in_database.funders.all()
        self.assertEquals(len(all_funders_for_coverage_in_database),1)
        only_funder_for_coverage_in_database = all_funders_for_coverage_in_database[0]
        self.assertEquals(only_funder_for_coverage_in_database,funder)
        
        # check that tags have been saved
        all_tags_for_coverage_in_database = only_coverage_in_database.tags.all()
        self.assertEquals(len(all_tags_for_coverage_in_database),1)
        only_tag_for_coverage_in_database = all_tags_for_coverage_in_database[0]
        self.assertEquals(only_tag_for_coverage_in_database,tag)
        
        # check that issues have been saved
        all_issues_for_coverage_in_database = only_coverage_in_database.issues.all()
        self.assertEquals(len(all_issues_for_coverage_in_database),1)
        only_issue_for_coverage_in_database = all_issues_for_coverage_in_database[0]
        self.assertEquals(only_issue_for_coverage_in_database,issue)
        
        # check that ads have been saved
        all_ads_for_coverage_in_database = only_coverage_in_database.ads.all()
        self.assertEquals(len(all_ads_for_coverage_in_database),1)
        only_ad_for_coverage_in_database = all_ads_for_coverage_in_database[0]
        self.assertEquals(only_ad_for_coverage_in_database,ad)
        
        # check that stances have been saved
        all_stances_for_coverage_in_database = only_coverage_in_database.stances.all()
        self.assertEquals(len(all_stances_for_coverage_in_database),1)
        only_stance_for_coverage_in_database = all_stances_for_coverage_in_database[0]
        self.assertEquals(only_stance_for_coverage_in_database,stance)

class CoverageTypeModelTest(TestCase):
    def test_creating_a_new_CoverageType_and_saving_it_to_the_database(self):
        # create a new BroadcastType object
        coverage_type = CoverageType()
        coverage_type.name = "Blog post"

        # make sure we can save it
        coverage_type.save()

        # make sure we can find it
        all_coverage_types_in_database = CoverageType.objects.all()
        self.assertEquals(len(all_coverage_types_in_database),1)
        only_coverage_type_in_database = all_coverage_types_in_database[0]
        self.assertEquals(only_coverage_type_in_database,coverage_type)
        
        # and check to make sure it saved its attributes
        self.assertEquals(only_coverage_type_in_database.name,"Blog post")
#        
class FunderModelTest(TestCase):
    fixtures = ['interestgroupcategory.json',
            'connectedorganization.json',
            'committeedesignation.json',
            'committeetype.json',
            'stance.json',
            'issue.json',
            'issuecategory.json']

    def test_creating_a_new_Funder_and_saving_it_to_the_database(self):
        # get FK-related objects
        committee_designation = CommitteeDesignation.objects.all()[0]
        committee_type = CommitteeType.objects.all()[0]
        interest_group_category = InterestGroupCategory.objects.all()[0]
        connected_organization = ConnectedOrganization.objects.all()[0]

        # Create a new Funder object
        funder = Funder()
        funder.FEC_id = 'C00012229'
        funder.name = 'Fingerlicans for John Jackson'
        funder.filing_frequency = 'Q'
        funder.party = 'REP'
        funder.treasurer_name = 'Hermes Conrad'
        funder.street_one = '2504 FAIRBANKS STREET'
        funder.street_two = ''
        funder.state = 'AK'
        funder.zip_code = '99503'

        # add foreign key constraints
        funder.interest_group_category = interest_group_category
        funder.committee_type = committee_type
        funder.committee_designation = committee_designation
        
        # save it
        funder.save()
        
        # check that we can find it
        all_funders_in_database = Funder.objects.all()
        self.assertEquals(len(all_funders_in_database),1)
        only_funder_in_database = all_funders_in_database[0]
        self.assertEquals(only_funder_in_database, funder)

        # check that its attributes have been saved
        self.assertEquals(only_funder_in_database.FEC_id,"C00012229")
        self.assertEquals(only_funder_in_database.name,
                'Fingerlicans for John Jackson')
        self.assertEquals(only_funder_in_database.filing_frequency,'Q')
        self.assertEquals(only_funder_in_database.party,'REP')
        self.assertEquals(only_funder_in_database.treasurer_name, 
                'Hermes Conrad')
        self.assertEquals(only_funder_in_database.street_one, 
                '2504 FAIRBANKS STREET')
        self.assertEquals(only_funder_in_database.street_two,'')
        self.assertEquals(only_funder_in_database.state,'AK')
        self.assertEquals(only_funder_in_database.zip_code,'99503')
        self.assertEquals(only_funder_in_database.interest_group_category,
                interest_group_category)
        self.assertEquals(only_funder_in_database.committee_type,committee_type)
        self.assertEquals(only_funder_in_database.committee_designation,
                committee_designation)
        self.assertEquals(only_funder_in_database.connected_organization,
                None)

        # add connected organization
        funder.connected_organization = connected_organization
        funder.save()

        # check that we can find it
        all_funders_in_database = Funder.objects.all()
        self.assertEquals(len(all_funders_in_database),1)
        only_funder_in_database = all_funders_in_database[0]
        self.assertEquals(only_funder_in_database, funder)

        # check that its attributes have been saved
        self.assertEquals(only_funder_in_database.connected_organization,
                connected_organization)

        # make sure that deleting the FK-related objects doesn't delete the
        # funder
        self.assertRaises(ProtectedError,interest_group_category.delete)
        
        self.assertRaises(ProtectedError,committee_type.delete)
        
        connected_organization.delete()
        check_funder = Funder.objects.all()[0]
        self.assertEquals(check_funder,funder)

    def test_creating_Funder_model_with_Stance(self):
        # get FK-related objects
        committee_designation = CommitteeDesignation.objects.all()[0]
        committee_type = CommitteeType.objects.all()[0]
        interest_group_category = InterestGroupCategory.objects.all()[0]
        connected_organization = ConnectedOrganization.objects.all()[0]

        # get MTM-related objects
        stance = Stance.objects.all()[0]

        # Create a new Funder object
        funder = Funder()
        funder.FEC_id = 'C00012229'
        funder.name = 'Fingerlicans for John Jackson'
        funder.filing_frequency = 'Q'
        funder.party = 'REP'
        funder.treasurer_name = 'Hermes Conrad'
        funder.street_one = '2504 FAIRBANKS STREET'
        funder.street_two = ''
        funder.state = 'AK'
        funder.zip_code = '99503'

        # add foreign key relations
        funder.interest_group_category = interest_group_category
        funder.committee_type = committee_type
        funder.committee_designation = committee_designation
        
        # save it
        funder.save()

        # add manytomany relation
        funder.stances.add(stance)

        # update it
        funder.save()

        # check that we can find it
        all_funders_in_database = Funder.objects.all()
        self.assertEquals(len(all_funders_in_database),1)
        only_funder_in_database = all_funders_in_database[0]
        self.assertEquals(only_funder_in_database, funder)

        # check that its attributes have been saved
        all_stances_for_only_funder_in_database = only_funder_in_database.stances.all()
        self.assertEquals(len(all_stances_for_only_funder_in_database),1)
        only_stance_for_only_funder_in_database = all_stances_for_only_funder_in_database[0]
        self.assertEquals(only_stance_for_only_funder_in_database,
                stance)

        # make sure deleting the stance doesn't delete the Funder
        stance.delete()
        all_funders_in_database = Funder.objects.all()
        self.assertEquals(len(all_funders_in_database),1)
        only_funder_in_database = all_funders_in_database[0]
        self.assertEquals(only_funder_in_database, funder)

        self.assertEquals(len(only_funder_in_database.stances.all()),0)
        
class FunderToCandidateModelTest(TestCase):
    fixtures = ['funder.json',
            'interestgroupcategory.json',
            'connectedorganization.json',
            'committeedesignation.json',
            'committeetype.json',
            'stance.json',
            'issue.json',
            'issuecategory.json',
            'candidate.json',
            'incumbentchallengerstatus.json',
            'candidatestatus.json']
    def test_create_a_new_FunderToCandidate_relation(self):
        # get candidate object and funder object
        candidate_from_db = Candidate.objects.all()[0]
        funder_from_db = Funder.objects.all()[0]

        # add funder-to-candidate relation
        funder_to_candidate = FunderToCandidate(funder=funder_from_db,
                candidate=candidate_from_db,
                relationship='Primary Campaign Committee')

        # save it
        funder_to_candidate.save()

        # make sure we can find it
        all_funder_to_candidates_in_database = FunderToCandidate.objects.all()
        self.assertEquals(len(all_funder_to_candidates_in_database),1)
        only_funder_to_candidate_in_database = all_funder_to_candidates_in_database[0]
        self.assertEquals(only_funder_to_candidate_in_database, funder_to_candidate)

        # check that its attributes have been saved
        self.assertEquals(only_funder_to_candidate_in_database.candidate,
                candidate_from_db)
        self.assertEquals(only_funder_to_candidate_in_database.funder,
                funder_from_db)

class IncumbentChallengerStatusModelTest(TestCase):
    def test_creating_a_new_IncumbentChallengerStatus_and_saving_it_to_the_database(self):
        # TODO: Create a new IncumbentChallengerStatus object 
        incumbent_challenger_status = IncumbentChallengerStatus()
        incumbent_challenger_status.code = 'O'
        incumbent_challenger_status.value = 'Open Seat'
        DESCRIPTION = "Open seats are defined as seats where the incumbent never sought re-election. There can be cases where an incumbent is defeated in the primary election. In these cases there will be two or more challengers in the general election."
        incumbent_challenger_status.description = DESCRIPTION
        # check that we can save it
        incumbent_challenger_status.save()

        # check that we can find it
        all_incumbent_challenger_statuses_in_database = IncumbentChallengerStatus.objects.all()
        self.assertEquals(len(all_incumbent_challenger_statuses_in_database),1)
        only_incumbent_challenger_status_in_database = all_incumbent_challenger_statuses_in_database[0]
        self.assertEquals(only_incumbent_challenger_status_in_database, incumbent_challenger_status)

        # check that its attributes have been saved
        self.assertEquals(only_incumbent_challenger_status_in_database.code,"O")
        self.assertEquals(only_incumbent_challenger_status_in_database.value,
                "Open Seat")
        self.assertEquals(only_incumbent_challenger_status_in_database.description, 
                DESCRIPTION)

class InterestGroupCategoryModelTest(TestCase):
    def test_creating_a_new_InterestGroupCategory_and_saving_it_to_the_database(self):
        # TODO: Create a new InterestGroupCategory object 
        interest_group_category = InterestGroupCategory()
        interest_group_category.code = 'L'
        interest_group_category.name = 'LABOR ORGANIZATION'
        DESCRIPTION = "These include unions and other representatives of workers"
        interest_group_category.description = DESCRIPTION
        # check that we can save it
        interest_group_category.save()

        # check that we can find it
        all_interest_group_categories_in_database = InterestGroupCategory.objects.all()
        self.assertEquals(len(all_interest_group_categories_in_database),1)
        only_interest_group_category_in_database = all_interest_group_categories_in_database[0]
        self.assertEquals(only_interest_group_category_in_database, interest_group_category)

        # check that its attributes have been saved
        self.assertEquals(only_interest_group_category_in_database.code,"L")
        self.assertEquals(only_interest_group_category_in_database.name,
                "LABOR ORGANIZATION")
        self.assertEquals(only_interest_group_category_in_database.description, 
                DESCRIPTION)

class IssueModelTest(TestCase):
    def test_creating_a_new_Issue_and_saving_it_to_the_database(self):
        # create a new Issue object with a null issue_category
        issue = Issue()
        issue.name = "Three cent titanium tax increase"
        DESCRIPTION = "The three cent titanium tax increase is a proposal designed to offset the cost of environmental damage of titanium manufacturing"
        issue.description = DESCRIPTION

        # make sure we can save it
        issue.save()

        # make sure we can find it
        all_issues_in_database = Issue.objects.all()
        self.assertEquals(len(all_issues_in_database),1)
        only_issue_in_database = all_issues_in_database[0]
        self.assertEquals(only_issue_in_database, issue)

        # check that its attributes have been saved
        self.assertEquals(only_issue_in_database.name, 
                "Three cent titanium tax increase")
        self.assertEquals(only_issue_in_database.description, DESCRIPTION)
        self.assertEquals(len(only_issue_in_database.issue_categories.all()),0)

    def test_creating_a_new_Issue_with_an_issue_category(self):
        # create a new IssueCategory
        issue_category = IssueCategory()
        issue_category.name = "Titanium Tax"

        # save IssueCategory
        issue_category.save()

        # create a new Issue with an IssueCategory
        issue = Issue()
        issue.name = "Three cent titanium tax increase"
        DESCRIPTION = "The three cent titanium tax increase is a proposal designed to offset the cost of environmental damage of titanium manufacturing"
        issue.description = DESCRIPTION

        # make sure we can save it
        issue.save()
        
        # add an issue category
        issue.issue_categories.add(IssueCategory.objects.filter( 
            name ='Titanium Tax')[0])

        # update
        issue.save()

        # make sure we can find it
        all_issues_in_database = Issue.objects.all()
        self.assertEquals(len(all_issues_in_database),1)
        only_issue_in_database = all_issues_in_database[0]
        self.assertEquals(only_issue_in_database, issue)

        # check that its attributes have been saved
        self.assertEquals(only_issue_in_database.name, 
                "Three cent titanium tax increase")
        self.assertEquals(only_issue_in_database.description, DESCRIPTION)
        self.assertEquals(len(only_issue_in_database.issue_categories.all()),1)
        self.assertEquals(only_issue_in_database.issue_categories.all()[0],issue_category)


class IssueCategoryModelTest(TestCase):
    def test_creating_a_new_IssueCategory_and_saving_it_to_the_database(self):
        # TODO: Create a new IssueCategory object with null parent
        issue_category = IssueCategory()
        issue_category.name = "Titanium tax"

        # make sure we can save it
        issue_category.save()

        # make sure we can find it
        all_issue_categories_in_database = IssueCategory.objects.all()
        self.assertEquals(len(all_issue_categories_in_database),1)
        only_issue_category_in_database = all_issue_categories_in_database[0]
        self.assertEquals(only_issue_category_in_database, issue_category)

        # check that its attributes have been saved
        self.assertEquals(only_issue_category_in_database.name,"Titanium tax")
        self.assertIsNone(only_issue_category_in_database.parent)

    def test_string_representation(self):
        issue_category = IssueCategory()
        issue_category.name = "Titanium tax"
        self.assertEquals(str(issue_category.name),"Titanium tax")

    def test_creating_a_parent_child_relationship_with_IssueCategory(self):
        # create parent IssueCategory
        issue_category_parent = IssueCategory()
        issue_category_parent.name = "Tax"
        
        # save parent IssueCategory
        issue_category_parent.save()
        
        # check to make sure we can find it
        issue_category_parents_in_database = IssueCategory.objects.filter(
                name="Tax")
        self.assertEquals(len(issue_category_parents_in_database),1)
        only_issue_category_parent_in_database = issue_category_parents_in_database[0]
        self.assertEquals(only_issue_category_parent_in_database,issue_category_parent)

        # create child IssueCategory
        issue_category_child = IssueCategory()
        issue_category_child.name = "Titanium tax"
        issue_category_child.parent = issue_category_parent

        # save child IssueCategory
        issue_category_child.save()
        
        # check to make sure we can find it
        issue_category_children_in_database = IssueCategory.objects.filter(
                name="Titanium tax")
        self.assertEquals(len(issue_category_children_in_database),1)
        only_issue_category_child_in_database = issue_category_children_in_database[0]
        self.assertEquals(only_issue_category_child_in_database,issue_category_child)
        
        # check to make sure parent has no parent
        self.assertIsNone(only_issue_category_parent_in_database.parent)

        # check to make sure child-parent relationship is established
        self.assertEquals(only_issue_category_child_in_database.parent,
                only_issue_category_parent_in_database)

    def test_on_delete_parameter(self):
        # create parent IssueCategory
        issue_category_parent = IssueCategory()
        issue_category_parent.name = "Tax"
        
        # save parent IssueCategory
        issue_category_parent.save()

        # create child IssueCategory
        issue_category_child = IssueCategory()
        issue_category_child.name = "Titanium tax"
        issue_category_child.parent = issue_category_parent

        # save child IssueCategory
        issue_category_child.save()

        # delete parent IssueCategory
        issue_category_parent.delete()

        # make sure the orphaned child IssueCategory wasn't deleted
        issue_categories_in_database = IssueCategory.objects.all()
        self.assertEquals(len(issue_categories_in_database),1)
        self.assertEquals(issue_categories_in_database[0],issue_category_child)
        

class MarketModelTest(TestCase):
    def test_market_type_choices(self):
        choices = (('A','Area'), 
                ('C','County'),
                ('S','State'),
                ('N','Nationwide'),
                )
        self.assertEquals(Market.MARKET_TYPE_CHOICES,choices)
    def test_creating_a_new_Market_and_saving_it_to_the_database(self):
        # create a new Market object
        market = Market()
        market.market_type = 'A'
        market.name = 'New New York'

        # check that we can save it
        market.save()

        # check that we can find it
        all_markets_in_database = Market.objects.all()
        self.assertEquals(len(all_markets_in_database),1)
        only_market_in_database = all_markets_in_database[0]
        self.assertEquals(only_market_in_database, market)

        # check that its attributes have been saved
        self.assertEquals(only_market_in_database.market_type,"A")
        self.assertEquals(only_market_in_database.name, "New New York")
    #def test_entering_a_bad_market_type(self):
        # Not possible to restrict?  maybe a validator?

class MediaModelTest(TestCase):
    fixtures = ['funder.json',
            'mediaprofile.json',
            'mediatype.json',
            'tag.json',
            'issue.json',
            'issuecategory.json',
            'committeedesignation.json',
            'committeetype.json',
            'interestgroupcategory.json',
            'connectedorganization.json',
            'stance.json',
            'ad.json',
            'market.json',
            'broadcasttype.json'
            ]


    def test_creating_a_new_Media_and_saving_it_to_the_database(self):
        media_profile = MediaProfile.objects.all()[0]
        tag = Tag.objects.all()[0]
        ad = Ad.objects.all()[0]
        EMBED_CODE =  '<iframe width="560" height="315" src="http://www.youtube.com/embed/BVdLafErW2w" frameborder="0" allowfullscreen></iframe>'

        # Create a new Media object 
        media = Media()
        media.url = "http://www.youtube.com/watch?v=BVdLafErW2w"
        #media.creator_description = "No description available."
        media.curator_description = "Attack ad against Claire McCaskill's bid for MO senate, Attacks McCaskill's association with stimulus spending"
        
        # add required FK relation
        media.media_profile = media_profile
        media.ad = ad

        # save it
        media.save()

        # check that we can find it
        all_medias_in_database = Media.objects.all()
        self.assertEquals(len(all_medias_in_database),1)
        only_media_in_database = all_medias_in_database[0]
        self.assertEquals(only_media_in_database, media)

        # check that its attributes have been saved
        self.assertEquals(only_media_in_database.media_profile,media_profile)
        self.assertEquals(only_media_in_database.ad,ad)
        self.assertEquals(only_media_in_database.link_broken,False)
        self.assertEquals(only_media_in_database.url,
                "http://www.youtube.com/watch?v=BVdLafErW2w")
        self.assertEquals(only_media_in_database.creator_description,
                "No description available.")
        self.assertEquals(only_media_in_database.curator_description,
                "Attack ad against Claire McCaskill's bid for MO senate, Attacks McCaskill's association with stimulus spending")
        self.assertEquals(only_media_in_database.embed_code,EMBED_CODE)


        # add optional MTM relation
        media.tags.add(tag)

        # save it
        media.save()

        # check that we can find it
        all_medias_in_database = Media.objects.all()
        self.assertEquals(len(all_medias_in_database),1)
        only_media_in_database = all_medias_in_database[0]
        self.assertEquals(only_media_in_database, media)

        # check that its attributes have been saved
        all_tags_for_only_media_in_database = only_media_in_database.tags.all()
        self.assertEquals(len(all_tags_for_only_media_in_database),1)
        only_tag_for_only_media_in_database = all_tags_for_only_media_in_database[0]
        self.assertEquals(only_tag_for_only_media_in_database,tag)

        # make sure that we can't delete the media profile
        self.assertRaises(ProtectedError, media_profile.delete)

        # make sure that we don't lose the media when we delete the tag
        tag.delete()
        only_media_in_database = Media.objects.all()[0]
        self.assertEquals(len(only_media_in_database.tags.all()),0)


class MediaProfileModelTest(TestCase):
    fixtures = ['funder.json',
            'committeedesignation.json',
            'committeetype.json',
            'interestgroupcategory.json',
            'connectedorganization.json',
            'stance.json',
            'issue.json',
            'issuecategory.json',
            'mediatype.json']

    def test_creating_a_new_MediaProfile_and_saving_it_to_the_database(self):
        # TODO: Create a new MediaProfile object 
        media_profile = MediaProfile()
        
        # add required FK relation to MediaType
        media_type = MediaType.objects.all()[0]
        media_profile.media_type = media_type
        
        # make sure we can't save it if url does not exist
        media_profile.url = 'http://www.boblannon.com/notreal'
        
        self.assertRaises(Exception,media_profile.save)

        media_profile.url = 'http://www.youtube.com/user/CrossroadsGPSChannel'

        # check that we can save it
        media_profile.save()

        # check that we can find it
        all_media_profiles_in_database = MediaProfile.objects.all()
        self.assertEquals(len(all_media_profiles_in_database),1)
        only_media_profile_in_database = all_media_profiles_in_database[0]
        self.assertEquals(only_media_profile_in_database, media_profile)

        # check that its attributes have been saved
        self.assertEquals(only_media_profile_in_database.url,"http://www.youtube.com/user/CrossroadsGPSChannel")
        self.assertEquals(only_media_profile_in_database.media_type,media_type)

        # add optional FK relation to funder
        funder = Funder.objects.all()[0]
        media_profile.funder = funder

        # save it
        media_profile.save()

        # check that we can find it
        all_media_profiles_in_database = MediaProfile.objects.all()
        self.assertEquals(len(all_media_profiles_in_database),1)
        only_media_profile_in_database = all_media_profiles_in_database[0]
        self.assertEquals(only_media_profile_in_database, media_profile)

        # check that its attributes have been saved
        self.assertEquals(only_media_profile_in_database.url,"http://www.youtube.com/user/CrossroadsGPSChannel")
        self.assertEquals(only_media_profile_in_database.funder,funder)
        self.assertEquals(only_media_profile_in_database.media_type,media_type)

        # make sure deleting the funder doesn't delete the media profile
        funder.delete()

        self.assertEquals(MediaProfile.objects.all()[0],media_profile)

        # make sure deleting the MediaType is not allowed
        self.assertRaises(ProtectedError,media_type.delete)



class MediaTypeModelTest(TestCase):
    def test_creating_a_new_MediaType_and_saving_it_to_the_database(self):
        # create a new MediaType
        media_type = MediaType()
        media_type.main_url = "http://www.youtube.com"
        media_type.scraper_added = True
        
        # check that we can save it
        media_type.save()

        # check that we can find it
        all_media_types_in_database = MediaType.objects.all()
        self.assertEquals(len(all_media_types_in_database),1)
        only_media_type_in_database = all_media_types_in_database[0]
        self.assertEquals(only_media_type_in_database, media_type)

        # check that its attributes have been saved
        self.assertEquals(only_media_type_in_database.main_url,
        "http://www.youtube.com")
        self.assertEquals(only_media_type_in_database.scraper_added, True)
    def test_creating_a_new_MediaType_with_default_values(self):
        # create a new MediaType, not specifying defaulted fields
        media_type = MediaType()
        media_type.main_url = "http://www.youtube.com"
        
        # assert that defaults are correct
        self.assertEquals(media_type.scraper_added,False)

class SourceModelTest(TestCase):
    def test_creating_a_new_Source_and_saving_it_to_the_database(self):
        # create a new Source
        source = Source()
        source.main_url = "http://www.factcheck.org"
        source.scraper_added = True
        
        # check that we can save it
        source.save()

        # check that we can find it
        all_sources_in_database = Source.objects.all()
        self.assertEquals(len(all_sources_in_database),1)
        only_source_in_database = all_sources_in_database[0]
        self.assertEquals(only_source_in_database, source)

        # check that its attributes have been saved
        self.assertEquals(only_source_in_database.main_url,
        "http://www.factcheck.org")
        self.assertEquals(only_source_in_database.scraper_added, True)
    def test_creating_a_new_Source_with_default_values(self):
        # create a new MediaType, not specifying defaulted fields
        source = Source()
        source.main_url = "http://www.youtube.com"
        
        # assert that defaults are correct
        self.assertEquals(source.scraper_added,False)

class StanceModelTest(TestCase):
    def test_creating_a_new_Stance_and_saving_it_to_the_database(self):
        # Create a new Issue object
        issue = Issue()
        issue.name = 'Three cent titanium tax increase'
        ISSUE_DESCRIPTION = "The three cent titanium tax increase is a proposal designed to offset the cost of environmental damage of titanium manufacturing"
        issue.description = ISSUE_DESCRIPTION

        # Save the Issue object
        issue.save()

        # Create a new Stance object 
        stance = Stance()
        stance.name = 'opposes'
        stance.description = 'explicitly opposes the issue'
        stance.issue = Issue.objects.get(name="Three cent titanium tax increase")
        
        # save it
        stance.save()

        # make sure we can find it
        all_stances_in_database = Stance.objects.all()
        self.assertEquals(len(all_stances_in_database),1)
        only_stance_in_database = all_stances_in_database[0]
        self.assertEquals(only_stance_in_database, stance)

        # check that its attributes have been saved
        self.assertEquals(only_stance_in_database.name,'opposes')
        self.assertEquals(only_stance_in_database.description, 
                'explicitly opposes the issue')
        self.assertEquals(only_stance_in_database.issue,issue)

    def test_attempting_to_save_a_Stance_with_no_Issue(self):
        # Create a new Stance object 
        stance = Stance()
        stance.name = 'opposes'
        stance.description = 'explicitly opposes the issue'

        # make sure we get an error if we try to save it
        self.assertRaises(IntegrityError,stance.save)

class TagModelTest(TestCase):
    def test_creating_a_new_Tag_and_saving_it_to_the_database(self):
        # Create a new Tag object 
        tag = Tag()
        tag.name = "titanium"
        
        # Check default values
        self.assertTrue(tag.relevant)
        self.assertTrue(tag.scraped)

        # assign new value
        tag.relevant = False

        # save the Tag
        tag.save()

        # make sure we can find it
        all_tags_in_database = Tag.objects.all()
        self.assertEquals(len(all_tags_in_database),1)
        only_tag_in_database = all_tags_in_database[0]
        self.assertEquals(only_tag_in_database, tag)

        # check that its attributes have been saved
        self.assertEquals(only_tag_in_database.name,'titanium')
        self.assertEquals(only_tag_in_database.relevant, tag.relevant)
        self.assertEquals(only_tag_in_database.scraped, tag.scraped)

    def test_cannot_be_false_for_both_relevant_and_scraped(self):
        # Create a new Tag object 
        tag = Tag()
        tag.name = "titanium"
        tag.relevant = False
        tag.scraped = False

        # check that we get an exception if we try to save this abomination
        self.assertRaises(Exception,tag.save)

    def test_adding_Tag_with_associated_issue(self):
        # create a new Issue object
        issue = Issue()
        issue.name = 'Three cent titanium tax increase'
        ISSUE_DESCRIPTION = "The three cent titanium tax increase is a proposal designed to offset the cost of environmental damage of titanium manufacturing"
        issue.description = ISSUE_DESCRIPTION

        # Save the Issue object
        issue.save()

        # Create a new Tag object 
        tag = Tag()
        tag.name = "titanium"
        
        # save the Tag
        tag.save()

        # add an issue
        tag.issues.add(issue)

        # make sure we can find it
        all_tags_in_database = Tag.objects.all()
        self.assertEquals(len(all_tags_in_database),1)
        only_tag_in_database = all_tags_in_database[0]
        self.assertEquals(only_tag_in_database, tag)

        # check that its attributes have been saved
        tags_issues_in_database = only_tag_in_database.issues.all()
        self.assertEquals(len(tags_issues_in_database),1)
        tags_only_issue_in_database = tags_issues_in_database[0]
        self.assertEquals(tags_only_issue_in_database,issue)
