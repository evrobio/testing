from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from rest_framework import permissions

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from .views import (
    AboutStats,
    APITokenView,
    CompendiumResultDetails,
    CompendiumResultList,
    ComputationalResultsList,
    ComputedFilesList,
    CreateApiTokenView,
    CreateDatasetView,
    DatasetView,
    DownloaderJobList,
    ExperimentDetail,
    ExperimentDocumentView,
    ExperimentList,
    FailedDownloaderJobStats,
    FailedProcessorJobStats,
    InstitutionList,
    OrganismList,
    OriginalFileList,
    PlatformList,
    ProcessorJobList,
    ProcessorList,
    QNTargetsAvailable,
    QNTargetsDetail,
    SampleDetail,
    SampleList,
    Stats,
    SurveyJobList,
    TranscriptomeIndexDetail,
    TranscriptomeIndexList,
    handle404error,
    handle500error,
)


# This provides _public_ access to the /admin interface!
# Enabling this by setting DEBUG to true this will allow unauthenticated access to the admin interface.
# Very useful for debugging (since we have no User accounts), but very dangerous for prod!
class AccessUser:
    has_module_perms = has_perm = __getattr__ = lambda s, *a, **kw: True


if settings.DEBUG:
    admin.site.has_permission = lambda r: setattr(r, "user", AccessUser()) or True

schema_view = get_schema_view(
    openapi.Info(
        title="Refine.bio API",
        default_version="v1",
        description="""
refine.bio is a multi-organism collection of genome-wide transcriptome or gene expression data that has been obtained from publicly available repositories and uniformly processed and normalized. refine.bio allows biologists, clinicians, and machine learning researchers to search for experiments from different source repositories all in one place and build custom data sets for their questions of interest.

The swagger-ui view can be found [here](http://api.refine.bio/swagger/).

The ReDoc view can be found [here](http://api.refine.bio/).

Additional documentation can be found at [docs.refine.bio](http://docs.refine.bio/en/latest/).

### Questions/Feedback?

If you have a question or comment, please [file an issue on GitHub](https://github.com/AlexsLemonade/refinebio/issues) or send us an email at [ccdl@alexslemonade.org](mailto:ccdl@alexslemonade.org).
        """,
        terms_of_service="https://www.refine.bio/terms",
        contact=openapi.Contact(email="ccdl@alexslemonade.org"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    url(
        r"^(?P<version>v1)/",
        include(
            [
                # Primary search and filter interface
                url(r"^search/$", ExperimentDocumentView.as_view({"get": "list"}), name="search"),
                url(r"^experiments/$", ExperimentList.as_view(), name="experiments"),
                url(
                    r"^experiments/(?P<accession_code>.+)/$",
                    ExperimentDetail.as_view(),
                    name="experiments_detail",
                ),
                url(r"^samples/$", SampleList.as_view(), name="samples"),
                url(
                    r"^samples/(?P<accession_code>.+)/$",
                    SampleDetail.as_view(),
                    name="samples_detail",
                ),
                url(r"^organisms/$", OrganismList.as_view(), name="organisms"),
                url(r"^platforms/$", PlatformList.as_view(), name="platforms"),
                url(r"^institutions/$", InstitutionList.as_view(), name="institutions"),
                url(r"^processors/$", ProcessorList.as_view(), name="processors"),
                # Deliverables
                url(r"^dataset/$", CreateDatasetView.as_view(), name="create_dataset"),
                url(r"^dataset/(?P<id>[0-9a-f-]+)/$", DatasetView.as_view(), name="dataset"),
                url(r"^token/$", CreateApiTokenView.as_view(), name="token"),
                url(r"^token/(?P<id>[0-9a-f-]+)/$", APITokenView.as_view(), name="token_id"),
                # Jobs
                url(r"^jobs/survey/$", SurveyJobList.as_view(), name="survey_jobs"),
                url(r"^jobs/downloader/$", DownloaderJobList.as_view(), name="downloader_jobs"),
                url(r"^jobs/processor/$", ProcessorJobList.as_view(), name="processor_jobs"),
                # Dashboard Driver
                url(r"^stats/$", Stats.as_view(), name="stats"),
                url(
                    r"^stats/failures/downloader$",
                    FailedDownloaderJobStats.as_view(),
                    name="stats_failed_downloader",
                ),
                url(
                    r"^stats/failures/processor$",
                    FailedProcessorJobStats.as_view(),
                    name="stats_failed_processor",
                ),
                url(r"^stats-about/$", AboutStats.as_view(), name="stats_about"),
                # Transcriptome Indices
                path(
                    "transcriptome_indices/",
                    include(
                        [
                            path(
                                "", TranscriptomeIndexList.as_view(), name="transcriptome_indices"
                            ),
                            path(
                                "<int:id>",
                                TranscriptomeIndexDetail.as_view(),
                                name="transcriptome_indices_read",
                            ),
                        ]
                    ),
                ),
                # QN Targets
                url(r"^qn_targets/$", QNTargetsAvailable.as_view(), name="qn_targets_available"),
                url(
                    r"^qn_targets/(?P<organism_name>.+)$",
                    QNTargetsDetail.as_view(),
                    name="qn_targets",
                ),
                # Computed Files
                url(r"^computed_files/$", ComputedFilesList.as_view(), name="computed_files"),
                url(r"^original_files/$", OriginalFileList.as_view(), name="original_files"),
                url(
                    r"^computational_results/$", ComputationalResultsList.as_view(), name="results"
                ),
                # Compendia
                url(r"^compendia/$", CompendiumResultList.as_view(), name="compendium_results"),
                url(
                    r"^compendia/(?P<id>[0-9]+)/$",
                    CompendiumResultDetails.as_view(),
                    name="compendium_result",
                ),
                # v1 api docs
                url(
                    r"^swagger/$",
                    schema_view.with_ui("swagger", cache_timeout=0),
                    name="schema_swagger_ui",
                ),
                url(r"^$", schema_view.with_ui("redoc", cache_timeout=0), name="schema_redoc"),
            ]
        ),
    ),
    # Admin
    url(r"^admin/", admin.site.urls),
    # Redirect root urls to latest version api docs
    url(r"^swagger/$", RedirectView.as_view(url="/v1/swagger")),
    url(r"^$", RedirectView.as_view(url="/v1")),
]

# handle errors
handler404 = handle404error
handler500 = handle500error
