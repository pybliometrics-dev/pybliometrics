How to access Scopus
~~~~~~~~~~~~~~~~~~~~

To access Scopus via its API, you need two things.  First, your institution needs to be a subscriber (not only to Scopus, but really to its API); second, you need to register API keys at https://dev.elsevier.com/apikey/manage.  For each profile, you may register 10 keys.

The Scopus API recognizes you as a member of your institution via IP range.  For working from home, Scopus can also grant InstTokens.  Thus one of three things needs to happen:

1. You are in your instition's network
2. You use your instition's VPN
3. You use an InstToken

Option 1 is easy and the most common.

Option 2 might require you to additionally set a proxy.  You can do so in the :doc:`configuration file <../configuration>`.

Option 3 is rare.  If you have an InstToken, please provide it during the setup when `pybliometrics` prompts you for it. Alternatively, add it to the :doc:`configuration file <../configuration>` manually.  You may also set the InstToken via `insttoken="XYZ"` in any class. This is the preferred solution if you possess multiple keys.

There are only three Scopus APIs that you can access without your institution subscribing to it: The Abstract Retrieval API, the Scopus Search API and the Subject Classifications API.

As a non-subscriber, use `view=META` in the :doc:`AbstractRetrieval() <../classes/ScopusSearch>` class.  To search for for documents via the Scopus Search API as a non-subscriber, set `subscriber=False` in the :doc:`ScopusSearch() <../classes/ScopusSearch>` (you will retrieve less information however).  The Subject Classifications API is the same for subscribers and non-subscribers.
