"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from knowledge_base.models import CandidateStatus,CommitteeDesignation,CommitteeType,ConnectedOrganization,CoverageType,BroadcastType,IncumbentChallengerStatus,InterestGroupCategory,Market,MediaType,Source

#class AdModelTest(TestCase):
#    def test_creating_a_new_Ad_and_saving_it_to_the_database(self):
#        # TODO: Create a new Ad object 
#        self.fail('todo: finish '+self.id())
#
#class AuthorModelTest(TestCase):
#    def test_creating_a_new_Author_and_saving_it_to_the_database(self):
#        # TODO: Create a new Author object 
#        self.fail('todo: finish '+self.id())
#
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
#class CandidateModelTest(TestCase):
#    def test_creating_a_new_Candidate_and_saving_it_to_the_database(self):
#        # TODO: Create a new Candidate object 
#        self.fail('todo: finish '+self.id())
#
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

#class CoverageModelTest(TestCase):
#    def test_creating_a_new_Coverage_and_saving_it_to_the_database(self):
#        # TODO: Create a new Coverage object 
#        self.fail('todo: finish '+self.id())
#
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
#class FunderModelTest(TestCase):
#    def test_creating_a_new_Funder_and_saving_it_to_the_database(self):
#        # TODO: Create a new CommitteeDesignation object 
#        self.fail('todo: finish '+self.id())
#
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

#class IssueModelTest(TestCase):
#    def test_creating_a_new_Issue_and_saving_it_to_the_database(self):
#        # TODO: Create a new Issue object 
#        self.fail('todo: finish '+self.id())
#
#class IssueCategoryModelTest(TestCase):
#    def test_creating_a_new_IssueCategory_and_saving_it_to_the_database(self):
#        # TODO: Create a new IssueCategory object 
#        self.fail('todo: finish '+self.id())
#
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

#class MediaModelTest(TestCase):
#    def test_creating_a_new_Media_and_saving_it_to_the_database(self):
#        # TODO: Create a new Media object 
#        self.fail('todo: finish '+self.id())
#
#class MediaProfileModelTest(TestCase):
#    def test_creating_a_new_MediaProfile_and_saving_it_to_the_database(self):
#        # TODO: Create a new MediaProfile object 
#        self.fail('todo: finish '+self.id())

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

#class StanceModelTest(TestCase):
#    def test_creating_a_new_Stance_and_saving_it_to_the_database(self):
#        # TODO: Create a new Stance object 
#        self.fail('todo: finish '+self.id())
#
#class TagModelTest(TestCase):
#    def test_creating_a_new_Tag_and_saving_it_to_the_database(self):
#        # TODO: Create a new Tag object 
#        self.fail('todo: finish '+self.id())
#
