from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export.resources import ModelResource
from .models import AutoChannel, OldResult, hololiveChannel2,\
    hololiveGenerations, VideoInfo, hololiveSongsResult,\
    videoTypeJudgement,FalseNameCorrect,ListOfJobTitles,\
    AnotherPerson, Lyricist, Composer, Arranger, Mixer,\
    Musician, VideoEditor, Illustrator, CoStar, OriginalSinger
    
#https://noauto-nolife.com/post/django-admin-custom/
class hololiveChannelResource2(ModelResource):
    class Meta:
        model = hololiveChannel2
@admin.register(hololiveChannel2)
class hololiveChannelAdmin2(ImportExportModelAdmin):
    resource_class = hololiveChannelResource2

class hololiveVideoInfoResource(ModelResource):
    class Meta:
        model = VideoInfo
@admin.register(VideoInfo)
class hololiveChannelAdmin2(ImportExportModelAdmin):
    list_per_page  = 1000
    resource_class = hololiveVideoInfoResource

admin.site.register(hololiveGenerations)

# class hololiveSongsResultResource(ModelResource):
#     class Meta:
#         model = hololiveSongsResult
# @admin.register(hololiveSongsResult)
# class hololiveSongsResultAdmin(ImportExportModelAdmin):
#   list_per_page  = 1000
#   resource_class = hololiveSongsResultResource

class hololiveSongsResultAdmin(admin.ModelAdmin):
    list_per_page  = 1000
    list_display = ("pk", "info", "aggregationDate", "viewCount", "likeCount", "viewCount7", "likeCount7", "viewCount30", "likeCount30")

admin.site.register(hololiveSongsResult, hololiveSongsResultAdmin)

admin.site.register(videoTypeJudgement)
admin.site.register(FalseNameCorrect)

class OldResultResource(ModelResource):
    class Meta:
        model = OldResult
@admin.register(OldResult)
class OldResultAdmin(ImportExportModelAdmin):
  list_per_page  = 1000
  resource_class = OldResultResource


class AutoChannelAdmin(admin.ModelAdmin):
  ordering = ("name",)
admin.site.register(AutoChannel,AutoChannelAdmin)

admin.site.register(ListOfJobTitles)

class AnotherPersonResource(ModelResource):
    class Meta:
        model = AnotherPerson
@admin.register(AnotherPerson)
class AnotherPersonAdmin(ImportExportModelAdmin):
  ordering = ("name",)
  list_display = ("pk", "name",)
  resource_class = AnotherPersonResource

class LyricistAdmin(admin.ModelAdmin):
  ordering = ("lyricist__name",)
admin.site.register(Lyricist,LyricistAdmin)

class ComposerAdmin(admin.ModelAdmin):
  ordering = ("composer__name",)
admin.site.register(Composer,ComposerAdmin)

class ArrangerAdmin(admin.ModelAdmin):
  ordering = ("arranger__name",)
admin.site.register(Arranger,ArrangerAdmin)

class MixerAdmin(admin.ModelAdmin):
  ordering = ("mixer__name",)
admin.site.register(Mixer,MixerAdmin)

class MusicianAdmin(admin.ModelAdmin):
  ordering = ("musician__name",)
admin.site.register(Musician,MusicianAdmin)

class VideoEditorAdmin(admin.ModelAdmin):
  ordering = ("videoEditor__name",)
admin.site.register(VideoEditor,VideoEditorAdmin)

class IllustratorAdmin(admin.ModelAdmin):
  ordering = ("illustrator__name",)
admin.site.register(Illustrator,IllustratorAdmin)

class CoStarAdmin(admin.ModelAdmin):
  ordering = ("coStar__name",)
admin.site.register(CoStar,CoStarAdmin)

class OriginalSingerAdmin(admin.ModelAdmin):
  ordering = ("originalSinger__name",)
admin.site.register(OriginalSinger,OriginalSingerAdmin)