from django.contrib import admin

from data_refinery_common.models import (
    ComputationalResult,
    DownloaderJob,
    Experiment,
    OrganismIndex,
    OriginalFile,
    ProcessorJob,
    Sample,
    SurveyJob,
)

admin.site.register(ProcessorJob)
admin.site.register(DownloaderJob)
admin.site.register(SurveyJob)

admin.site.register(Experiment)
admin.site.register(Sample)
admin.site.register(OriginalFile)
admin.site.register(ComputationalResult)
admin.site.register(OrganismIndex)
