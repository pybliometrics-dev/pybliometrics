

def detect_id_type(sid):
    """Method that tries to infer the type of abstract ID.

        Parameters
        ----------
        sid : str
            The ID of an abstract on Scopus.

        Raises
        ------
        ValueError
            If the ID type cannot be inferred.

        Notes
        -----
        PII usually has 17 chars, but in Scopus there are valid
        cases with only 16 for old converted articles.

        Scopus ID contains only digits, but it can have leading
        zeros. If ID with leading zeros is treated as a number,
        SyntaxError can occur, or the ID will be rendered invalid
        and the type will be misinterpreted.

    """
    sid = str(sid)

    if sid.startswith('2-s2.0-'):
        return 'eid'
    elif '/' in sid:
        return 'doi'
    elif 16 <= len(sid) <= 17:
        return 'pii'
    elif 10 <= len(sid) < 16 and sid.isnumeric():
        return 'scopus_id'
    elif len(sid) < 10 and sid.isnumeric():
        return 'pubmed_id'
    else:
        raise ValueError('ID type detection failed for \'{}\'.'.format(sid))
