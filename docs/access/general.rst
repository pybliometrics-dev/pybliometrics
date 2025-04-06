How to access Scopus
--------------------

To access Scopus via its API, you need two things.  First, your institution needs to be a subscriber (not only to Scopus, but really to its API); second, you need to register API keys at https://dev.elsevier.com/apikey/manage.  For each profile, you may register 10 keys.

The Scopus API recognizes you as a member of your institution via IP range.  For working from home, Scopus can also grant InstTokens.  Thus one of three things needs to happen:

1. You are in your institution's network
2. You use your institution's VPN
3. You use an InstToken

Option 1 is easy and the most common.

Option 2 might require you to additionally set a proxy.  You can do so in the :doc:`configuration file <../configuration>`.

Option 3 is rare.  An InstToken is provided directly by Scopus/Elsevier to allow remote access in the absence of a VPN.  It is coupled directly to a key.  If you have an InstToken, please provide it during the setup when `pybliometrics` prompts you for it.  Alternatively, add it to the :doc:`configuration file <../configuration>` manually.  Remember to remove them (or comment out) when you're in your VPN again.

There are only three Scopus APIs that you can access without your institution subscribing to it: The Abstract Retrieval API through :doc:`AbstractRetrieval(..., view=META) <../reference/scopus/ScopusSearch>`, the Scopus Search API through doc:`ScopusSearch(..., subscriber=False) <../reference/scopus/ScopusSearch>`, and the Subject Classifications API doc:`SubjectClassification() <../reference/scopus/SubjectClassification>` without special parameters.

How to access ScienceDirect
---------------------------

The access to ScienceDirect is similar to the Scopus API, yet totally independent.  Institutions may subscribe to the ScienceDirect API but not to the Scopus API, and vice versa.
