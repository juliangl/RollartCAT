from django.contrib import admin

# Register your models here.

from .models import Type,Element,Value,Competition,Category,Level,Program,Territorial,Club,Skater

class ElementAdmin(admin.ModelAdmin):
    list_display=('id','description')
admin.site.register(Element,ElementAdmin)

class TypeAdmin(admin.ModelAdmin):
    list_display=('id','description')
admin.site.register(Type,TypeAdmin)

class ValueAdmin(admin.ModelAdmin):
    list_display=('id','type','element','p3','p2','p1','base','n1','n2','n3')
admin.site.register(Value,ValueAdmin)

class CompetitionAdmin(admin.ModelAdmin):
    list_display=('id','description')
admin.site.register(Competition,CompetitionAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display=('id','description')
admin.site.register(Category,CategoryAdmin)

class LevelAdmin(admin.ModelAdmin):
    list_display=('id','description')
admin.site.register(Level,LevelAdmin)

class ProgramAdmin(admin.ModelAdmin):
    list_display=('id','description')
admin.site.register(Program,ProgramAdmin)

class TerritorialAdmin(admin.ModelAdmin):
    list_display=('id','description')
admin.site.register(Territorial,TerritorialAdmin)

class ClubAdmin(admin.ModelAdmin):
    list_display=('id','name')
admin.site.register(Club,ClubAdmin)

class SkaterAdmin(admin.ModelAdmin):
    list_display=('id','name','club','music')
admin.site.register(Skater,SkaterAdmin)


