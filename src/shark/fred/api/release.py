"""The "fred/release" and "fred/releases" API.

See the official FRED API docs for more info:
    https://fred.stlouisfed.org/docs/api/fred/

"""

from typing import ClassVar

import pandas as pd

from ._api import Dataset, get


class _ReleasesDates(Dataset):
    """Get release dates for all releases of economic data."""

    #: FRED API endpoint name.
    endpoint: ClassVar[str] = "releases/dates"

    @classmethod
    def get(
        cls,
        *,
        realtime_start: None | int | str = None,
        realtime_end: None | int | str = None,
        limit: None | int = 1000,
        offset: None | int = 0,
        order_by: None | str = "release_date",
        sort_order: None | str = "desc",
        include_release_dates_with_no_data: None | bool = False,
        api_key: None | str = None,
    ) -> pd.DataFrame:
        """Get all releases of economic data.

        See the related FRED API documentation at:
            https://fred.stlouisfed.org/docs/api/fred/releases_dates.html

        Args:
            realtime_start: Start date for fetching results
                according to their publication date.
            realtime_end: End date for fetching results according
                to their publication date.
            limit: Maximum number of results to return.
            offset: Result start offset.
            order_by: Variable to order results by.
                Options include:
                    - "release_date"
                    - "release_id"
                    - "release_name"
            sort_order: Sort results in ascending ("asc") or
                descending ("desc") order.
            include_release_dates_with_no_data: Whether to return release
                dates that don't contain any data.
            api_key: Your FRED API key. Pulled from the `FRED_API_KEY`
                environment variable if left `None`.

        Returns:
            A dataframe containing data on release dates for all
            releases of economic data.

        """
        data = get(
            cls.url,
            realtime_start=realtime_start,
            realtime_end=realtime_end,
            limit=limit,
            offset=offset,
            order_by=order_by,
            sort_order=sort_order,
            include_release_dates_with_no_data=include_release_dates_with_no_data,
            api_key=api_key,
        ).json()
        data = data["releases"]
        return pd.DataFrame(data)


class _Releases(Dataset):
    """Get all releases of economic data."""

    #: "releases/dates" FRED API. Get dates for releases of economic data.
    dates: ClassVar[type[_ReleasesDates]] = _ReleasesDates

    #: FRED API endpoint name.
    endpoint: ClassVar[str] = "releases"

    @classmethod
    def get(
        cls,
        *,
        realtime_start: None | int | str = None,
        realtime_end: None | int | str = None,
        limit: None | int = 1000,
        offset: None | int = 0,
        order_by: None | str = "release_id",
        sort_order: None | str = "asc",
        api_key: None | str = None,
    ) -> pd.DataFrame:
        """Get all releases of economic data.

        See the related FRED API documentation at:
            https://fred.stlouisfed.org/docs/api/fred/releases.html

        Args:
            realtime_start: Start date for fetching results
                according to their publication date.
            realtime_end: End date for fetching results according
                to their publication date.
            limit: Maximum number of results to return.
            offset: Result start offset.
            order_by: Variable to order results by.
                Options include:
                    - "release_id"
                    - "name"
                    - "press_release"
                    - "realtime_start"
                    - "realtime_end"
            sort_order: Sort results in ascending ("asc") or
                descending ("desc") order.
            api_key: Your FRED API key. Pulled from the `FRED_API_KEY`
                environment variable if left `None`.

        Returns:
            A dataframe containing data on all releases of economic
            data.

        """
        data = get(
            cls.url,
            realtime_start=realtime_start,
            realtime_end=realtime_end,
            limit=limit,
            offset=offset,
            order_by=order_by,
            sort_order=sort_order,
            api_key=api_key,
        ).json()
        data = data["releases"]
        return pd.DataFrame(data)


class _ReleaseDates(Dataset):
    """Get data on release dates for a particular release of economic data."""

    #: FRED API endpoint name.
    endpoint: ClassVar[str] = "release/dates"

    @classmethod
    def get(
        cls,
        release_id: int,
        /,
        *,
        realtime_start: None | int | str = None,
        realtime_end: None | int | str = None,
        limit: None | int = 10000,
        offset: None | int = 0,
        sort_order: None | str = "asc",
        include_release_dates_with_no_data: None | bool = False,
        api_key: None | str = None,
    ) -> pd.DataFrame:
        """Get data on release dates for a particular release of economic data.

        See the related FRED API documentation at:
            https://fred.stlouisfed.org/docs/api/fred/release_dates.html

        Args:
            release_id: The ID for a release.
            realtime_start: Start date for fetching results
                according to their publication date.
            realtime_end: End date for fetching results according
                to their publication date.
            limit: Maximum number of results to return.
            offset: Result start offset.
            sort_order: Sort results in ascending ("asc") or
                descending ("desc") order.
            include_release_dates_with_no_data: Whether to return release
                dates that don't contain any data.
            api_key: Your FRED API key. Pulled from the `FRED_API_KEY`
                environment variable if left `None`.

        Returns:
            A dataframe containing data for an economic data release's release dates.

        """
        data = get(
            cls.url,
            release_id=release_id,
            realtime_start=realtime_start,
            realtime_end=realtime_end,
            limit=limit,
            offset=offset,
            sort_order=sort_order,
            include_release_dates_with_no_data=include_release_dates_with_no_data,
            api_key=api_key,
        ).json()
        data = data["release_dates"]
        return pd.DataFrame(data)


class _Series(Dataset):
    """Get data on the series related to a release of economic data."""

    #: FRED API endpoint name.
    endpoint: ClassVar[str] = "release/series"

    @classmethod
    def get(
        cls,
        release_id: int,
        /,
        *,
        realtime_start: None | int | str = None,
        realtime_end: None | int | str = None,
        limit: None | int = 1000,
        offset: None | int = 0,
        order_by: None | str = "series_id",
        sort_order: None | str = "asc",
        filter_variable: None | str = None,
        filter_value: None | str = None,
        tag_names: None | str | list[str] = None,
        exclude_tag_names: None | str | list[str] = None,
        api_key: None | str = None,
    ) -> pd.DataFrame:
        """Get data on the series related to a release of economic data.

        See the related FRED API documentation at:
            https://fred.stlouisfed.org/docs/api/fred/release_series.html

        Args:
            release_id: The ID for a release.
            realtime_start: Start date for fetching results
                according to their publication date.
            realtime_end: End date for fetching results according
                to their publication date.
            limit: Maximum number of results to return.
            offset: Result start offset.
            order_by: Variable to order results by.
                Options include:
                    - "series_id"
                    - "title"
                    - "units"
                    - "frequency"
                    - "seasonal_adjustment"
                    - "realtime_start"
                    - "realtime_end"
                    - "last_updated"
                    - "observation_start"
                    - "observation_end"
                    - "popularity"
                    - "group_popularity"
            sort_order: Sort results in ascending ("asc") or
                descending ("desc") order.
            filter_variable: The attribute (or column) to filter results by.
                Options include:
                    - "frequency"
                    - "units"
                    - "seasonal_adjustment"
            filter_value: The value of `filter_variable` to filter results
                by.
            tag_names: Find tags related to these tags.
            exclude_tag_names: Exclude tags related to these tags.
            api_key: Your FRED API key. Pulled from the `FRED_API_KEY`
                environment variable if left `None`.

        Returns:
            A dataframe containing series data for a release.

        """
        data = get(
            cls.url,
            release_id=release_id,
            realtime_start=realtime_start,
            realtime_end=realtime_end,
            limit=limit,
            offset=offset,
            order_by=order_by,
            sort_order=sort_order,
            filter_variable=filter_variable,
            filter_value=filter_value,
            tag_names=tag_names,
            exclude_tag_names=exclude_tag_names,
            api_key=api_key,
        ).json()
        data = data["seriess"]
        return pd.DataFrame(data)


class _Sources(Dataset):
    """Get sources related to an economic release."""

    #: FRED API endpoint name.
    endpoint: ClassVar[str] = "release/sources"

    @classmethod
    def get(
        cls,
        release_id: int,
        /,
        *,
        realtime_start: None | int | str = None,
        realtime_end: None | int | str = None,
        api_key: None | str = None,
    ) -> pd.DataFrame:
        """Get sources related to an economic release.

        See the related FRED API documentation at:
            https://fred.stlouisfed.org/docs/api/fred/release_sources.html

        Args:
            release_id: The ID for a release.
            realtime_start: Start date for fetching results
                according to their publication date.
            realtime_end: End date for fetching results according
                to their publication date.
            api_key: Your FRED API key. Pulled from the `FRED_API_KEY`
                environment variable if left `None`.

        Returns:
            A dataframe containing sources related to an economic release.

        """
        data = get(
            cls.url,
            release_id=release_id,
            realtime_start=realtime_start,
            realtime_end=realtime_end,
            api_key=api_key,
        ).json()
        data = data["sources"]
        return pd.DataFrame(data)


class _Tags(Dataset):
    """Get tags for an economic release."""

    #: FRED API endpoint name.
    endpoint: ClassVar[str] = "release/tags"

    @classmethod
    def get(
        cls,
        release_id: int,
        /,
        *,
        realtime_start: None | int | str = None,
        realtime_end: None | int | str = None,
        tag_names: None | str | list[str] = None,
        tag_group_id: None | str = None,
        search_text: None | str | list[str] = None,
        limit: None | int = 1000,
        offset: None | int = 0,
        order_by: None | str = "series_count",
        sort_order: None | str = "asc",
        api_key: None | str = None,
    ) -> pd.DataFrame:
        """Get tags for an economic release.

        See the related FRED API documentation at:
            https://fred.stlouisfed.org/docs/api/fred/release_tags.html

        Args:
            release_id: The ID for a release.
            realtime_start: Start date for fetching results
                according to their publication date.
            realtime_end: End date for fetching results according
                to their publication date.
            tag_names: Filtering of tag names to include in the results.
            tag_group_id: A tag group ID to filter tags by.
                Options include:
                    - "freq" = frequency
                    - "gen" = general or concept
                    - "geo" = geography
                    - "geot" = geography type
                    - "rls" = release
                    - "seas" = seasonal adjustment
                    - "src" = source
            search_text: The words to find matching tags with.
            limit: Maximum number of results to return.
            offset: Result start offset.
            order_by: Variable to order results by.
                Options include:
                    - "series_count"
                    - "popularity"
                    - "created"
                    - "name"
                    - "group_id"
            sort_order: Sort results in ascending ("asc") or
                descending ("desc") order.
            api_key: Your FRED API key. Pulled from the `FRED_API_KEY`
                environment variable if left `None`.

        Returns:
            A dataframe containing data for an economic release's tags
            according to the given parameters.

        """
        data = get(
            cls.url,
            release_id=release_id,
            realtime_start=realtime_start,
            realtime_end=realtime_end,
            tag_names=tag_names,
            tag_group_id=tag_group_id,
            search_text=search_text,
            limit=limit,
            offset=offset,
            order_by=order_by,
            sort_order=sort_order,
            api_key=api_key,
        ).json()
        data = data["tags"]
        return pd.DataFrame(data)


class _RelatedTags(Dataset):
    """Get tags related to an economic release."""

    #: FRED API endpoint name.
    endpoint: ClassVar[str] = "release/related_tags"

    @classmethod
    def get(
        cls,
        release_id: int,
        /,
        *,
        realtime_start: None | int | str = None,
        realtime_end: None | int | str = None,
        tag_names: None | str | list[str] = None,
        exclude_tag_names: None | str | list[str] = None,
        tag_group_id: None | str = None,
        search_text: None | str | list[str] = None,
        limit: None | int = 1000,
        offset: None | int = 0,
        order_by: None | str = "series_count",
        sort_order: None | str = "asc",
        api_key: None | str = None,
    ) -> pd.DataFrame:
        """Get data for tags related to an economic release.

        See the related FRED API documentation at:
            https://fred.stlouisfed.org/docs/api/fred/release_related_tags.html

        Args:
            release_id: The ID for a release.
            realtime_start: Start date for fetching results
                according to their publication date.
            realtime_end: End date for fetching results according
                to their publication date.
            tag_names: Find tags related to these tags.
            exclude_tag_names: Exclude tags related to these tags.
            tag_group_id: A tag group ID to filter tags by.
                Options include:
                    - "freq" = frequency
                    - "gen" = general or concept
                    - "geo" = geography
                    - "geot" = geography type
                    - "rls" = release
                    - "seas" = seasonal adjustment
                    - "src" = source
            search_text: The words to find matching tags with.
            limit: Maximum number of results to return.
            offset: Result start offset.
            order_by: Variable to order results by.
                Options include:
                    - "series_count"
                    - "popularity"
                    - "created"
                    - "name"
                    - "group_id"
            sort_order: Sort results in ascending ("asc") or
                descending ("desc") order.
            api_key: Your FRED API key. Pulled from the `FRED_API_KEY`
                environment variable if left `None`.

        Returns:
            A dataframe containing data for tags related to an economic
            release according to the given parameters.

        """
        data = get(
            cls.url,
            release_id=release_id,
            realtime_start=realtime_start,
            realtime_end=realtime_end,
            tag_names=tag_names,
            exclude_tag_names=exclude_tag_names,
            tag_group_id=tag_group_id,
            search_text=search_text,
            limit=limit,
            offset=offset,
            order_by=order_by,
            sort_order=sort_order,
            api_key=api_key,
        ).json()
        data = data["tags"]
        return pd.DataFrame(data)


class _Tables(Dataset):
    """Get release tables for a given economic release."""

    #: FRED API endpoint name.
    endpoint: ClassVar[str] = "release/tables"

    @classmethod
    def get(
        cls,
        release_id: int,
        /,
        *,
        element_id: None | int = 0,
        include_observation_values: None | bool = False,
        observation_date: None | str = None,
        api_key: None | str = None,
    ) -> pd.DataFrame:
        """Get release tables for a given economic release.

        See the related FRED API documentation at:
            https://fred.stlouisfed.org/docs/api/fred/release_tables.html

        Args:
            release_id: The ID for a release.
            element_id: The release table element you'd like to retrieve.
            include_observation_values: A flag indicating whether observations
                need to be returned.
            observation_date: The observation date to be included with the
                returned release table.
            api_key: Your FRED API key. Pulled from the `FRED_API_KEY`
                environment variable if left `None`.

        Returns:
            A dataframe of release tables for a given economic release.

        """
        data = get(
            cls.url,
            release_id=release_id,
            element_id=element_id,
            include_observation_values=include_observation_values,
            observation_date=observation_date,
            api_key=api_key,
        ).json()
        data = data["tables"]
        return pd.DataFrame(data)


class _Release(Dataset):
    """Collection of `fred/release` APIs."""

    #: "release/dates" FRED API. Get economic release dates.
    dates: ClassVar[type[_ReleaseDates]] = _ReleaseDates

    #: FRED API endpoint name.
    endpoint: ClassVar[str] = "release"

    #: "release/related_tags" FRED API. Get tags related to an economic release.
    related_tags: ClassVar[type[_RelatedTags]] = _RelatedTags

    #: "release/series" FRED API. Get the series of an economic release.
    series: ClassVar[type[_Series]] = _Series

    #: "release/sources" FRED API. Get the sources for an economic release.
    sources: ClassVar[type[_Sources]] = _Sources

    #: "release/tables" FRED API. Get the tables of an economic release.
    tables: ClassVar[type[_Tables]] = _Tables

    #: "release/tags" FRED API. Get tags of an economic release.
    tags: ClassVar[type[_Tags]] = _Tags

    @classmethod
    def get(
        cls,
        release_id: int,
        /,
        *,
        realtime_start: None | int | str = None,
        realtime_end: None | int | str = None,
        api_key: None | str = None,
    ) -> pd.DataFrame:
        """Get overview data of an economic release.

        See the related FRED API documentation at:
            https://fred.stlouisfed.org/docs/api/fred/release.html

        Args:
            release_id: The ID for a release.
            realtime_start: Start date for fetching results
                according to their publication date.
            realtime_end: End date for fetching results according
                to their publication date.
            api_key: Your FRED API key. Pulled from the `FRED_API_KEY`
                environment variable if left `None`.

        Returns:
            A dataframe containing high-level info on an economic release.

        """
        data = get(
            cls.url,
            release_id=release_id,
            realtime_start=realtime_start,
            realtime_end=realtime_end,
            api_key=api_key,
        ).json()
        data = data["releases"]
        return pd.DataFrame(data)


#: Public-facing "fred/release" and "fred/releases" APIs.
releases = _Releases
release = _Release
