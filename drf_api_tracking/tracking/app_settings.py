'''
    maghadire default ro inja moshakhas mikonim. alave bar on inja ye prefix hm gharar 
    mifim mikhaym ye DRF_TRACKING betore automatic ghbl az hameye mtanzimate in app biad.
'''

class AppSettings:
    def __init__(self,prefix):      #prefix
        self.prefix = prefix
        
    def _setting(self, name, default):
        from django.conf import settings
        
        return getattr(settings, self.prefix , default)  #mige boro tooye file settings self.prefix ro vaseye ma 
                                                         #bekhon age ham nabodesh vasamoon meghdare defaulto bargardon.
    
    #hala maghadrire default ro moshakhas mikonim:
    
    @property
    def PATH_LENGTH(self):   
        return self._setting('PATH_LENGTH' , 200)    #boro toye _setting() meghdare 'PATH_LENGTH' ro bekhoon ag
                                                     #hamchin mghdari nabood 200 ro b argardoon.
    
    
'''
    az classemon y instance misaziim be esme app_setting k az in tooye 
    jahaye mokhtalefe barnamamoon estefade mikonim v inke bhsh meghdare 
    prefix 'DRF_TRACKING_' midim. in ebarat avale har tanzimati ke bood
    b barnameye ma marboot mishe baghieye ebarat ro maghadire default
     moshakhas mikonan.
'''    
app_settings=AppSettings('DRF_TRACKING_')   
    