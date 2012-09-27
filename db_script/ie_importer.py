from influenceexplorer import InfluenceExplorer
import urllib2
import logging

API = InfluenceExplorer('***REMOVED***')

log = logging.getLogger('db_script.ie_importer')

class IEIDImporter():
    def __init__(self,funder_object,ie_api):
        self.api = ie_api
        self.funder = funder_object
        self.ie_id = self.get_ie_id()
    def get_ie_id(self):
        FEC_id = self.funder.FEC_id
        if self.funder.candidate_id:
            try: 
                ie_cand_id = self.api.entities.id_lookup(
                        namespace='urn:fec:candidate',
                        id=self.funder.candidate_id)[0]['id']
            except IndexError:
                log.error("Candidate (%s): not found"%(
                                self.funder.candidate_id,))
            ie_cand_exids = self.api.entities.metadata(
                                ie_cand_id)['external_ids']
            for exid in ie_cand_exids:
                if exid['namespace'] == 'urn:fec:committee':
                    if exid['id'] == self.funder.FEC_id:
                        log.info('%s will link to candidate page for %s'%(
                            self.funder.FEC_id,self.funder.candidate_id))
                        return ie_cand_id
        log.info('looking up %s at ie api'%(FEC_id,))
        try:
            ie_id = self.api.entities.id_lookup(
                    namespace='urn:fec:committee',id=FEC_id)[0]['id']
            return ie_id
        except IndexError:
            log.error("%s (%s): not found"%(self.funder.name,FEC_id))
            return False
    def save_to_funder(self):
        log.info('...saving %s'%(self.funder.FEC_id,))
        self.funder.IE_id = self.ie_id
        self.funder.save()

class IEDescriptionImporter():
    def __init__(self,funder_object,ie_api):
        self.funder = funder_object
        self.api = ie_api
        self.ie_description = self.get_ie_description()
    def get_ie_description(self):
        log.info('looking for %s bio at ie api'%(self.funder.FEC_id,))
        md = self.api.entities.metadata(self.funder.IE_id)
        try:
            return md['metadata']['bio'].replace('</p>','').replace('<p>','')
        except KeyError:
            log.error("... bio for %s (%s): not found"%(self.funder.name,
                                                        self.funder.FEC_id))
            return False
    def save_to_funder(self):
        log.info('...saving new info for %s'%(self.funder.FEC_id,))
        self.funder.description = self.ie_description
        self.funder.save()
