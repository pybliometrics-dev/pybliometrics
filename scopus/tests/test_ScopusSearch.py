#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `ScopusSearch` module."""

from collections import namedtuple
from nose.tools import assert_equal

import scopus


order = 'eid doi pii pubmed_id title subtype creator afid affilname '\
        'affiliation_city affiliation_country author_count author_names '\
        'author_ids author_afids coverDate coverDisplayDate publicationName '\
        'issn source_id eIssn aggregationType volume issueIdentifier '\
        'article_number pageRange description authkeywords citedby_count '\
        'openaccess fund_acr fund_no fund_sponsor'
doc = namedtuple('Document', order)

# Set to False because of citation count
s_au = scopus.ScopusSearch('AU-ID(24320488600)', refresh=False)
s_j = scopus.ScopusSearch('SOURCE-ID(22900) AND PUBYEAR IS 2010', refresh=False)
s_empty = scopus.ScopusSearch('SOURCE-ID(19700188323) AND PUBYEAR IS 1900', refresh=False)


def test_get_eids_author():
    assert_equal(s_au.get_eids(), ['2-s2.0-26444452434'])


def test_get_eids_journal():
    assert_equal(len(s_j.get_eids()), 118)


def test_results_author():
    expected = doc(eid='2-s2.0-26444452434', doi='10.1016/0014-2921(92)90085-B',
        pii='001429219290085B', pubmed_id=None, title='Economists as policymakers: A round-table discussion. Introduction',
        subtype='ar', creator='Draghi M.', afid=None, affilname=None,
        affiliation_city=None, affiliation_country=None, author_count='1',
        author_names='Draghi, Mario', author_ids='24320488600',
        author_afids=None, coverDate='1992-01-01', coverDisplayDate='April 1992',
        publicationName='European Economic Review', issn='00142921',
        source_id='20749', eIssn=None, aggregationType='Journal', volume='36',
        issueIdentifier='2-3', article_number=None, pageRange='307-309',
        description=None, authkeywords=None, citedby_count='1', openaccess='0',
        fund_acr=None, fund_no='undefined', fund_sponsor=None)
    assert_equal(s_au.results[-1], expected)


def test_results_journal():
    abstract = 'In recent years, the threat of global climate change has '\
        'come to be seen as one of the most serious confronting humanity. '\
        'To meet this challenge will require the development of new '\
        'technologies and the substantial improvement of existing ones, as '\
        'well as ensuring their prompt and widespread deployment. Some have '\
        'argued that the urgency of the situation requires a "Manhattan '\
        'Project" or an "Apollo Program". This paper examines why such a '\
        'policy model is inappropriate, arguing that the nature of the '\
        'policy context for confronting climate change necessitates a '\
        'different kind of technology policy than that for building an '\
        'atomic bomb or for achieving a manned lunar landing. Instead, it '\
        'seeks to draw lessons from three sectors that seem to be more '\
        'pertinent and where government technological development and '\
        'deployment programs have been pursued with some success in the '\
        'United States - namely, agriculture, biomedical research and '\
        'information technology. It compares and contrasts these with the '\
        'policies pursued with regard to the first two of these sectors in '\
        'the United Kingdom. The paper concludes by drawing out the '\
        'implications for the design of policies supporting technological '\
        'development and innovation to address the problem of global climate '\
        'change. © 2010 Elsevier B.V. All rights reserved.'
    keywords = 'Global warming | Innovation | R&amp;D | Technology adoption '\
               '| Technology policy'
    expected = doc(eid='2-s2.0-77955427414', doi='10.1016/j.respol.2010.05.008',
        pii='S0048733310001320', pubmed_id=None,
        title="Technology policy and global warming: Why new policy models are needed (or why putting new wine in old bottles won't work)",
        subtype='no', creator='Mowery D.', afid='60072522;60030162;60003771;60017317',
        affilname='UC Berkeley Haas School of Business;Columbia University in the City of New York;University of Manchester;University of Sussex',
        affiliation_city='Berkeley;New York;Manchester;Sussex',
        affiliation_country='United States;United States;United Kingdom;United Kingdom',
        author_count='4', author_names='Mowery, David C.;Nelson, Richard R.;Martin, Ben R.',
        author_ids='7003916189;7404560006;7402931873',
        author_afids='60072522;60030162-60003771;60017317', coverDate='2010-01-01',
        coverDisplayDate='October 2010', publicationName='Research Policy',
        issn='00487333', source_id='22900', eIssn=None, aggregationType='Journal',
        volume='39', issueIdentifier='8', article_number=None, pageRange='1011-1023',
        description=abstract, authkeywords=keywords, citedby_count='120',
        openaccess='0', fund_acr='NSF', fund_no='0531184', fund_sponsor='Array BioPharma')
    assert_equal(s_j.results[-1], expected)

def test_results_empty():
    assert_equal(s_empty.results, None)