from argparse import Namespace
from datetime import datetime
from time import sleep, time_ns
import logging
from itertools import islice
import json
from functools import partial

from tqdm.contrib.concurrent import thread_map

from callusgs import Api
from callusgs import Types
from callusgs.utils import (
    ogr2internal,
    month_names_to_index,
    report_usgs_messages,
    downloadable_and_preparing_scenes,
    singular_download,
)

api_logger = logging.getLogger("callusgs")

BYTES_TO_GB = 9.3132257461548e-10


def download(args: Namespace):
    """
    _summary_

    :param args: CLI args
    :type args: Namespace
    """
    download_logger = logging.getLogger("callusgs.download")
    logging.basicConfig(
        level=(
            logging.DEBUG
            if args.very_verbose
            else logging.INFO if args.verbose else logging.WARNING
        ),
        format="%(asctime)s [%(name)s %(levelname)s]: %(message)s",
    )
    for handler in logging.root.handlers:
        handler.addFilter(logging.Filter("callusgs"))
        handler.setLevel(
            logging.DEBUG
            if args.very_verbose
            else logging.INFO if args.verbose else logging.WARNING
        )

    download_logger.debug(f"CLI tool started with the following args: {vars(args)}")

    assert (
        args.username is not None and args.auth is not None
    ), "Username and/or Authentication key (e.g. password, token) not specified"
    assert (
        args.cloudcover[0] >= 0
        and args.cloudcover[1] <= 100
        and args.cloudcover[0] <= args.cloudcover[1]
    ), "cloud cover must be from 0 to 100 and minimal cloud cover must be smaller or equal to upper bound"
    assert datetime.strptime(args.date[0], "%Y-%m-%d") <= datetime.strptime(
        args.date[1], "%Y-%m-%d"
    ), "Start date must be earlier or on same day than end date"
    assert (
        args.aoi_coordinates is not None or args.aoi_file is not None
    ), "Either coordinate list or file with AOI must be given"
    if args.aoi_coordinates is not None:
        assert (
            len(args.aoi_coordinates) % 2
        ) == 0, "Number of coordinates given must be even"
        if len(args.aoi_coordinates) > 2:
            assert (
                args.aoi_coordinates[:2] == args.aoi_coordinates[-2:]
            ), "Polygon ring must be closed"
        else:
            assert (
                args.aoi_type != "Mbr"
            ), "Point coordinate can't be used with Mbr AOI type"

    download_logger.info("Passed preconditions")

    args.outdir.mkdir(parents=True, exist_ok=True)

    coordinates = None
    if args.aoi_coordinates:
        if len(args.aoi_coordinates) == 2:
            coordinates = Types.GeoJson("Point", args.aoi_coordinates[::-1])
        else:
            coordinates = Types.GeoJson(
                "Polygon",
                [
                    list(
                        zip(
                            islice(
                                args.aoi_coordinates, 1, len(args.aoi_coordinates), 2
                            ),
                            islice(
                                args.aoi_coordinates, 0, len(args.aoi_coordinates), 2
                            ),
                        )
                    )
                ],
            )

        if coordinates.type == "Polygon" and args.aoi_type == "Mbr":
            coordinates = (
                Types.Coordinate(
                    min([lat for lon, lat in coordinates.coordinates]),
                    min([lon for lon, lat in coordinates.coordinates]),
                ),
                Types.Coordinate(
                    max([lat for lon, lat in coordinates.coordinates]),
                    max([lon for lon, lat in coordinates.coordinates]),
                ),
            )
    if args.aoi_file:
        coordinates = ogr2internal(args.aoi_file, args.aoi_type)

    scene_filter = Types.SceneFilter(
        acquisition_filter=Types.AcquisitionFilter(*args.date),
        cloudcover_filter=Types.CloudCoverFilter(
            *args.cloudcover, args.include_unknown_clouds
        ),
        dataset_name=args.product,
        ingest_filter=None,
        metadata_filter=None,
        seasonal_filter=(
            None if "all" in args.months else month_names_to_index(args.months)
        ),
        spatial_filter=(
            Types.SpatialFilterMbr(*coordinates)
            if args.aoi_type == "Mbr"
            else Types.SpatialFilterGeoJson(coordinates)
        ),
    )

    download_logger.info("Constructed scene filter")

    with Api(
        relogin=not args.no_relogin,
        method=args.auth_method,
        user=args.username,
        auth=args.auth,
    ) as ee_session:
        report_usgs_messages(ee_session.notifications("EE").data)
        report_usgs_messages(ee_session.notifications("M2M").data)
        report_usgs_messages(ee_session.dataset_messages("EE", dataset_name=args.product).data)

        if "order" not in ee_session.permissions().data or "download" not in ee_session.permissions().data:
            raise RuntimeError("Either 'order' or 'downlaod' permission not present for user. "
                               "Did you request access to the M2M API from your ERS profile at 'https://ers.cr.usgs.gov/profile/access'?")

        # use scene-search to query scenes
        entities = []
        scene_search_results = ee_session.scene_search(
            args.product, scene_filter=scene_filter
        )
        initially_discovered_products = scene_search_results.data["totalHits"]
        download_logger.info(
            f"Request {scene_search_results.request_id} in session {scene_search_results.session_id}: Found {initially_discovered_products} scenes for request"
        )

        if initially_discovered_products == 0:
            download_logger.warning("Found no scenes")
            exit(0)

        entities.extend(
            search_result["entityId"]
            for search_result in scene_search_results.data["results"]
        )

        while (
            start_num := scene_search_results.data["nextRecord"]
        ) != initially_discovered_products and start_num != 0:
            scene_search_results = ee_session.scene_search(
                args.product, scene_filter=scene_filter, starting_number=start_num
            )
            entities.extend(
                search_result["entityId"]
                for search_result in scene_search_results.data["results"]
            )
            download_logger.info(
                f"Request {scene_search_results.request_id} in session {scene_search_results.session_id}: Walking over paged search results ({start_num}/{initially_discovered_products})"
            )

        assert (
            len(entities) == initially_discovered_products
        ), "Whoops, some scenes went missing"

        download_logger.debug(
            f"Search filter: {json.dumps(scene_filter, default=vars)}"
        )

        download_label = str(time_ns())
        ## use download-options to get id which is needed for download together with entityId; only if product is marked as available and potentially secondary file groups set to true
        ##      I don't fully understand all of the other scene entires in the response but filtering for "available" works and only gets the product bundles
        entity_download_options = ee_session.download_options(
            args.product, entities, include_secondary_file_groups=False
        )
        download_logger.info(
            f"Request {entity_download_options.request_id} in session {entity_download_options.session_id}: Requested download options"
        )

        available_downloads = []
        total_size = 0
        for i in entity_download_options.data:
            # band files are marked as not available; but since I'm only interested in product bundles I don't care
            if i["available"]:
                available_downloads.append((i["entityId"], i["id"]))
                total_size += i["filesize"]
        downloads_to_request = [
            Types.DownloadInput(*i, None, download_label) for i in available_downloads
        ]

        download_logger.info(
            f"Total size to download is {total_size * BYTES_TO_GB:.2f} Gb"
        )

        if args.dry_run:
            download_logger.info("Not performing download as dry run was requested.")

            ## and now delete the label (i.e. remove order from download queue)
            ee_session.download_order_remove(label=download_label)
            download_logger.debug(f"Removed order {download_label}")
            exit(0)

        # TODO change test to order
        ## use download-request to request products and set a label
        requested_downloads = ee_session.download_request(
            "test", downloads=downloads_to_request, label=download_label
        )
        download_logger.info(
            f"Request {requested_downloads.request_id} in session {requested_downloads.session_id}: Requested downloads for available scenes"
        )

        ## use download-retrieve to retrieve products, regardless of their status (can be checked to if looping over requested downloads is needed)
        ueids = set()
        preparing_ueids = set()
        download_dict = {}
        retrieved_downloads = ee_session.download_retrieve(label=download_label)
        download_logger.info(
            f"Request {retrieved_downloads.request_id} in session {retrieved_downloads.session_id}: Retrieved download queue"
        )
        ueids, download_dict, preparing_ueids = downloadable_and_preparing_scenes(
            [i for i in retrieved_downloads.data["available"] + retrieved_downloads.data["requested"] if "Product Bundle" in i["productName"]]
        )

        assert len(ueids) == len(download_dict) and (
            len(ueids) + len(preparing_ueids)
        ) == len(entities), "Hm, now here are scenes missing"

        # TODO come up with a nicer way to do this
        #   This now bloack download until all scenes are available
        while preparing_ueids:
            download_logger.info(
                "Did not get all downloads, trying again in 30 seconds"
            )
            sleep(30)
            retrieved_downloads = ee_session.download_retrieve(label=download_label)
            download_logger.info(
                f"Request {retrieved_downloads.request_id} in session {retrieved_downloads.session_id}: Retrieved download queue"
            )
            ueids, new_download_dict, new_preparing_ueids = (
                downloadable_and_preparing_scenes(
                    [i for i in retrieved_downloads.data["available"] + retrieved_downloads.data["requested"] if "Product Bundle" in i["productName"]],
                    ueids,
                )
            )
            download_dict.update(new_download_dict)
            preparing_ueids.difference_update(new_preparing_ueids)

        assert len(ueids) == len(download_dict) and len(download_dict) == len(entities),\
            "How are scenes missing at this point?"

        ## use download method to download files
        _ = thread_map(partial(singular_download, connection=ee_session, outdir=args.outdir), download_dict.items(), max_workers=5, desc="Total scenes downloaded")

        ## and now delete the label (i.e. remove order from download queue)
        ee_session.download_order_remove(label=download_label)
        download_logger.info(f"Removed order {download_label}")


def geocode(args: Namespace):
    geocode_logger = logging.getLogger("callusgs")
    with Api(method=args.auth_method, user=args.username, auth=args.auth) as ee_session:
        print(vars(ee_session.placename(args.feature, args.name)))


def grid2ll(args: Namespace):
    grid2ll_logger = logging.getLogger("callusgs")
    with Api(method=args.auth_method, user=args.username, auth=args.auth) as ee_session:
        print(ee_session.grid2ll(args.grid, args.response_shape, args.path, args.row))
