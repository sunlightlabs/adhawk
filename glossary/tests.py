import helpers
from models import Item
import unittest
from django.core.urlresolvers import reverse


class HelperTestCase(unittest.TestCase):

    def setUp(self):
        self.glossary_base_url = reverse('glossary')

    def tearDown(self):
        Item.objects.all().delete()

    def test_autogeneration_of_slug(self):
        item = self.create_troubled_asset()
        slug = item.slug
        self.assertEquals(slug, 'troubled-assets')

    def test_glossarize_with_1_glossary_item(self):
        self.create_warrant()
        plain = 'the warrants were issued'
        actual = helpers.glossarize(plain)
        expected = 'the <a href="%s#warrants">warrants</a> were issued' \
            % self.glossary_base_url
        self.assertEquals(actual, expected)

    def test_glossarize_with_2_glossary_items(self):
        self.create_warrant()
        self.create_troubled_asset()
        plain = 'the warrants were issued ... the troubled assets'
        actual = helpers.glossarize(plain)
        expected = 'the <a href="%s#warrants">warrants</a> were issued ' \
            '... the <a href="%s#troubled-assets">troubled assets</a>' \
            % (self.glossary_base_url, self.glossary_base_url)
        self.assertEquals(actual, expected)

    def test_glossarize_with_blank_acronym(self):
        """
        A glossary item with a blank acronym could mistakenly get pluralized
        into 's'. This would result in unexpected matches to 's (apostrophe s)
        """
        self.create_loan_guarantee()
        plain = "the Treasury Department's reliance on loan guarantees is ..."
        actual = helpers.glossarize(plain)
        expected = "the Treasury Department's reliance on " \
            '<a href="%s#loan-guarantee">loan guarantees</a> is ...' \
            % (self.glossary_base_url,)
        self.assertEquals(actual, expected)

    def test_glossarize_with_blank_synonym(self):
        """
        A glossary item with a blank synonym could mistakenly get pluralized
        into 's'. This would result in unexpected matches to 's (apostrophe s)
        """
        self.create_abcp()
        plain = "the Treasury Department's reliance on ABCP is ..."
        actual = helpers.glossarize(plain)
        expected = "the Treasury Department's reliance on " \
            '<a href="%s#abcp">ABCP</a> is ...' \
            % (self.glossary_base_url,)
        self.assertEquals(actual, expected)

    def test_glossarize_with_overlapping_glossary_items_v1(self):
        'create a "loan" then a "loan guarantee"'
        self.create_loan()
        self.create_loan_guarantee()
        self.assert_ok_with_2_overlapping_glossary_items()

    def test_glossarize_with_2_overlapping_glossary_items_v2(self):
        'create a "loan guarantee" then a "loan"'
        self.create_loan_guarantee()
        self.create_loan()
        self.assert_ok_with_2_overlapping_glossary_items()

    def assert_ok_with_2_overlapping_glossary_items(self):
        'helper for test_glossarize_with_overlapping_glossary_items_'
        plain = 'the loan guarantee was'
        actual = helpers.glossarize(plain)
        expected = 'the <a href="%s#loan-guarantee">loan guarantee</a> was' \
            % self.glossary_base_url
        self.assertEquals(actual, expected)

    # --------------------

    def create_warrant(self):
        """
        Creates a glossary item where the slug is already specified.
        """
        return self.create_item(
            term = "warrants",
            slug = "warrants",
            definition = """Options to buy stock (equity) at a specific price
            within a certain time frame. In this case, the specific terms will
            be agreed upon between Treasury and the respective bank.
            """)

    def create_troubled_asset(self):
        """
        Creates a glossary items where the slug is not given,
        therefore the model should automatically generate one.
        """
        return self.create_item(
            term = "troubled assets",
            slug = "",
            definition = """In relation to TARP, troubled assets are defined
            as any residential or commercial mortgages - or any stocks and
            bonds, debt or other instruments based on such mortgages - that
            originated or were issued on or before March 14, 2008, the
            purchase of which the Treasury Secretary determines promotes
            financial market stability. The term can also apply to any other
            financial instrument that the Secretary, after consulting with the
            Federal Reserve Chair, determines the purchase of which is
            necessary to promote financial market stability, but only after
            such determination is given in writing to appropriate
            Congressional committees.""")

    def create_loan(self):
        """
        Creates a glossary item ("loan") that overlaps with another
        item ("loan guarantee").
        """
        return self.create_item(
            term = "loan",
            slug = "",
            definition = """A sum of money given from one party to another for
            use over a period of time. The money is paid back according to
            terms agreed upon by both parties, including the specified
            interest rates and the timeframe over which the loan will be
            repaid.""")

    def create_loan_guarantee(self):
        """
        Creates a glossary item ("loan guarantee") that contains another
        item ("loan").  Note that the acronym is not defined.
        """
        return self.create_item(
            term = "loan guarantee",
            slug = "",
            definition = """A commitment on the part of the guaranteeing
            agency or enterprise to pay off a loan if the borrower
            defaults.""")

    def create_abcp(self):
        """
        Creates a glossary item with an associated acronym.
        """
        return self.create_item(
            term = "Asset-Backed Commercial Paper",
            slug = "",
            definition = """A corporate debt due within a year, and backed by
            assets such as real estate, autos and other commercial assets.
            Asset-backed commercial paper is similar to a mortgage-backed
            security; both are packages of loans resold to other investors.
            However, asset-backed commercial paper includes assets other than
            home mortgages.""",
            acronym = "ABCP")

    # --------------------

    def create_item(self, term, slug, definition, acronym="", synonym=""):
        item = Item()
        item.term = term
        if slug:
            item.slug = slug
        item.definition = definition
        if acronym:
            item.acronym = acronym
        if synonym:
            item.synonym = synonym
        item.save()
        return item
