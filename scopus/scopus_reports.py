import matplotlib.pyplot as plt
from operator import itemgetter

from .scopus_api import ScopusAbstract, ScopusJournal
from .scopus_author import ScopusAuthor


def report(scopus_search, label):
    """Print out an org-mode report for the results from the scopus_search
    with the label.
    """

    counts = {}  # to count papers per author
    journals = {}  # to count publications per journal
    author_count = []  # to count a paper's number of authors for a histogram
    paper_cites = {}
    Ncites = 0
    document_types = {}

    N = 0  # to count number of publications

    for eid in scopus_search.EIDS:
        a = ScopusAbstract(eid)

        # Get types of documents
        if a.aggregationType in document_types:
            document_types[a.aggregationType] += 1
        else:
            document_types[a.aggregationType] = 1

        if a.aggregationType == 'Journal':
            Ncites += int(a.citedby_count)  # get total cites
            N += 1  # count all the papers

            # get count for journals
            jkey = (a.publicationName, a.source_id, a.issn)
            if jkey in journals:
                journals[jkey] += 1
            else:
                journals[jkey] = 1

            # get authors per paper
            author_count += [len(a.authors)]

            # now count papers per author
            for author in a.authors:
                key = (author.indexed_name, author.auid)
                if key in counts:
                    counts[key] += 1
                else:
                    counts[key] = 1

            # counting cites per paper
            key = (a.title, a.scopus_link)
            if key in paper_cites:
                paper_cites[key] += a.citedby_count
            else:
                paper_cites[key] = a.citedby_count

    print('*** Report for {}\n'.format(label))
    print('#+attr_latex: :placement [H] :center nil')
    print('#+caption: Types of documents found for {}.'.format(label))
    print('| Document type | count |\n|-')
    for key in document_types:
        print('| {0} | {1} |'.format(key, document_types[key]))

    print('\n\n')
    print('{0} articles ({2} citations) '
          'found by {1} authors'.format(N, len(counts), Ncites))

    # Author counts  {(name, scopus-id): count}
    view = [('[[scopusid:{0}][{1}]]'.format(k[1], k[0]),  # org-mode link
             v,  # counts
             k[1])  # scopus-id
            for k, v in counts.items()]
    view.sort(reverse=True, key=itemgetter(1))

    print('\n#+attr_latex: :placement [H] :center nil')
    print('#+caption: Author publication counts for {0}.'.format(label))
    print('| name | count | categories |')
    print('|-')
    for name, count, scopus_id in view[0:20]:
        cats = ', '.join(['{0} ({1})'.format(cat[0], cat[1])
                          for cat in ScopusAuthor(scopus_id).categories[0:3]])
        print('| {0} | {1} | {2} |'.format(name, count, cats))

    # journal view
    s = '[[http://www.scopus.com/source/sourceInfo.url?sourceId={0}][{1}]]'
    jview = [(s.format(k[1], k[0][0:50]),  # url
              k[1],  # source_id
              k[2],  # issn
              v)  # count
             for k, v in journals.items()]
    jview.sort(reverse=True, key=itemgetter(3))

    print('\n\n')
    print('#+attr_latex: :placement [H] :center nil')
    print('#+caption: Journal publication counts for {0}.'.format(label))
    print('| Journal | count | IPP |')
    print('|-')

    for journal, sid, issn, count in jview[0:12]:
        JOURNAL = ScopusJournal(issn)
        IPP = JOURNAL.IPP or 0
        print('| {0} | {1} | {2} |'.format(journal, count, IPP))

    # view of journals sorted by `IPP
    JVIEW = []
    for journal, sid, issn, count in jview:
        JOURNAL = ScopusJournal(issn)
        IPP = JOURNAL.IPP or 0
        JVIEW.append([journal, count, IPP])
    JVIEW.sort(reverse=True, key=itemgetter(2))

    print('\n\n')
    print('#+attr_latex: :placement [H] :center nil')
    print('#+caption: Journal publication counts'
          ' for {0} sorted by IPP.'.format(label))
    print('| Journal | count | IPP |')
    print('|-')
    for journal, count, IPP in JVIEW[0:12]:
        print('|{0}|{1}|{2}|'.format(journal, count, IPP))

    # top cited papers
    pview = [('[[{0}][{1}]]'.format(k[1], k[0][0:60]),
              int(v))
             for k, v in paper_cites.items()]
    pview.sort(reverse=True, key=itemgetter(1))

    # Compute department j-index
    hindex = 0
    for i, entry in enumerate(pview):
        # entry is url, source_id, count
        u, count = entry
        if count > i + 1:
            continue
        else:
            hindex = i + 1
            break

    print('\n\n#+attr_latex: :placement [H] :center nil')
    print('#+caption: Top cited publication'
          ' counts for {0}. j-index = {1}.'.format(label, hindex))
    print('| title | cite count |\n|-')
    for title, count in pview[0:10]:
        print('| {0} | {1} |'.format(title, count))

    plt.figure()
    plt.hist(author_count, 20)
    plt.xlabel('# authors')
    plt.ylabel('frequency')
    plt.savefig('{0}-nauthors-per-publication.png'.format(label))

    print('\n\n#+caption: Number of authors '
          'on each publication for {}.'.format(label))
    print('[[./{0}-nauthors-per-publication.png]]'.format(label))

    print('''**** Bibliography  :noexport:
     :PROPERTIES:
     :VISIBILITY: folded
     :END:''')

    print(scopus_search.org_summary)
