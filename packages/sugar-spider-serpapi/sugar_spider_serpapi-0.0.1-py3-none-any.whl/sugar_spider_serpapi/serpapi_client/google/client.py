import asyncio
import logging
import urllib.parse
from typing import Callable, List

import aiohttp
from aiolimiter import AsyncLimiter

from ..conf import METADATA_ATTRS, PAGINATION_ATTRS
from ..exception import SerpApiError
from ..handler.local import LocalStore

logger = logging.getLogger(__name__)


def serp_log_maker(url: str, results_page: dict) -> str:
    _log = list()
    _log.append(f"Request({url})")
    _results_page = ", ".join([f"{k}: {len(v) if isinstance(v, list) else 1}" for k, v in results_page.items()])
    _log.append(f"Response({_results_page})")
    return ", ".join(_log)


################################################################
# _GoogleSearch
################################################################
class _GoogleSearch:
    def __init__(
        self,
        api_key: str,
        gl: str,
        location: str,
        hl: str,
        google_domain: str,
        output: str,
        tpm: int,
        handler: Callable = None,
    ):
        self.base_url = "https://serpapi.com/search.json"

        self.gl = gl
        self.location = location

        self.limiter = AsyncLimiter(max_rate=tpm, time_period=60)
        self.handler = handler

        self.default_params = {
            "api_key": api_key,
            "gl": gl,
            "location": location,
            "hl": hl,
            "engine": "google_shopping",
            "google_domain": google_domain,
            "output": output,
        }

    # _search
    async def _search(self, engine: str, num_per_page: int = 100, max_pages: int = 1, **kwargs):
        params = {"engine": engine, "num": num_per_page, **kwargs}

        async with aiohttp.ClientSession() as session:
            # first hit
            _query = {k: v for k, v in {**self.default_params, **params}.items() if v is not None}
            query = urllib.parse.urlencode(query=_query)
            url = "?".join([self.base_url, query])
            first_page = await self._get(session=session, url=url)
            if not first_page:
                return

            if (max_pages < 2) or (first_page.get("serpapi_pagination") is None):
                return [first_page]

            # second hit
            other_pages = first_page["serpapi_pagination"]["other_pages"]
            coros = list()
            for i, url in other_pages.items():
                if int(i) > max_pages:
                    break
                url += f'&api_key={self.default_params["api_key"]}'
                coros.append(self._get(session=session, url=url))
            other_pages = await asyncio.gather(*coros, return_exceptions=True)

        pages = list()
        for page in [first_page, *other_pages]:
            if isinstance(page, Exception):
                logger.warning(page)
                continue

        return pages

    # _get
    async def _get(self, session: aiohttp.ClientSession, url: str, serpapi_retries: int = 3):
        original_url = url
        for i in range(serpapi_retries):
            try:
                async with self.limiter:
                    async with session.get(url) as response:
                        response.raise_for_status()
                        page = await response.json()
                        if "error" in page:
                            # SerpApi.com 에러 발생하면 no_cache=true 조건을 붙여야 함. 아니면 계속 에러난 것을 재반환
                            url = original_url + f"&no_cache=true"
                            error_message = page["error"]
                            raise SerpApiError(error_message)

                        # logging
                        _log = serp_log_maker(url=url, results_page=page)
                        logger.debug(_log)

                        # handler
                        if self.handler:
                            _ = await self.handler(page)

                        return page
            except SerpApiError as ex:
                last_exception = ex
                _msg = f"Try {i+1}/{serpapi_retries} failed with '{error_message}', try again..."
                logger.warning(_msg)
        else:
            raise last_exception

    #  filter results pages by results type
    @staticmethod
    def _filter_results_pages_by_results_types(
        results_pages: List[dict], incl_results_types: List[str] = None, excl_results_types: List[str] = None
    ) -> List[dict]:
        # return metadata and reviews_results
        filtered_pages = list()
        for page in results_pages:
            filtered_page = dict()
            for k, v in page.items():
                if excl_results_types and (k in excl_results_types):
                    continue
                if incl_results_types and (k not in incl_results_types):
                    continue
                filtered_page.update({k: v})
            filtered_pages.append(filtered_page)
        return filtered_pages


################################################################
# GoogleSearch
################################################################
class GoogleSearch(_GoogleSearch):
    def __init__(
        self,
        api_key: str,
        gl: str,
        location: str = None,
        hl: str = None,
        google_domain: str = "google.com",
        output: str = "json",
        tpm: int = 30,
        handler: Callable = LocalStore(),
    ):
        """Google Search.

        Parameters:
        gl (str, optional): Parameter defines the country to use for the Google search.
            It's a two-letter country code (e.g., us for the United States, uk for United Kingdom). Defaults to None.

        location (str, optional): Parameter defines from where you want the search to originate.
            If several locations match the location requested, we'll pick the most popular one.
            Location and uule parameters can't be used together. It is recommended to specify
            location at the city level to simulate a real user’s search. Defaults to None.

        hl (str, optional): Parameter defines the language to use for the Google search.
            It's a two-letter language code (e.g., en for English, es for Spanish). Defaults to None.

        google_domain (str, optional): Parameter defines the Google domain to use. Defaults to google.com. Defaults to None.

        handler (Callalbe, optional): Handler for handle results, like Kafka producer. Defaults to None.
        """
        super().__init__(
            api_key=api_key,
            gl=gl,
            location=location,
            hl=hl,
            google_domain=google_domain,
            output=output,
            tpm=tpm,
            handler=handler,
        )

    ################################
    # Search
    ################################
    async def search(
        self,
        q: str,
        ludocid: str = None,
        lsig: str = None,
        kgmid: str = None,
        si: str = None,
        ibp: str = None,
        cr: str = None,
        lr: str = None,
        tbs: str = None,
        safe: str = None,
        nfpr: str = None,
        filter: str = None,
        tbm: str = None,
        num_per_page: int = 100,
        max_pages: int = 1,
        **kwargs,
    ):
        """Google Search API.

        Parameters:
        q (str): Required. Parameter defines the query you want to search.
            You can use anything that you would use in a regular Google search.
            e.g., inurl:, site:, intitle:. Advanced search query parameters are also supported.

        ludocid (str, optional): Parameter defines the id (CID) of the Google My Business listing you want to scrape.
            Also known as Google Place ID. Defaults to None.

        lsig (str, optional): Parameter to force the knowledge graph map view to show up. Defaults to None.

        kgmid (str, optional): Parameter defines the id (KGMID) of the Google Knowledge Graph listing you want to scrape.
            Also known as Google Knowledge Graph ID. Defaults to None.

        si (str, optional): Parameter defines the cached search parameters of the Google Search you want to scrape.
            Defaults to None.

        ibp (str, optional): Parameter for rendering layouts and expansions for some elements. Defaults to None.

        cr (str, optional): Parameter defines one or multiple countries to limit the search to.
            Uses country{two-letter upper-case country code} to specify countries and | as a delimiter. Defaults to None.

        lr (str, optional): Parameter defines one or multiple languages to limit the search to.
            Uses lang_{two-letter language code} to specify languages and | as a delimiter. Defaults to None.

        tbs (str, optional): Parameter defines advanced search parameters. Defaults to None.

        safe (str, optional): Parameter defines the level of filtering for adult content.
            Can be set to active or off. Defaults to None.

        nfpr (int, optional): Parameter defines the exclusion of results from an auto-corrected query.
            Can be set to 1 to exclude these results, or 0 to include them (default). Defaults to None.

        filter (int, optional): Parameter defines if the filters for 'Similar Results' and 'Omitted Results' are on or off.
            Can be set to 1 (default) to enable these filters, or 0 to disable these filters. Defaults to None.

        tbm (str, optional): Parameter defines the type of search you want to do.
            e.g., isch for Google Images, lcl for Google Local, shop for Google Shopping. Defaults to None.

        num_per_page (int, optional): Parameter defines the maximum number of results to return.
            Defaults to 10.

        max_pages (str, optional): Max pages.

        **kwargs: Additional keyword arguments.

        Returns:
        Response from the SerpApi search request.
        """
        ENGINE = "google"

        return await self._search(
            engine=ENGINE,
            q=q,
            ludocid=ludocid,
            lsig=lsig,
            kgmid=kgmid,
            si=si,
            ibp=ibp,
            cr=cr,
            lr=lr,
            tbs=tbs,
            safe=safe,
            nfpr=nfpr,
            filter=filter,
            tbm=tbm,
            num_per_page=num_per_page,
            max_pages=max_pages,
            **kwargs,
        )

    # (Custom) site
    async def site(
        self,
        q: str,
        ludocid: str = None,
        lsig: str = None,
        kgmid: str = None,
        si: str = None,
        ibp: str = None,
        cr: str = None,
        lr: str = None,
        tbs: str = None,
        safe: str = None,
        nfpr: str = None,
        filter: str = None,
        tbm: str = None,
        num_per_page: int = 100,
        max_pages: int = 1,
        **kwargs,
    ):
        """Google Search API.

        Parameters:
        q (str): Required. Parameter defines the query you want to search.
            You can use anything that you would use in a regular Google search.
            e.g., inurl:, site:, intitle:. Advanced search query parameters are also supported.

        ludocid (str, optional): Parameter defines the id (CID) of the Google My Business listing you want to scrape.
            Also known as Google Place ID. Defaults to None.

        lsig (str, optional): Parameter to force the knowledge graph map view to show up. Defaults to None.

        kgmid (str, optional): Parameter defines the id (KGMID) of the Google Knowledge Graph listing you want to scrape.
            Also known as Google Knowledge Graph ID. Defaults to None.

        si (str, optional): Parameter defines the cached search parameters of the Google Search you want to scrape.
            Defaults to None.

        ibp (str, optional): Parameter for rendering layouts and expansions for some elements. Defaults to None.

        cr (str, optional): Parameter defines one or multiple countries to limit the search to.
            Uses country{two-letter upper-case country code} to specify countries and | as a delimiter. Defaults to None.

        lr (str, optional): Parameter defines one or multiple languages to limit the search to.
            Uses lang_{two-letter language code} to specify languages and | as a delimiter. Defaults to None.

        tbs (str, optional): Parameter defines advanced search parameters. Defaults to None.

        safe (str, optional): Parameter defines the level of filtering for adult content.
            Can be set to active or off. Defaults to None.

        nfpr (int, optional): Parameter defines the exclusion of results from an auto-corrected query.
            Can be set to 1 to exclude these results, or 0 to include them (default). Defaults to None.

        filter (int, optional): Parameter defines if the filters for 'Similar Results' and 'Omitted Results' are on or off.
            Can be set to 1 (default) to enable these filters, or 0 to disable these filters. Defaults to None.

        tbm (str, optional): Parameter defines the type of search you want to do.
            e.g., isch for Google Images, lcl for Google Local, shop for Google Shopping. Defaults to None.

        num_per_page (int, optional): Parameter defines the maximum number of results to return.
            Defaults to 10.

        max_pages (str, optional): Max pages.

        **kwargs: Additional keyword arguments.

        Returns:
        Response from the SerpApi search request.
        """
        ENGINE = "google"

        return await self._search(
            engine=ENGINE,
            q=q,
            ludocid=ludocid,
            lsig=lsig,
            kgmid=kgmid,
            si=si,
            ibp=ibp,
            cr=cr,
            lr=lr,
            tbs=tbs,
            safe=safe,
            nfpr=nfpr,
            filter=filter,
            tbm=tbm,
            num_per_page=num_per_page,
            max_pages=max_pages,
            **kwargs,
        )

    ################################
    # Shopping
    ################################
    async def shopping(
        self,
        q: str,
        num_per_page: int = 100,
        max_pages: int = 1,
        **kwargs,
    ):
        """Google Shopping API.

        Parameters:
        q (str): Required. Parameter defines the query you want to search.
            You can use anything that you would use in a regular Google Shopping search.

        tbs (str, optional): Parameter defines advanced search parameters. Defaults to None.

        num_per_page (int, optional): Parameter defines the maximum number of results to return.
            Defaults to 10.

        max_pages (str, optional): Max pages.

        **kwargs: Additional keyword arguments.

        Returns:
        Response from the SerpApi search request.
        """
        ENGINE = "google_shopping"

        return await self._search(
            engine=ENGINE,
            q=q,
            num_per_page=num_per_page,
            max_pages=max_pages,
            **kwargs,
        )

    ################################
    # News
    ################################
    async def news(
        self,
        q: str,
        topic_token: str = None,
        publication_token: str = None,
        section_token: str = None,
        story_token: str = None,
        so: int = None,
        num_per_page: int = 100,
        max_pages: int = 1,
        **kwargs,
    ):
        """Google News API.

        Parameters:
        q (str): Required. Parameter defines the query you want to search.
            You can use anything that you would use in a regular Google News search. e.g. site:, when:.
            This parameter can't be used together with publication_token, story_token, and topic_token parameters.

        topic_token : str, optional
            Defines the Google News topic token. It is used for accessing the news results for a specific topic (e.g., "World", "Business", "Technology").
            The token can be found in our JSON response or the URL of the Google News page (in the URL, it is a string of characters preceded by /topics/).
            This parameter can't be used together with q, story_token, and publication_token parameters.

        publication_token : str, optional
            Defines the Google News publication token. It is used for accessing the news results from a specific publisher (e.g., "CNN", "BBC", "The Guardian").
            The token can be found in our JSON response or the URL of the Google News page (in the URL, it is a string of characters preceded by /publications/).
            This parameter can't be used together with q, story_token, and topic_token parameters.

        section_token : str, optional
            Defines the Google News section token. It is used for accessing the sub-section of a specific topic (e.g., "Business -> Economy").
            The token can be found in our JSON response or the URL of the Google News page (in the URL, it is a string of characters preceded by /sections/).
            This parameter can only be used in combination with topic_token or publication_token parameters.

        story_token : str, optional
            Defines the Google News story token. It is used for accessing the news results with full coverage of a specific story.
            The token can be found in our JSON response or the URL of the Google News page (in the URL, it is a string of characters preceded by /stories/).
            This parameter can't be used together with q, topic_token, and publication_token parameters.

        so : int, optional
            Defines the sorting method. Results can be sorted by relevance or by date. By default, the results are sorted by relevance.
            List of supported values are:
            0 - Relevance
            1 - Date
            This parameter can only be used in combination with story_token parameter.

        num_per_page (int, optional): Parameter defines the maximum number of results to return.
            Defaults to 10.

        max_pages (str, optional): Max pages.

        **kwargs: Additional keyword arguments.
        """
        ENGINE = "google_news"

        return await self._search(
            engine=ENGINE,
            q=q,
            topic_token=topic_token,
            publication_token=publication_token,
            section_token=section_token,
            story_token=story_token,
            so=so,
            num_per_page=num_per_page,
            max_pages=max_pages,
            **kwargs,
        )

    ################################
    # Trends
    ################################
    async def trends(
        self,
        q: str,
        geo: str = None,
        region: str = None,
        data_type: str = None,
        tz: int = None,
        cat: int = None,
        gprop: str = None,
        date: str = None,
        csv: str = None,
        num_per_page: int = 100,
        max_pages: int = 1,
        **kwargs,
    ):
        """Google Trends API.

        Parameters:

        q : str
            Required. Defines the query or queries you want to search. You can use anything that you would use in a regular Google Trends search.
            The maximum number of queries per search is 5 (this only applies to "Interest over time" and "Compared breakdown by region" data_type, other types of data will only accept 1 query per search).
            When passing multiple queries you need to use a comma (,) to separate them (e.g. coffee,pizza,dark chocolate,/m/027lnzs,bread).
            Query can be a "Search term" (e.g. World Cup, Eminem, iPhone, etc.) or a "Topic" (e.g. /m/0663v, /m/027lnzs, /g/11mw8j71m4, etc.). Queries that are "Topics" are encoded.
            To retrieve these values you can use our Google Trends Autocomplete API. Maximum length for each query is 100 characters.

        geo : str, optional
            Defines the location from where you want the search to originate. It defaults to Worldwide (activated when the value of geo parameter is not set or empty).
            Refer to the Google Trends Locations for a full list of supported Google Trends locations.

        region : str, optional
            Used for getting more specific results when using "Compared breakdown by region" and "Interest by region" data_type charts. Other data_type charts do not accept region parameter.
            The default value depends on the geo location that is set. Available options:
            - COUNTRY: Country
            - REGION: Subregion
            - DMA: Metro
            - CITY: City
            Note: Not all region options will return results for every geo location.

        data_type : str, optional
            Defines the type of search you want to do. Available options:
            - TIMESERIES: Interest over time (default) - Accepts both single and multiple queries per search.
            - GEO_MAP: Compared breakdown by region - Accepts only multiple queries per search.
            - GEO_MAP_0: Interest by region - Accepts only single query per search.
            - RELATED_TOPICS: Related topics - Accepts only single query per search.
            - RELATED_QUERIES: Related queries - Accepts only single query per search.

        tz : int, optional
            Defines a time zone offset. The default value is set to 420 (Pacific Day Time(PDT): -07:00). Value is shown in minutes and can span from -1439 to 1439.
            tz can be calculated using the time difference between UTC +0 and desired timezone.
            Examples:
            - 420: PDT
            - 600: Pacific/Tahiti
            - -540: Asia/Tokyo
            - -480: Canada/Pacific.
            Refer to the time zone database and your programming language UTC offset calculation for accuracy.

        cat : int, optional
            Defines a search category. The default value is set to 0 ("All categories"). Refer to the Google Trends Categories for a full list of supported Google Trends Categories.

        gprop : str, optional
            Used for sorting results by property. The default property is set to Web Search (activated when the value of gprop parameter is not set or empty).
            Other available options:
            - images: Image Search
            - news: News Search
            - froogle: Google Shopping
            - youtube: YouTube Search

        date : str, optional
            Defines a date. Available options:
            - now 1-H: Past hour
            - now 4-H: Past 4 hours
            - now 1-d: Past day
            - now 7-d: Past 7 days
            - today 1-m: Past 30 days
            - today 3-m: Past 90 days
            - today 12-m: Past 12 months
            - today 5-y: Past 5 years
            - all: 2004 - present
            You can also pass custom values:
            - Dates from 2004 to present: yyyy-mm-dd yyyy-mm-dd (e.g. 2021-10-15 2022-05-25)
            - Dates with hours within a week range: yyyy-mm-ddThh yyyy-mm-ddThh (e.g. 2022-05-19T10 2022-05-24T22). Hours will be calculated depending on the tz (time zone) parameter.

        csv : bool, optional
            Used for retrieving the CSV results. Set the parameter to true to retrieve CSV results as an array.

        num_per_page (int, optional): Parameter defines the maximum number of results to return.
            Defaults to 10.

        max_pages (str, optional): Max pages.

        **kwargs: Additional keyword arguments.
        """
        ENGINE = "google_trends"

        return await self._search(
            engine=ENGINE,
            q=q,
            geo=geo,
            region=region,
            data_type=data_type,
            tz=tz,
            cat=cat,
            gprop=gprop,
            date=date,
            csv=csv,
            num_per_page=num_per_page,
            max_pages=max_pages,
            **kwargs,
        )

    ################################
    # Related Questions
    ################################
    async def related_questions(
        self,
        next_page_token: str,
        **kwargs,
    ):
        """Google Related Questions.
        Parameters:

        next_page_token : str
            Required. Defines the token needed to show the additional related questions that Google generates when a specific question gets clicked.
            This token can be found in the Related Questions block returned in a regular Google Search API response.
        """
        ENGINE = "google_related_questions"

        return await self._search(engine=ENGINE, next_page_token=next_page_token, **kwargs)

    ################################
    # Scholar
    ################################
    async def scholar(
        self,
        q: str,
        sites: int = None,
        as_ylo: int = None,
        as_yhi: int = None,
        scisbd: str = 0,
        cluster: str = None,
        specs: str = None,
        lr: str = None,
        as_sdt: int = 0,
        safe: str = None,
        filter: int = 1,
        as_vis: int = 0,
        as_rr: int = 0,
        num_per_page: int = 100,
        max_pages: int = 1,
        **kwargs,
    ):
        """Google Scholar API.
        Parameters:

        q : str
            Required. Defines the query you want to search. You can also use helpers in your query such as: author:, or source:.
            Usage of cites parameter makes q optional. Usage of cites together with q triggers search within citing articles.
            Usage of cluster together with q and cites parameters is prohibited. Use cluster parameter only.

        cites : str, optional
            Defines unique ID for an article to trigger Cited By searches. Usage of cites will bring up a list of citing documents in Google Scholar.
            Example value: cites=1275980731835430123. Usage of cites and q parameters triggers search within citing articles.

        as_ylo : int, optional
            Defines the year from which you want the results to be included. (e.g. if you set as_ylo parameter to the year 2018, the results before that year will be omitted.).
            This parameter can be combined with the as_yhi parameter.

        as_yhi : int, optional
            Defines the year until which you want the results to be included. (e.g. if you set as_yhi parameter to the year 2018, the results after that year will be omitted.).
            This parameter can be combined with the as_ylo parameter.

        scisbd : int, optional
            Defines articles added in the last year, sorted by date. It can be set to 1 to include only abstracts, or 2 to include everything. The default value is 0 which means that the articles are sorted by relevance.

        cluster : str, optional
            Defines unique ID for an article to trigger All Versions searches. Example value: cluster=1275980731835430123.
            Usage of cluster together with q and cites parameters is prohibited. Use cluster parameter only.

        lr : str, optional
            Defines one or multiple languages to limit the search to. It uses lang_{two-letter language code} to specify languages and | as a delimiter.
            (e.g., lang_fr|lang_de will only search French and German pages). Refer to the Google lr languages for a full list of supported languages.

        as_sdt : int, optional
            Can be used either as a search type or a filter.
            As a Filter (only works when searching articles):
            - 0: exclude patents (default).
            - 7: include patents.
            As a Search Type:
            - 4: Select case law (US courts only). This will select all the State and Federal courts.
            Example: as_sdt=4 - Selects case law (all courts)
            To select specific courts, see the full list of supported Google Scholar courts.
            Example: as_sdt=4,33,192 - 4 is the required value and should always be in the first position, 33 selects all New York courts and 192 selects Tax Court.
            Values have to be separated by comma (,).

        safe : str, optional
            Defines the level of filtering for adult content. It can be set to active or off, by default Google will blur explicit content.

        filter : int, optional
            Defines if the filters for 'Similar Results' and 'Omitted Results' are on or off. It can be set to 1 (default) to enable these filters, or 0 to disable these filters.

        as_vis : int, optional
            Defines whether you would like to include citations or not. It can be set to 1 to exclude these results, or 0 (default) to include them.

        as_rr : int, optional
            Defines whether you would like to show only review articles or not (these articles consist of topic reviews, or discuss the works or authors you have searched for).
            It can be set to 1 to enable this filter, or 0 (default) to show all results.
        """
        ENGINE = "google_scholar"

        return await self._search(
            engine=ENGINE,
            q=q,
            sites=sites,
            as_ylo=as_ylo,
            as_yhi=as_yhi,
            scisbd=scisbd,
            cluster=cluster,
            specs=specs,
            lr=lr,
            as_sdt=as_sdt,
            safe=safe,
            filter=filter,
            as_vis=as_vis,
            as_rr=as_rr,
            num_per_page=num_per_page,
            max_pages=max_pages,
            **kwargs,
        )

    ################################
    # Product
    ################################
    async def product(
        self,
        product_id: str,
        offers: bool = None,
        specs: bool = None,
        reviews: bool = None,
        filter: str = None,
        offer_id: str = None,
        num_per_page: int = 100,
        max_pages: int = 1,
        **kwargs,
    ):
        """Google Product.
        Parameters:

        product_id : str
            Required. Defines the product to get results for. Normally found from shopping results for supported products (e.g., https://www.google.com/shopping/product/{product_id}).

        offers : bool, optional
            Parameter for fetching offers results. Replaces former sellers=online results. It can be set to 1 or true.
            The offers parameter cannot be used with offer_id parameter.

        specs : bool, optional
            Parameter for fetching specs results. It can be set to 1 or true.
            The specs parameter cannot be used with offer_id parameter.

        reviews : bool, optional
            Parameter for fetching reviews results. It can be set to 1 or true.
            The reviews parameter cannot be used with offer_id parameter.

        filter : str, optional
            Defines filters, sorting, and pagination for reviews and offers results.
            Offers filters:
            - freeship:1 Show only products with free shipping
            - ucond:1 Show only used products
            - scoring:p Sort by base price
            - scoring:tp Sort by total price
            - scoring:cpd Sort by current promotion deals (special offers)
            - scoring:mrd Sort by sellers rating

            Reviews filters:
            - rnum:{number} Number of results (100 is max).
            - rpt:{encoded value} Encoded pagination offset. You can get the value of rpt needed for the next page from the serpapi_pagination.
                next or serpapi_pagination.next_page_filter key in the JSON response to any Google Product API search with reviews enabled.
            It is recommended to use all filters provided in serpapi_pagination.next or serpapi_pagination.next_page_filter when paginating.

        offer_id : str, optional
            Defines ID used to fetch multiple offers from an online seller, and can be found inside sellers_results.online_sellers.
            The offer_id parameter can't be used with offers, specs, and reviews parameters.

        num_per_page (int, optional): Parameter defines the maximum number of results to return.
            Defaults to 10.

        max_pages (str, optional): Max pages.

        **kwargs: Additional keyword arguments.
        """
        ENGINE = "google_product"

        return await self._search(
            engine=ENGINE,
            product_id=product_id,
            offers=offers,
            specs=specs,
            reviews=reviews,
            filter=filter,
            offer_id=offer_id,
            num_per_page=num_per_page,
            max_pages=max_pages,
            **kwargs,
        )

    # (CUSTOM) product page
    async def product_page(self, product_id: str, num_per_page: int = 100, max_pages: int = 1, **kwargs):
        """Google Product.
        Parameters:

        product_id : str
            Required. Defines the product to get results for.
            Normally found from shopping results for supported products (e.g., https://www.google.com/shopping/product/{product_id}).

        num_per_page (int, optional): Parameter defines the maximum number of results to return.
            Defaults to 10.

        max_pages (str, optional): Max pages.

        **kwargs: Additional keyword arguments.
        """
        ENGINE = "google_product"
        SWITCH = {"offers": None, "specs": None, "reviews": None, "offer_id": None}
        EXCL_RESULTS_TYPES = ["online_sellers", "specs_results", "reviews_results", *PAGINATION_ATTRS]

        pages = await self._search(
            engine=ENGINE, product_id=product_id, **SWITCH, num_per_page=num_per_page, max_pages=max_pages, **kwargs
        )

        return self._filter_results_pages_by_results_types(pages, excl_results_types=EXCL_RESULTS_TYPES)

    # (CUSTOM) product offers
    async def product_offers(self, product_id: str, num_per_page: int = 100, max_pages: int = 1, **kwargs):
        """Google Product.
        Parameters:

        product_id : str
            Required. Defines the product to get results for.
            Normally found from shopping results for supported products (e.g., https://www.google.com/shopping/product/{product_id}).

        num_per_page (int, optional): Parameter defines the maximum number of results to return.
            Defaults to 10.

        max_pages (str, optional): Max pages.

        **kwargs: Additional keyword arguments.
        """
        ENGINE = "google_product"
        SWITCH = {"offers": True, "specs": None, "reviews": None, "offer_id": None}
        INCL_RESULTS_TYPES = [*METADATA_ATTRS, "online_sellers"]

        pages = await self._search(
            engine=ENGINE, product_id=product_id, **SWITCH, num_per_page=num_per_page, max_pages=max_pages, **kwargs
        )

        return self._filter_results_pages_by_results_types(pages, incl_results_types=INCL_RESULTS_TYPES)

    # (CUSTOM) product specs
    async def product_specs(self, product_id: str, num_per_page: int = 100, max_pages: int = 1, **kwargs):
        """Google Product.
        Parameters:

        product_id : str
            Required. Defines the product to get results for.
            Normally found from shopping results for supported products (e.g., https://www.google.com/shopping/product/{product_id}).

        num_per_page (int, optional): Parameter defines the maximum number of results to return.
            Defaults to 10.

        max_pages (str, optional): Max pages.

        **kwargs: Additional keyword arguments.
        """
        ENGINE = "google_product"
        SWITCH = {"offers": None, "specs": True, "reviews": None, "offer_id": None}
        INCL_RESULTS_TYPES = [*METADATA_ATTRS, "specs_results"]

        pages = await self._search(
            engine=ENGINE, product_id=product_id, **SWITCH, num_per_page=num_per_page, max_pages=max_pages, **kwargs
        )

        return self._filter_results_pages_by_results_types(pages, incl_results_types=INCL_RESULTS_TYPES)

    # (CUSTOM) product_reviews
    async def product_reviews(self, product_id: str, reviews_per_page: int = 100, **kwargs):
        """Google Product.
        [NOTE] reviews_per_page (rnum)은 최대 100이라고 했는데 99까지만 됨. 100을 넣으면 empty product 발생

        Parameters:

        product_id : str
            Required. Defines the product to get results for.
            Normally found from shopping results for supported products (e.g., https://www.google.com/shopping/product/{product_id}).

        reviews_per_page (int, optional): Parameter defines the maximum number of reviews to return.
            Max to 100, Defaults to 100.

        **kwargs: Additional keyword arguments.
        """
        ENGINE = "google_product"
        SWITCH = {"offers": None, "specs": None, "reviews": True, "offer_id": None}
        INCL_RESULTS_TYPES = [*METADATA_ATTRS, "reviews_results"]

        # first page
        first_page_filter = f"rnum:{reviews_per_page}"
        pages = await self._search(engine=ENGINE, product_id=product_id, **SWITCH, filter=first_page_filter, **kwargs)

        # other pages
        current_page = pages[0]
        reviews_cnt = current_page["product_results"].get("reviews")
        if not reviews_cnt:
            return
        fetched_reviews_cnt = len(current_page["reviews_results"]["reviews"])
        while fetched_reviews_cnt < reviews_cnt:
            if (current_page.get("serpapi_pagination") is None) or (
                current_page["serpapi_pagination"].get("next_page_filter") is None
            ):
                break
            next_page_filter = current_page["serpapi_pagination"]["next_page_filter"]
            next_pages = await self._search(
                engine=ENGINE, product_id=product_id, **SWITCH, filter=next_page_filter, **kwargs
            )
            current_page = next_pages[0]
            pages += next_pages
            fetched_reviews_cnt += len(current_page["reviews_results"]["reviews"])

        return self._filter_results_pages_by_results_types(pages, incl_results_types=INCL_RESULTS_TYPES)

    ################################
    # Videos
    ################################
    async def videos(
        self,
        q: str,
        lr: str = None,
        tbs: str = None,
        safe: str = None,
        nfpr: str = None,
        filter: str = None,
        num_per_page: int = 100,
        max_pages: int = 1,
        **kwargs,
    ):
        """Google Videos.
        Parameters:

        q : str
            Required. Defines the query you want to search. You can use anything that you would use in a regular Google Videos search.
            Examples include: inurl:, site:, intitle:. Advanced search query parameters such as as_dt and as_eq are also supported.
            Refer to the full list of supported advanced search query parameters for more details.

        lr : str, optional
            Defines one or multiple languages to limit the search to. It uses lang_{two-letter language code} to specify languages and | as a delimiter.
            (e.g., lang_fr|lang_de will only search French and German pages).
            Refer to the Google lr languages page for a full list of supported languages.

        tbs : str, optional
            Defines advanced search parameters that aren't possible in the regular query field.
            Examples include advanced search for patents, dates, news, videos, images, apps, or text contents.

        safe : str, optional
            Defines the level of filtering for adult content. It can be set to active or off. By default, Google will blur explicit content.

        nfpr : int, optional
            Defines the exclusion of results from an auto-corrected query when the original query is spelled wrong.
            It can be set to 1 to exclude these results, or 0 to include them (default). Note that this parameter may not prevent Google from returning results
            for an auto-corrected query if no other results are available.

        filter : int, optional
            Defines if the filters for 'Similar Results' and 'Omitted Results' are on or off.
            It can be set to 1 (default) to enable these filters, or 0 to disable these filters.
        """
        ENGINE = "google_videos"

        return await self._search(
            engine=ENGINE,
            q=q,
            lr=lr,
            tbs=tbs,
            safe=safe,
            nfpr=nfpr,
            filter=filter,
            num_per_page=num_per_page,
            max_pages=max_pages,
            **kwargs,
        )

    ################################
    # Patents
    ################################
    async def patents(
        self,
        q: str,
        sort: str = None,
        clustered: str = None,
        dups: str = None,
        patents: str = None,
        scholar: str = None,
        before: str = None,
        after: str = None,
        inventor: str = None,
        assignee: str = None,
        country: str = None,
        language: str = None,
        status: str = None,
        type: str = None,
        litigation: str = None,
        num_per_page: int = 100,
        max_pages: int = 1,
        **kwargs,
    ):
        """Google Pagtents API.
        Parameters:

        q : str, optional
            Defines the query you want to search. You can split multiple search terms with semicolon (;). For advanced search syntax, please refer to About Google Patents.
            Example for single search term: (Coffee) OR (Tea)
            Example for multiple search terms (separated by semicolon ;): (Coffee) OR (Tea);(A47J)

        page : int, optional
            Defines the page number. It's used for pagination. (e.g., 1 (default) is the first page of results, 2 is the 2nd page of results, etc.).

        num : int, optional
            Controls the number of results per page. Minimum: 10, Maximum: 100.

        sort : str, optional
            Defines the sorting method. By default, the results are sorted by Relevance.
            List of supported values are:
            - new: Newest
            - old: Oldest
            Patent results are sorted by filing_date while scholar results are sorted by publication_date for new and old values.

        clustered : str, optional
            Defines how the results should be grouped.
            List of supported values are:
            - true: Classification

        dups : str, optional
            Defines the method of deduplication. Either Family (default) or Publication.
            List of supported values are:
            - language: Publication

        patents : bool, optional
            Controls whether or not to include Google Patents results. (Defaults to true)

        scholar : bool, optional
            Controls whether or not to include Google Scholar results. (Defaults to false)

        before : str, optional
            Defines the maximum date of the results. The format of this field is type:YYYYMMDD. type can be one of priority, filing, and publication.
            Example:
            - priority:20221231
            - publication:20230101

        after : str, optional
            Defines the minimum date of the results. The format of this field is type:YYYYMMDD. type can be one of priority, filing, and publication.
            Example:
            - priority:20221231
            - publication:20230101

        inventor : str, optional
            Defines the inventors of the patents. Split multiple inventors with , (comma).

        assignee : str, optional
            Defines the assignees of the patents. Split multiple assignees with , (comma).

        country : str, optional
            Filters patent results by countries. Split multiple country codes with , (comma).
            List of supported country codes. Example:WO,US.

        language : str, optional
            Filters patent results by languages. Split multiple languages with , (comma).
            List of supported values are:
            - ENGLISH
            - GERMAN
            - CHINESE
            - FRENCH
            - SPANISH
            - ARABIC
            - JAPANESE
            - KOREAN
            - PORTUGUESE
            - RUSSIAN
            - ITALIAN
            - DUTCH
            - SWEDISH
            - FINNISH
            - NORWEGIAN
            - DANISH
            Example:ENGLISH,GERMAN.

        status : str, optional
            Filters patent results by status.
            List of supported values are:
            - GRANT: Grant
            - APPLICATION: Application

        type : str, optional
            Filters patent results by type.
            List of supported values are:
            - PATENT: Patent
            - DESIGN: Design

        litigation : str, optional
            Filters patent results by litigation status.
            List of supported values are:
            - YES: Has Related Litigation
            - NO: No Known Litigation
        """
        ENGINE = "google_patents"

        return await self._search(
            engine=ENGINE,
            q=q,
            sort=sort,
            clustered=clustered,
            dups=dups,
            patents=patents,
            scholar=scholar,
            before=before,
            after=after,
            inventor=inventor,
            assignee=assignee,
            country=country,
            language=language,
            status=status,
            type=type,
            litigation=litigation,
            num_per_page=num_per_page,
            max_pages=max_pages,
            **kwargs,
        )

    ################################
    # YouTube
    ################################
    async def yotube(
        self,
        search_query: str,
        sp: str = None,
        **kwargs,
    ):
        """YouTube
        Parameters:

        search_query : str
            Required. Defines the search query. You can use anything that you would use in a regular YouTube search.

        sp : str, optional
            Can be used for pagination. YouTube uses continuous pagination and the next page token can be found in the SerpApi JSON response
            `serpapi_pagination -> next_page_token` and `pagination -> next_page_token` fields.

            Can also be used to filter the search results:
            - By Upload date: CAI%3D
            - By 4K: EgJwAQ%3D%3D
            - For forcing the exact search query spelling: QgIIAQ%3D%3D

            If you are interested in passing other filters, visit the YouTube website, set the filters you want, and copy the sp value from their URL to the SerpApi URL.
        """
        ENGINE = "youtube"

        return await self._search(engine=ENGINE, search_query=search_query, sp=sp, **kwargs)

    ################################
    # Immersive Product
    ################################
    async def immersive_product(self, page_token: str, **kwargs):
        """Google Immersive Product.
        Parameters:

        page_token : str
            Required. Defines the token needed to show more product info in Google immersive popup.
            Token is generated by SerpApi using our Google Immersive Product API.
        """
        ENGINE = "google_immersive_product"

        return await self._search(engine=ENGINE, page_token=page_token, **kwargs)
