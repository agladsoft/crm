from dataclasses import dataclass
import requests
from requests_ntlm import HttpNtlmAuth
import csv
from pathlib import Path
import os
from abc import ABC


class CrmClient(object):
    @property
    def baseurl(self):
        return 'http://srvr-mscrm.first/Ruscon/api/data/v8.2/'

    def get_auth(self):
        return HttpNtlmAuth('first\\request', 'Edc789')


@dataclass
class RemoteEntity(ABC):
    data_root_path = "/home/ruscon/sambashare/crm/done"
    crm_client: 'CrmClient'

    @property
    def header(self):
        return None

    @property
    def pattern(self):
        raise NotImplementedError(f'Определите pattern в {self.__class__.__name__}.')

    @property
    def csv_file(self):
        return f'{self.data_root_path}/{self.pattern}.csv'

    @property
    def url(self):
        return '%s%s' % (self.crm_client.baseurl, self.pattern)

    def modifier(self, value):
        return value

    def get_dto_row(self, row, header):
        dto_row = row.copy()
        for field_dto in iter(row.keys()):
            if not field_dto in header:
                del dto_row[field_dto]
            else:
                dto_row[field_dto] = self.modifier(dto_row[field_dto])
        return dto_row

    def move_files(self):
        for each_file in Path(self.data_root_path).glob(f'{self.pattern}.csv'):
            trg_path = each_file.parent.parent
            each_file.rename(trg_path.joinpath(each_file.name))

    def save_to_csv(self, all_fields=False, next_link=None, write_mode='w', print_keys=False):
        url = next_link if next_link else self.url
        r = requests.get(url, auth=self.crm_client.get_auth())
        if r.status_code != 200:
            raise Exception(f'Код ответа {r.status_code}')
        data = r.json()
        value = data['value']
        if not 'value' in data:
            raise Exception('В ответе нет ключа value')
        value = data['value']
        keys = value[0].keys()
        if print_keys:
            print(keys)
        header = keys if not self.header or all_fields else self.header
        if write_mode == 'w' and os.path.exists(self.csv_file):
            os.remove(self.csv_file)
        with open(self.csv_file, write_mode, encoding='utf-8', newline='') as f:
            w = csv.DictWriter(f, header, delimiter=";", quoting=csv.QUOTE_NONNUMERIC)
            if write_mode == 'w':
                w.writeheader()
            for row in value:
                w.writerow(self.get_dto_row(row, header))
            f.close()
        if "@odata.nextLink" in data:
            self.save_to_csv(all_fields, data["@odata.nextLink"], 'a', print_keys)


class StageHistory(RemoteEntity):
    @property
    def pattern(self):
        return 'rn_stagehistories'

    @property
    def header(self):
        return (
            '@odata.etag', 'timezoneruleversionnumber', 'versionnumber', '_owningbusinessunit_value', 'rn_stagestep',
            '_owninguser_value', 'statecode', 'statuscode', '_createdby_value', 'rn_name', 'rn_stagehistoryid',
            '_ownerid_value', 'modifiedon', '_rn_stageid_value', '_modifiedby_value', '_rn_opportunityid_value',
            'createdon', 'rn_eventdate', 'utcconversiontimezonecode', 'overriddencreatedon', 'importsequencenumber',
            '_modifiedonbehalfby_value', '_createdonbehalfby_value', '_owningteam_value'
        )


class GapPowerbiOption(RemoteEntity):
    @property
    def pattern(self):
        return 'gap_powerbioptionsetrefs'

    @property
    def header(self):
        return (
            '@odata.etag', '_organizationid_value', 'statecode', 'statuscode', 'gap_label', 'gap_powerbioptionsetrefid',
            'modifiedon', '_modifiedby_value', 'gap_entityschemaname', 'versionnumber', 'gap_entityname',
            'gap_optionsetschemaname', 'gap_value', 'gap_language', 'createdon', '_createdby_value', 'gap_imageurl',
            'overriddencreatedon', '_modifiedonbehalfby_value', 'importsequencenumber', '_createdonbehalfby_value',
            'timezoneruleversionnumber', 'utcconversiontimezonecode'
        )


class Lead(RemoteEntity):
    @property
    def pattern(self):
        return 'leads'

    @property
    def header(self):
        return (
            '@odata.etag', 'confirminterest', 'statecode', 'statuscode', 'address2_shippingmethodcode',
            'address1_addressid', 'leadqualitycode', 'donotbulkemail', 'salesstagecode', 'donotsendmm', 'leadid',
            'emailaddress1', '_owningteam_value', 'fullname', 'address1_addresstypecode', 'subject', 'donotpostalmail',
            '_ownerid_value', 'modifiedon', 'stageid', 'donotemail', 'donotphone', 'address2_addresstypecode',
            'kc_convertingemail', 'versionnumber', 'createdon', 'prioritycode', 'traversedpath',
            'address1_shippingmethodcode', 'description', 'leadsourcecode', '_modifiedby_value', 'decisionmaker',
            'preferredcontactmethodcode', '_owningbusinessunit_value', 'lastname', 'yomifullname', 'donotfax', 'merged',
            '_createdby_value', 'processid', 'address2_addressid', 'evaluatefit', 'participatesinworkflow',
            'address1_name', 'rn_tenderorderdate', 'address1_county', 'address1_telephone2', 'address1_city',
            'address1_telephone1', 'utcconversiontimezonecode', 'address2_country', 'address2_postofficebox',
            'address2_city', 'budgetamount_base', 'estimatedvalue', 'lastusedincampaign', 'rn_tenderorderprice_base',
            'budgetstatus', 'address1_line3', 'estimatedclosedate', 'rn_deadline', 'salesstage', 'initialcommunication',
            'followemail', 'rn_tenderresult', 'estimatedamount_base', 'budgetamount', 'rn_suspectspam', 'industrycode',
            'telephone3', 'address1_country', 'middlename', 'exchangerate', 'overriddencreatedon', 'mobilephone', 'fax',
            'yomilastname', '_accountid_value', 'sic', 'entityimageid', 'address1_composite', 'need',
            '_owninguser_value', 'address1_upszone', 'purchaseprocess', '_createdonbehalfby_value',
            'address1_postalcode', '_parentcontactid_value', 'entityimage', 'yomifirstname', 'address1_stateorprovince',
            'timespentbymeonemailandmeetings', '_customerid_value', 'address1_postofficebox', 'entityimage_url',
            'address2_county', '_originatingcaseid_value', '_contactid_value', 'telephone2', 'address2_line3',
            'address2_line1', 'salutation', 'numberofemployees', 'rn_tenderorderprice', 'kc_directioncode',
            'companyname', '_qualifyingopportunityid_value', '_slaid_value', 'firstname', 'address1_latitude',
            'schedulefollowup_qualify', 'address2_latitude', 'address1_line2', '_masterid_value', 'address2_fax',
            'rn_tenderconclusion', 'address2_telephone1', 'address1_telephone3', 'purchasetimeframe', 'address2_line2',
            'address2_upszone', 'websiteurl', 'address2_postalcode', 'rn_tendertype', 'address2_name', 'pager',
            'kc_saleschannelcode', 'rn_spamcheckdate', 'address2_telephone2', 'entityimage_timestamp',
            '_campaignid_value', 'address1_fax', 'yomimiddlename', 'jobtitle', 'timezoneruleversionnumber',
            'emailaddress2', 'emailaddress3', 'lastonholdtime', '_relatedobjectid_value', '_modifiedonbehalfby_value',
            'address1_utcoffset', '_transactioncurrencyid_value', 'qualificationcomments', 'onholdtime', 'revenue',
            'address2_stateorprovince', 'estimatedamount', 'kc_industrycode', '_slainvokedid_value',
            'address1_longitude', 'address2_utcoffset', 'address2_composite', 'schedulefollowup_prospect',
            'yomicompanyname', 'telephone1', 'address2_telephone3', '_parentaccountid_value', 'address2_longitude',
            '_rn_tenderplatform_value', 'kc_isoverdue', 'address1_line1', 'importsequencenumber', 'revenue_base'
        )


class Interview(RemoteEntity):
    @property
    def pattern(self):
        return 'kc_interviews'

    @property
    def header(self):
        return (
            '@odata.etag', 'kc_customsservices', 'kc_interviewformcode', 'kc_question3', 'kc_question2', 'kc_question1',
            'kc_question7', 'kc_question6', 'kc_question5', 'kc_question4', 'statecode', 'kc_answer11',
            '_kc_managerretentionid_value', 'kc_customerstatuscode', 'kc_signofrelationship', '_kc_accountid_value',
            '_owningbusinessunit_value', '_owninguser_value', '_kc_businessunitid_value', '_kc_contactid_value',
            'kc_train', 'kc_interviewid', '_ownerid_value', 'kc_jobtitle', 'kc_portservices', 'kc_ratingcode',
            'kc_other', 'kc_auto', 'timezoneruleversionnumber', 'statuscode', 'createdon', 'kc_inn', 'versionnumber',
            'modifiedon', 'kc_internationalcarriage', 'kc_feedback', 'kc_interviewdate', 'kc_name',
            'kc_offdockterminalservices', 'kc_email', 'kc_phonenumber', 'kc_question11', 'kc_needforcorrectiveaction',
            '_modifiedby_value', '_createdby_value', 'kc_formpassedtohead', 'kc_needreinterview', 'kc_typecustomercode',
            'kc_interviewtypecode', 'kc_answer1', 'kc_answer3', 'kc_answer2', 'kc_answer5', 'kc_answer4', 'kc_answer7',
            'kc_answer6', '_kc_userid_value', 'kc_comment10', 'kc_answer8', 'kc_comment8', 'kc_workphonenumber',
            'kc_question10', 'kc_comment7', '_owningteam_value', 'kc_comment12', 'kc_question12', 'kc_answer9',
            'kc_openingslogans', 'kc_comment6', '_kc_campaignid_value', 'kc_answer12', 'kc_comment11', 'rn_comment14',
            'rn_question14', 'kc_interviewtype', 'kc_comment2', 'kc_comment3', 'overriddencreatedon',
            '_rn_incident_value', 'kc_answer10', 'kc_comment1', 'kc_comment5', 'kc_description',
            'utcconversiontimezonecode', '_createdonbehalfby_value', 'kc_question8', 'kc_comment4',
            'importsequencenumber', 'kc_finalslogans', 'kc_whenneedreinterview', 'kc_comment9', 'rn_answer14',
            'kc_question9', '_modifiedonbehalfby_value'
        )


class Opportunity(RemoteEntity):
    @property
    def pattern(self):
        return 'opportunities'

    @property
    def header(self):
        return (
            '@odata.etag', 'kc_directioncode', 'prioritycode', 'completeinternalreview', 'stepname',
            'rn_lastactivitydate', 'filedebrief', 'kc_guidukt', 'confirminterest', 'captureproposalfeedback',
            'exchangerate', 'opportunityid', '_parentcontactid_value', 'identifycompetitors', '_parentaccountid_value',
            'name',
            'decisionmaker', 'kc_sendtoukt', 'isrevenuesystemcalculated', '_transactioncurrencyid_value',
            'kc_potencialprofitperunit', '_owninguser_value', 'totalamount', 'presentproposal', 'createdon',
            'kc_potencialteu', '_ownerid_value', 'sendthankyounote', 'identifycustomercontacts', 'stageid',
            'traversedpath',
            'rn_lastactivitydate_date', 'evaluatefit', 'totalamountlessfreight', 'kc_potencialamountwithvat',
            'totallineitemdiscountamount', 'totalamountlessfreight_base', 'totaldiscountamount', 'processid',
            'statuscode', 'kc_potencialamount', 'totaltax_base', 'totallineitemamount_base', 'totalamount_base',
            'developproposal', 'versionnumber',
            'description', 'modifiedon', 'resolvefeedback', 'totaltax', 'totaldiscountamount_base',
            'rn_lastactivitydate_state', '_modifiedby_value', 'presentfinalproposal', '_createdby_value',
            'pricingerrorcode', 'salesstagecode', 'totallineitemdiscountamount_base', 'identifypursuitteam',
            'participatesinworkflow',
            'statecode', '_owningbusinessunit_value', 'pursuitdecision', 'opportunityratingcode', '_customerid_value',
            'totallineitemamount', 'completefinalproposal', 'schedulefollowup_prospect', 'kc_loststatuscode',
            'actualvalue', 'freightamount', 'kc_projectnumber', 'timezoneruleversionnumber',
            'utcconversiontimezonecode', 'rn_paymentrate', 'rn_initiatives', 'freightamount_base',
            'timespentbymeonemailandmeetings', 'salesstage', 'actualclosedate', 'actualvalue_base', 'quotecomments',
            'kc_reason', '_owningteam_value', '_slainvokedid_value', 'discountamount', '_pricelevelid_value',
            'budgetamount', 'closeprobability', 'budgetstatus',
            'estimatedvalue_base', 'estimatedclosedate', 'need', 'lastonholdtime', '_contactid_value',
            'rn_accounting_system', 'importsequencenumber', '_modifiedonbehalfby_value', '_originatingleadid_value',
            'kc_datenexttender', 'purchaseprocess', 'stepid', 'onholdtime', 'discountpercentage', 'proposedsolution',
            'schedulefollowup_qualify', 'customerneed', 'overriddencreatedon', '_accountid_value', 'finaldecisiondate',
            'estimatedvalue', '_campaignid_value', 'kc_plandateapplication', '_slaid_value', 'discountamount_base',
            'kc_guidisr', 'purchasetimeframe', 'budgetamount_base', 'qualificationcomments', '_createdonbehalfby_value',
            'currentsituation', 'customerpainpoints', 'scheduleproposalmeeting', 'initialcommunication', 'timeline',
            'rn_lastorderdate'
        )


class Systemuser(RemoteEntity):
    @property
    def pattern(self):
        return 'systemusers'

    @property
    def header(self):
        return (
            '@odata.etag', 'systemuserid', 'accessmode', 'kc_guidisr', 'issyncwithdirectory', 'address1_addressid',
            'incomingemaildeliverymethod', 'internalemailaddress', 'domainname', '_queueid_value', 'isintegrationuser',
            'createdon', '_calendarid_value', 'fullname', '_businessunitid_value', 'invitestatuscode',
            'defaultodbfoldername', 'caltype', 'modifiedon', 'defaultfilterspopulated', 'outgoingemaildeliverymethod',
            'emailrouteraccessapproval', 'versionnumber', 'kc_initialseng', 'mobilephone', 'setupuser',
            'userlicensetype', '_modifiedby_value', 'organizationid', 'middlename', 'lastname',
            'isemailaddressapprovedbyo365admin', 'firstname', 'yomifullname', 'kc_guidukt', 'isdisabled',
            'address2_addressid', '_defaultmailbox_value', 'islicensed', 'ownerid', '_createdby_value',
            'preferredaddresscode', 'nickname', 'azureactivedirectoryobjectid', 'kc_fullnameeng',
            'address2_stateorprovince', 'applicationiduri', 'address1_county', 'address2_country',
            'address2_postofficebox', 'preferredphonecode', 'yammeruserid', 'title', 'trx_phone_calls_recording',
            'employeeid', '_territoryid_value', 'jobtitle', 'skills', 'rn_guid', 'address2_composite',
            'address1_postalcode', 'entityimage', 'windowsliveid', 'address1_line3', 'disabledreason',
            'address2_utcoffset', 'address1_line2', 'address1_city', 'personalemailaddress', '_kc_cfoid_value',
            'address1_telephone2', '_createdonbehalfby_value', 'address1_longitude', 'sharepointemailaddress',
            'yomifirstname', 'exchangerate', 'address1_shippingmethodcode', 'yomimiddlename', 'address2_line2',
            'address1_line1', 'address1_telephone1', 'traversedpath', 'address1_country', 'yomilastname',
            'address2_latitude', 'address2_fax', 'address1_composite', 'trx_extension', 'address1_latitude',
            'entityimage_timestamp', 'photourl', '_siteid_value', '_transactioncurrencyid_value', 'passportlo',
            '_mobileofflineprofileid_value', 'address1_name', 'address2_telephone2', '_parentsystemuserid_value',
            'stageid', 'address2_longitude', 'salutation', 'yammeremailaddress', 'address2_city', 'entityimageid',
            'address1_addresstypecode', 'address2_county', 'address2_line1', 'address2_upszone', 'address1_utcoffset',
            '_positionid_value', 'address2_shippingmethodcode', 'passporthi', 'address1_telephone3',
            'address2_postalcode', 'address2_telephone1', 'entityimage_url', 'processid', 'governmentid',
            '_modifiedonbehalfby_value', 'address2_line3', 'utcconversiontimezonecode', 'homephone', 'trx_lic',
            'preferredemailcode', 'address2_name', 'overriddencreatedon', 'address1_upszone', 'importsequencenumber',
            'mobilealertemail', 'address2_addresstypecode', 'address1_fax', 'address2_telephone3',
            'address1_postofficebox', 'address1_stateorprovince', 'displayinserviceviews', 'timezoneruleversionnumber',
            'applicationid'
        )


class Businessunits(RemoteEntity):
    @property
    def pattern(self):
        return 'businessunits'

    @property
    def header(self):
        return (
            '@odata.etag', 'inheritancemask', 'address2_addressid', 'modifiedon', 'createdon', 'versionnumber',
            'isdisabled', 'name', '_organizationid_value', 'businessunitid', 'address1_addressid', 'address1_line2',
            'address1_stateorprovince', 'address1_addresstypecode', 'address2_addresstypecode',
            '_modifiedonbehalfby_value', 'creditlimit', 'exchangerate', 'emailaddress', '_modifiedby_value',
            'stockexchange',
            'address1_telephone1', 'address2_shippingmethodcode', 'address2_country', 'address2_name', 'tickersymbol',
            'address2_utcoffset', 'address2_latitude', '_parentbusinessunitid_value', 'address2_fax',
            'importsequencenumber', 'picture', 'address1_county', 'address2_line1', '_createdonbehalfby_value',
            'address2_telephone2', 'divisionname', 'websiteurl', 'address2_telephone1', 'address2_postofficebox',
            'fileasname', 'address1_telephone3', 'address1_line1', 'address2_line3', 'address1_city', 'utcoffset',
            'address2_longitude', 'address1_shippingmethodcode', 'address1_latitude', 'costcenter',
            'address1_utcoffset', 'address2_line2', 'address1_fax', 'address1_name', 'address1_line3',
            'address2_telephone3', 'address1_longitude', 'address2_upszone', '_calendarid_value', 'address2_county',
            'address2_city', 'address1_postofficebox', 'workflowsuspended', 'address1_postalcode', '_createdby_value',
            '_transactioncurrencyid_value', 'address1_telephone2', 'address1_upszone', 'address2_stateorprovince',
            'overriddencreatedon', 'address2_postalcode', 'address1_country', 'description', 'disabledreason',
            'ftpsiteurl'
        )


class Account(RemoteEntity):
    @property
    def pattern(self):
        return 'accounts'

    @property
    def header(self):
        return (
            '@odata.etag', 'kc_portservices', 'kc_customsservices', 'kc_provider', 'address2_addresstypecode', 'merged',
            'rn_regnom', 'kc_lastinterviewdate_state', 'rn_taxnumber',
            'kc_competitor', 'territorycode', 'emailaddress1', 'exchangerate', 'rn_getbyinn', 'rn_projects', 'name',
            'websiteurl', 'kc_auto_state', 'kc_sendtoukt', 'kc_customsservices_date',
            '_owningbusinessunit_value', '_owninguser_value', '_primarycontactid_value', 'address2_line1',
            'address1_composite', 'donotpostalmail', 'accountratingcode', 'marketingonly',
            'rn_number', 'donotphone', 'preferredcontactmethodcode', '_ownerid_value', 'accountclassificationcode',
            'kc_firstsalesorderdate_state', 'customersizecode',
            'kc_offdockterminalservices_state', 'kc_quantityinterview_state', 'rn_clientmonitoring',
            'kc_firstsalesorderdate_date', 'trx_phone_calls_recording', 'donotemail',
            'kc_train_state', 'address2_shippingmethodcode', 'kc_auto', 'kc_portservices_state',
            'address2_freighttermscode', 'statuscode', 'createdon', 'rn_lastsalesorderdate_date',
            '_originatingleadid_value', 'kc_line', 'rn_haslead', 'kc_internationalcarriage', 'donotsendmm', 'donotfax',
            'kc_opfcode', 'donotbulkpostalmail', 'versionnumber',
            'openrevenue_date', 'address1_line1', 'kc_train_date', 'modifiedon', 'creditonhold', 'telephone1',
            'kc_train', 'kc_ruscon', '_transactioncurrencyid_value',
            'kc_internationalcarriage_state', 'accountid', 'kc_auto_date', 'kc_internationalcarriage_date',
            'kc_customsservices_state', '_modifiedby_value',
            'kc_quantityinterview_date', 'followemail', 'businesstypecode', '_createdby_value',
            'kc_offdockterminalservices_date', 'kc_fullname', 'donotbulkemail',
            'rn_lastsalesorderdate_state', 'kc_fullnameeng', 'kc_quantityinterview', 'rn_isnumber',
            'address2_composite', 'kc_offdockterminalservices', 'address1_addressid',
            'participatesinworkflow', 'statecode', 'address2_addressid', 'kc_lastinterviewdate_date',
            'kc_portservices_date', 'shippingmethodcode', 'opendeals_date',
            'openrevenue_state', 'rn_monitoringdate', 'telephone3', 'openrevenue', 'address2_longitude',
            'address1_longitude', 'emailaddress2', 'address1_country',
            'rn_dokey', 'lastusedincampaign', 'address1_postofficebox', '_modifiedonbehalfby_value',
            'preferredappointmenttimecode', 'timespentbymeonemailandmeetings',
            'address2_name', 'address2_upszone', 'primarysatoriid', 'entityimage_url', 'timezoneruleversionnumber',
            'kc_customerstatuscode', 'c4crm_guiduktorganisation',
            'address1_stateorprovince', '_slaid_value', 'kc_guiduktpayer', 'address2_city', 'address1_upszone',
            'stockexchange', 'entityimage', '_preferredserviceid_value',
            '_masterid_value', 'address2_latitude', 'address2_utcoffset', 'telephone2', 'paymenttermscode',
            '_territoryid_value', '_modifiedbyexternalparty_value', 'entityimageid',
            'kc_guiduktline', '_owningteam_value', 'fax', 'stageid', 'utcconversiontimezonecode', 'marketcap_base',
            'onholdtime', 'address1_primarycontactname', 'yominame',
            '_defaultpricelevelid_value', 'ownershipcode', 'address2_telephone2', 'address2_line3',
            '_createdonbehalfby_value', 'kc_productdescription', '_createdbyexternalparty_value',
            'kc_inn', 'kc_guiduktclient', 'overriddencreatedon', 'address1_utcoffset', 'primarytwitterid', 'ftpsiteurl',
            'sic', 'address1_telephone2', 'tickersymbol',
            'rn_lastsalesorderdate', 'address1_line2', 'numberofemployees', 'kc_industrycode', 'aging60_base',
            'revenue_base', 'openrevenue_base', 'industrycode',
            'address2_telephone3', 'address1_line3', 'address1_latitude', 'address1_telephone1', 'accountnumber',
            'entityimage_timestamp', '_preferredsystemuserid_value',
            'kc_guidisrclient', 'address2_postalcode', 'kc_guidisrorganisation', 'preferredappointmentdaycode',
            'kc_kpp', 'processid', 'creditlimit_base', 'address2_stateorprovince',
            '_kc_managerretentionid_value', 'kc_rate', 'emailaddress3', 'importsequencenumber', '_slainvokedid_value',
            'aging90', 'sharesoutstanding', 'opendeals_state', 'kc_ogrn',
            'address1_shippingmethodcode', 'kc_fixingmanagerdate', 'address2_county', 'description', 'kc_guidisrpayer',
            'aging60', 'marketcap', 'accountcategorycode', 'aging30_base', 'address1_name',
            'opendeals', 'aging30', 'address1_addresstypecode', 'address1_fax', 'traversedpath',
            '_parentaccountid_value', 'address1_freighttermscode', 'address2_telephone1', 'address1_telephone3',
            'kc_guiduktorganisation', 'address1_postalcode', '_preferredequipmentid_value', 'rn_status',
            'kc_lastinterviewdate', 'address2_fax', 'lastonholdtime', 'kc_okpo', 'customertypecode',
            '_kc_whobroughtid_value', 'kc_firstsalesorderdate', 'creditlimit', 'aging90_base', 'address2_country',
            'address1_county', 'address2_line2', 'revenue', 'rn_uid', 'address2_primarycontactname',
            'address2_postofficebox', 'address1_city', 'rn_accountsource'
        )


class OpportunitySalesProcesses(RemoteEntity):
    @property
    def pattern(self):
        return 'opportunitysalesprocesses'

    @property
    def header(self):
        return (
            '@odata.etag', 'activestagestartedon', '_organizationid_value', '_processid_value', 'traversedpath',
            'statecode', 'statuscode', '_createdby_value', 'modifiedon',
            '_modifiedby_value', 'businessprocessflowinstanceid', 'createdon', 'versionnumber', '_activestageid_value',
            '_opportunityid_value', 'name',
            '_createdonbehalfby_value', '_modifiedonbehalfby_value', '_quoteid_value', 'overriddencreatedon',
            '_salesorderid_value', '_transactioncurrencyid_value',
            'exchangerate', 'completedon', 'importsequencenumber', 'duration'
        )


class ProcesStages(RemoteEntity):
    @property
    def pattern(self):
        return 'processstages'

    @property
    def header(self):
        return (
            '@odata.etag', '_ownerid_value', '_processid_value', 'owningbusinessunit', 'stagename', 'versionnumber',
            'primaryentitytypecode', 'clientdata',
            'processstageid', 'stagecategory'
        )


class Teams(RemoteEntity):
    @property
    def pattern(self):
        return 'teams'

    @property
    def header(self):
        return (
            '@odata.etag', '_queueid_value', 'organizationid', '_businessunitid_value', '_administratorid_value',
            'systemmanaged', 'isdefault', 'teamtype',
            'createdon', 'description', 'versionnumber', 'modifiedon', 'name', 'teamid', 'ownerid',
            '_transactioncurrencyid_value', 'yominame', '_teamtemplateid_value',
            '_modifiedonbehalfby_value', 'traversedpath', 'exchangerate', 'importsequencenumber', '_createdby_value',
            'emailaddress', 'processid', '_regardingobjectid_value',
            'stageid', 'overriddencreatedon', '_modifiedby_value', '_createdonbehalfby_value'
        )


def main():
    print_keys = False
    crm_cient = CrmClient()

    stage_history = StageHistory(crm_cient)
    stage_history.save_to_csv(print_keys=print_keys)
    stage_history.move_files()

    gap_powerbi_option = GapPowerbiOption(crm_cient)
    gap_powerbi_option.save_to_csv(print_keys=print_keys)
    gap_powerbi_option.move_files()

    lead = Lead(crm_cient)
    lead.save_to_csv(print_keys=print_keys)
    lead.move_files()

    interview = Interview(crm_cient)
    interview.save_to_csv(print_keys=print_keys)
    interview.move_files()

    opportunity = Opportunity(crm_cient)
    opportunity.save_to_csv(print_keys=print_keys)
    opportunity.move_files()

    systemuser = Systemuser(crm_cient)
    systemuser.save_to_csv(print_keys=print_keys)
    systemuser.move_files()

    businessunits = Businessunits(crm_cient)
    businessunits.save_to_csv(print_keys=print_keys)
    businessunits.move_files()

    account = Account(crm_cient)
    account.save_to_csv(print_keys=print_keys)
    account.move_files()

    opportunity_sales_processes = OpportunitySalesProcesses(crm_cient)
    opportunity_sales_processes.save_to_csv(print_keys=print_keys)
    opportunity_sales_processes.move_files()

    proces_stages = ProcesStages(crm_cient)
    proces_stages.save_to_csv(print_keys=print_keys)
    proces_stages.move_files()

    teams = Teams(crm_cient)
    teams.save_to_csv(print_keys=print_keys)
    teams.move_files()


if __name__ == "__main__":
    main()
