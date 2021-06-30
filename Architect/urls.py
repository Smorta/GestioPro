from django.conf.urls import url
from django.urls import include, path
from Architect import views

urlpatterns = [
	url(r'^Home/$',views.index,name='index'),
	url(r'^Chantier/New/$', views.Chantier_new, name='Chantier_new'),
	url(r'^Chantier/Modif/(?P<chant_id>[0-9]+)/$', views.Chantier_modif, name='Chantier_Modif'),
	url(r'^Chantier/Delete(?P<chant_id>[0-9]+)/$', views.chantierDelete, name='Chantier_delete'),
	url(r'^Phase/Modif(?P<phase_id>[0-9]+)/$',views.Phase_modif,name='Phase_modif'),
	url(r'^Phase/New/(?P<chant_id>[0-9]+)(?P<typePhase>\w+)/$', views.Phase_new,name='Phase_new'),
	url(r'^Phase/Save(?P<phase_id>[0-9]+)/$',views.Phase_save,name='Phase_save'),
	url(r'^Phase/Delete(?P<phase_id>[0-9]+)/$', views.phaseDelete, name='Phase_delete'),
	url(r'^RefreshTimelineChant/$', views.refreshScheduleChant, name = 'RefreshScheduleChant'),
	url(r'^RefreshTimelineArchi/$', views.refreshScheduleAchat, name='RefreshScheduleAchat'),
	url(r'^ResizeTask/$', views.resizeTask, name = 'ResizeTask'),
	url(r'^Responsable/New$', views.responsableNew, name='ResponsableNew'),
	url(r'^Responsable/Modif(?P<resp_id>[0-9]+)/$', views.responsableModif, name='ResponsableModif'),
	url(r'^SetDateTimeline/$', views.setDateTimeline, name = 'SetDateTimeline'),
	url(r'^TimelineChant/$', views.scheduleChant, name='timelineChant'),
	url(r'^TimelineArchi/$', views.scheduleArchi, name='timelineArchi')
]
