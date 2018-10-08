

def discover_id_type(ID):
    """Method that tries to infer the type of abstract ID.

        Parameters
        ----------
        ID : str
            The ID of an abstract on Scopus.

        Raises
        ------
        ValueError
            If the ID type cannot be inferred.

        Notes
        -----
        PII usually has 17 chars, but in Scopus there are valid
        cases with only 16 for old converted articles.

    """
    if ID.startswith('2-s2.0-'):
        return 'eid'
    elif '/' in ID:
        return 'doi'
    elif 16 <= len(ID) <= 17:
        return 'pii'
    elif 10 <= len(ID) < 16 and ID.isnumeric():
        return 'scopus_id'
    elif len(ID) < 10 and ID.isnumeric():
        return 'pubmed_id'
    else:
        raise ValueError('ID type autodiscovery failed for \'{}\'.'.format(ID))
