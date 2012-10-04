import sys
import os
import collections
import logging
from decimal import Decimal

from knowledge_base.models import Candidate, \
        CandidateStatus, \
        CommitteeDesignation, \
        CommitteeType, \
        ConnectedOrganization, \
        IncumbentChallengerStatus, \
        InterestGroupCategory, \
        Candidate, \
        Funder, \
        FunderToFunder, \
        FunderToCandidate
#from db_script.log import set_up_logger
from django.db import connections
from django.db.utils import IntegrityError

log = logging.getLogger('db_script.fec_kb_updater')

CONN = connections['default']

def str_or_zero(val):
    if val:
        return str(val)
    else:
        return "0"

def make_result_object(executed_cursor):
    return collections.namedtuple('Result', 
            ', '.join([col.name for col in executed_cursor.description]))

def make_candidate_object(cr):
    if cr.incumbent_challenger_open:
        ics,created_ics = IncumbentChallengerStatus.objects.get_or_create(
            code=cr.incumbent_challenger_open)
        if created_ics:
            log.info("...created\tIncumbentChallengerStatus\t%s"%(unicode(ics),))
    else:
        ics = None
    if cr.candidate_status:
        cs,created_cs = CandidateStatus.objects.get_or_create(
                code=cr.candidate_status)
        if created_cs:
            log.info("...created\tCandidateStatus\t%s"%(unicode(cs),))
    else:
        cs = None
    candidate = Candidate(FEC_id=cr.candidate_id,
            name=cr.candidate_name,
            year_of_election=cr.election_year,
            street_one=cr.street1,
            street_two=cr.street2,
            city=cr.city,
            state=cr.state,
            zip_code=cr.zipcode,
            incumbent_challenger_status=ics,
            candidate_status=cs)
    if cr.party:
        candidate.party = cr.party
    return candidate

def diff_candidate(candidate,cr):
    if cr.incumbent_challenger_open:
        try:
            ics = IncumbentChallengerStatus.objects.get_or_create(
                code=cr.incumbent_challenger_open)
        except IncumbentChallengerStatus.DoesNotExist:
            return True
    else:
        ics = None
    if cr.candidate_status:
        try:
            cs = CandidateStatus.objects.get_or_create(
                code=cr.candidate_status)
        except CandidateStatus.DoesNotExist:
            return True
    else:
        cs = None
    if  candidate.name!=cr.candidate_name or \
        candidate.year_of_election!=cr.election_year or \
        candidate.party != cr.party or \
        candidate.street_one!=cr.street1 or \
        candidate.street_two!=cr.street2 or \
        candidate.city!=cr.city or \
        candidate.state!=cr.state or \
        candidate.zip_code!=cr.zipcode or \
        candidate.incumbent_challenger_status!=ics or \
        candidate.candidate_status!=cs:
        return True
    else:
        return False

def merge_candidate_object(candidate,cr):
    if cr.incumbent_challenger_open:
        ics,created_ics = IncumbentChallengerStatus.objects.get_or_create(
                code=cr.incumbent_challenger_open)
        if created_ics:
            log.info("...created\tIncumbentChallengerStatus\t%s"%(unicode(ics),))
    else:
        ics = None
    if cr.candidate_status:
        cs,created_cs = CandidateStatus.objects.get_or_create(
                code=cr.candidate_status)
        if created_cs:
            log.info("...created\tCandidateStatus\t%s"%(unicode(cs),))
    else:
        cs = None
    candidate.name=cr.candidate_name
    candidate.year_of_election=cr.election_year
    candidate.street_one=cr.street1
    candidate.street_two=cr.street2
    candidate.city=cr.city
    candidate.state=cr.state
    candidate.zip_code=cr.zipcode
    candidate.party=cr.party
    candidate.incumbent_challenger_status=ics
    candidate.candidate_status=cs
    return candidate

def make_committee_object(cr):
    if cr.interest_group:
        igc,created_igc = InterestGroupCategory.objects.get_or_create(
                code=cr.interest_group)
        if created_igc:
            log.info("...created\tInterestGroupCategory\t%s"%(unicode(igc),))
    else:
        igc = None
    if cr.committee_type:
        ct,created_ct = CommitteeType.objects.get_or_create(
                code=cr.committee_type)
        if created_ct:
            log.info("...created\tCommitteeType\t%s"%(unicode(ct),))
    else:
        ct = None
    if cr.committee_designation:
        cd,created_cd = CommitteeDesignation.objects.get_or_create(
                code=cr.committee_designation)
        if created_cd:
            log.info("...created\tCommitteeDesignation\t%s"%(unicode(ct),))
    else:
        cd = None
    if cr.connected_org:
        co,created_org = ConnectedOrganization.objects.get_or_create(
                name=cr.connected_org)
        if created_org:
            log.info("...created\tConnectedOrganization\t%s"%(unicode(co),))
    else:
        co = None
    committee = Funder()
    repayments = Decimal(str_or_zero(cr.candidate_loan_repayments)) + \
                    Decimal(str_or_zero(cr.other_loan_repayments))
    refunds = Decimal(str_or_zero(cr.refunds_to_individuals)) + \
                Decimal(str_or_zero(cr.refunds_to_committees))
    committee.total_contributions = Decimal(str_or_zero(cr.total_receipts)) - \
                                        (repayments + refunds)
    committee.total_disbursements = Decimal(str_or_zero(cr.total_disbursements))
    committee.cash_on_hand = Decimal(str_or_zero(cr.cash_close_of_period))
    committee.party = cr.committee_party
    committee.FEC_id=cr.committee_id
    if cr.candidate_id:
        committee.candidate_id = cr.candidate_id
    committee.name=cr.committee_name
    committee.treasurer_name=cr.treasurers_name
    committee.street_one=cr.street1
    committee.street_two=cr.street2
    committee.city=cr.city
    committee.state=cr.state
    committee.zip_code=cr.zipcode
    committee.interest_group_category=igc
    committee.committee_type=ct
    committee.committee_designation=cd
    committee.connected_organization=co
    return committee

def diff_committee(committee,cr):
    if cr.interest_group:
        try:
            igc = InterestGroupCategory.objects.get_or_create(
                code=cr.interest_group)
        except InterestGroupCategory.DoesNotExist:
            return True
    else:
        igc = None
    if cr.committee_type:
        try:
            ct = CommitteeType.objects.get_or_create(
                code=cr.committee_type)
        except CommitteeType.DoesNotExist:
            return True
    else:
        ct = None
    if cr.committee_designation:
        try:
            cd = CommitteeDesignation.objects.get_or_create(
                code=cr.committee_designation)
        except CommitteeDesignation.DoesNotExist:
            return True
    else:
        cd = None
    if cr.connected_org:
        try: 
            co,created_org = ConnectedOrganization.objects.get_or_create(
                    name=cr.connected_org)
        except Connected_Organization.DoesNotExist:
            return True
    else:
        co = None
    if  committee.name!=cr.committee_name or \
        committee.treasurer_name!=cr.treasurers_name or \
        committee.party!=cr.committee_party or \
        committee.street_one!=cr.street1 or \
        committee.street_two!=cr.street2 or \
        committee.city!=cr.city or \
        committee.state!=cr.state or \
        committee.zip_code!=cr.zipcode or \
        committee.filing_frequency!=cr.filing_frequency or \
        committee.interest_group_category!=igc or \
        committee.committee_type!=ct or \
        committee.committee_designation!=cd or \
        committee.connected_organization!=co:
        return True
    else:
        return False

def merge_committee_object(committee,cr):
    if cr.interest_group:
        igc,created_igc = InterestGroupCategory.objects.get_or_create(
                code=cr.interest_group)
        if created_igc:
            log.info("...created\tInterestGroupCategory\t%s"%(unicode(igc),))
    else:
        igc = None
    if cr.committee_type:
        ct,created_ct = CommitteeType.objects.get_or_create(
                code=cr.committee_type)
        if created_ct:
            log.info("...created\tCommitteeType\t%s"%(unicode(ct),))
    else:
        ct = None
    if cr.committee_designation:
        cd,created_cd = CommitteeDesignation.objects.get_or_create(
                code=cr.committee_designation)
        if created_cd:
            log.info("...created\tCommitteeDesignation\t%s"%(unicode(ct),))
    else:
        cd = None
    if cr.connected_org:
        co,created_org = ConnectedOrganization.objects.get_or_create(
                name=cr.connected_org)
        if created_org:
            log.info("...created\tConnectedOrganization\t%s"%(unicode(co),))
    else:
        co = None
    #if not committee.ftum_url:
    repayments = Decimal(str_or_zero(cr.candidate_loan_repayments)) + \
                        Decimal(str_or_zero(cr.other_loan_repayments))
    refunds = Decimal(str_or_zero(cr.refunds_to_individuals)) + \
                    Decimal(str_or_zero(cr.refunds_to_committees))
    total_contributions = Decimal(str_or_zero(cr.total_receipts)) - (repayments + refunds)
    try:
        committee.total_contributions = max(committee.total_conributions, 
                                            total_contributions)
    except AttributeError:
        committee.total_contributions = total_contributions
    try:
        committee.total_disbursements = max(committee.total_disbursements, Decimal(str_or_zero(cr.total_disbursements)))
    except AttributeError:
        committee.total_disbursements = Decimal(str_or_zero(cr.total_disbursements))
    try:
        committee.cash_on_hand = max(committee.cash_on_hand, Decimal(str_or_zero(cr.cash_close_of_period)))
    except AttributeError:
        committee.cash_on_hand = Decimal(str_or_zero(cr.cash_close_of_period))
    committee.name=cr.committee_name
    committee.treasurer_name=cr.treasurers_name
    if cr.candidate_id:
        committee.candidate_id = cr.candidate_id
    committee.street_one=cr.street1
    committee.street_two=cr.street2
    committee.party=cr.committee_party
    committee.city=cr.city
    committee.state=cr.state
    committee.zip_code=cr.zipcode
    committee.interest_group_category=igc
    committee.committee_type=ct
    committee.committee_designation=cd
    committee.connected_organization=co
    return committee

class CandidateQuery():
    def __init__(self,conn,fec_id_set):
        self.id_list_string = self.make_id_list_string(fec_id_set)
        self.cursor = conn.cursor()
    def get_result_cursor(self):
        quy = "select * from fec_candidates WHERE candidate_id in "
        quy += self.id_list_string
        self.cursor.execute(quy)
        return self.cursor
    def make_id_list_string(self,id_set):
        return ' ('+','.join(["'"+str(a)+"'" for a in id_set])+') '

class CandidateCommitteeQuery():
    def __init__(self,conn,fec_id_set):
        self.id_list_string = self.make_id_list_string(fec_id_set)
        self.cursor = conn.cursor()
    def get_result_cursor(self):
        quy = """select fcm.*,
        fcns.total_receipts, fcns.total_disbursements, fcns.ending_cash as
        cash_close_of_period, fcns.candidate_loan_repayments, 
        fcns.other_loan_repayments, fcns.refunds_to_individuals, 
        fcns.refunds_to_committees from fec_candidates fcn join 
        fec_candidate_summaries fcns on fcn.candidate_id = 
        fcns.candidate_id join fec_committees fcm on fcm.committee_id =
        fcn.committee_id where fcn.committee_id in """
        quy += self.id_list_string
        self.cursor.execute(quy)
        return self.cursor
    def make_id_list_string(self,id_set):
        return ' ('+','.join(["'"+str(a)+"'" for a in id_set])+') '

class CommitteeQuery():
    def __init__(self,conn,fec_id_set):
        self.id_list_string = self.make_id_list_string(fec_id_set)
        self.cursor = conn.cursor()
    def get_result_cursor(self):
        quy = """select fc.*, fcs.cash_close_of_period, fcs.total_receipts,
        fcs.total_disbursements, fcs.candidate_loan_repayments,
        fcs.loan_repayments as other_loan_repayments, fcs.refunds_to_individuals,
        fcs.refunds_to_committees from fec_committees fc left join 
        fec_committee_summaries fcs on fc.committee_id = fcs.committee_id 
        WHERE fc.committee_id in """
        quy += self.id_list_string
        self.cursor.execute(quy)
        return self.cursor
    def make_id_list_string(self,id_set):
        return ' ('+','.join(["'"+str(a)+"'" for a in id_set])+') '

class CandidateImporter():
    def __init__(self,processing_dir,conn=CONN):
        self.processing_dir = os.path.expanduser(processing_dir)
        #self.log = set_up_logger('candidate_importer',self.processing_dir)
        self.conn = conn
        self.imported_id_set = self.get_imported_ids()
        self.model_id_set = self.get_model_ids()
        self.create_id_set = self.get_new_ids()
        self.update_id_set = self.get_matched_ids()
        self.done_msg = "\nDone.\n\nREPORT\n"+"="*80+"\n"
        #self.delete_id_set = self.get_missing_ids()
    def get_imported_ids(self):
        c = self.conn.cursor()
        c.execute("select candidate_id from fec_candidates")
        return set([i[0] for i in c])
    def get_model_ids(self):
        return set([obj.FEC_id for obj in Candidate.objects.all()])
    def get_new_ids(self):
        return self.imported_id_set - self.model_id_set
    def get_matched_ids(self):
        return self.imported_id_set & self.model_id_set
    #def get_missing_ids(self):
    #    return self.model_id_set - self.imported_id_set
    def update(self):
        log.info("Adding Candidates...\n"+ \
                '\n'.join(['+'+str(a) for a in self.create_id_set]))
        if self.create_id_set:
            self.add_candidates()

        log.info("Updating Candidates...\n"+ \
                '\n'.join(['++'+str(a) for a in self.update_id_set]))
        if self.update_id_set:
            self.update_candidates()

        log.info(self.done_msg)

        #log.info("Deleting Candidates...\n"+ \
        #        '\n'.join(['-'+str(a) for a in self.delete_id_set]))
        #delete_candidates()
    def add_candidates(self):
        added_entries = 0
        cq = CandidateQuery(self.conn,self.create_id_set)
        ec = cq.get_result_cursor()
        CandidateResult = make_result_object(ec)
        for r in ec:
            cr = CandidateResult(*r)
            candidate = make_candidate_object(cr)
            try:
                candidate.save()
                log.info("...added\tCandidate\t%s"%(unicode(candidate),))
                added_entries += 1
            except IntegrityError e:
                log.error(e)
                continue
        self.done_msg += "Added %d new entries\n"%(added_entries,)

    def update_candidates(self):
        merged_entries = 0
        cq = CandidateQuery(self.conn,self.update_id_set)
        ec = cq.get_result_cursor()
        CandidateResult = make_result_object(ec)
        for r in ec:
            cr = CandidateResult(*r)
            old_c = Candidate.objects.get(FEC_id=cr.candidate_id)
            if diff_candidate(old_c,cr):
                merged = merge_candidate_object(old_c,cr)
                merged.save()
                merged_entries += 1
                log.info("...merged\tCandidate\t%s"%(unicode(merged),))
            else:
                continue
        self.done_msg += "Merged %d entries\n"%(merged_entries,)

class CommitteeImporter():
    def __init__(self,processing_dir,conn=CONN):
        self.processing_dir = os.path.expanduser(processing_dir)
        #self.log = set_up_logger('committee_importer',self.processing_dir)
        self.conn = conn
        self.imported_id_set = self.get_imported_ids()
        self.model_id_set = self.get_model_ids()
        self.create_id_set = self.get_new_ids()
        self.update_id_set = self.get_matched_ids()
        #self.delete_id_set = self.get_missing_ids()
        self.done_msg = "\nDone.\n\nREPORT\n"+"="*80+"\n"
    def get_imported_ids(self):
        c = self.conn.cursor()
        c.execute("select committee_id from fec_committees")
        return set([i[0] for i in c])
    def get_model_ids(self):
        return set([obj.FEC_id for obj in Funder.objects.all()])
    def get_new_ids(self):
        return self.imported_id_set - self.model_id_set
    def get_matched_ids(self):
        return self.imported_id_set & self.model_id_set
    #def get_missing_ids(self):
    #    return self.model_id_set - self.imported_id_set
    def update(self):
        log.info("Adding Committees...\n"+ \
                '\n'.join(['+'+str(a) for a in self.create_id_set]))
        if self.create_id_set:
            self.add_committees()
            self.add_candidate_committees()

        log.info("Updating Committees...\n"+ \
                '\n'.join(['++'+str(a) for a in self.update_id_set]))
        if self.update_id_set:
            self.update_committees()
            self.update_candidate_committees()

        log.info(self.done_msg)
        #self.log.info("Deleting Candidates...\n"+ \
        #        '\n'.join(['-'+str(a) for a in self.delete_id_set]))
        #delete_candidates()
    def add_committees(self):
        added_entries = 0
        cq = CommitteeQuery(self.conn,self.create_id_set)
        ec = cq.get_result_cursor()
        CommitteeResult = make_result_object(ec)
        for r in ec:
            cr = CommitteeResult(*r)
            committee = make_committee_object(cr)
            committee.save()
            log.info("...added\tCommittee\t%s"%(unicode(committee),))
            added_entries += 1
        self.done_msg += "Added %d new entries\n"%(added_entries,)
    def update_committees(self):
        merged_entries = 0
        cq = CommitteeQuery(self.conn,self.update_id_set)
        ec = cq.get_result_cursor()
        CommitteeResult = make_result_object(ec)
        for r in ec:
            cr = CommitteeResult(*r)
            old_c = Funder.objects.get(FEC_id=cr.committee_id)
            if diff_committee(old_c,cr):
                merged = merge_committee_object(old_c,cr)
                merged.save()
                merged_entries += 1
                log.info("...updated\tCommittee\t%s"%(unicode(merged),))
            else:
                continue
        self.done_msg += "...Merged %d new entries"%(merged_entries,)
    def add_candidate_committees(self):
        added_entries = 0
        cq = CandidateCommitteeQuery(self.conn,self.create_id_set)
        ec = cq.get_result_cursor()
        CommitteeResult = make_result_object(ec)
        for r in ec:
            cr = CommitteeResult(*r)
            committee = make_committee_object(cr)
            committee.save()
            log.info("...added\tCommittee\t%s"%(unicode(committee),))
            added_entries += 1
        self.done_msg += "Added %d new entries\n"%(added_entries,)
    def update_candidate_committees(self):
        merged_entries = 0
        cq = CandidateCommitteeQuery(self.conn,self.update_id_set)
        ec = cq.get_result_cursor()
        CommitteeResult = make_result_object(ec)
        for r in ec:
            cr = CommitteeResult(*r)
            old_c = Funder.objects.get(FEC_id=cr.committee_id)
            if diff_committee(old_c,cr):
                merged = merge_committee_object(old_c,cr)
                merged.save()
                merged_entries += 1
                log.info("...updated\tCommittee\t%s"%(unicode(merged),))
            else:
                continue
        self.done_msg += "...Merged %d new entries"%(merged_entries,)
