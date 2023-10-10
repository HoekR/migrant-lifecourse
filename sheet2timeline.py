import pandas as pd
import numpy as np
from helpers import *
from patterns import *
from templates import *

class Sheet2Timeline(object):
    def __init__(self, name, excelfile, 
                 schemes, 
                 mcard=mcard,
                 naa_templt=naa_templ,
                 mcardtmplt=mcardtmplt,
                 youtubetempl=youtubetempl,
                 linktemplate=linktemplate,
                 pat1=pat1,
                 pat2=pat2):
        strik = excelfile.parse(name)
        self.name = name
        self.df = strik
        self.df = self.df[self.df.event.notna()]
        self.df.event = self.df.event.str.strip()
        self.schemes = schemes
        self.mcard = mcard
        self.mcardtmplt = mcardtmplt
        self.naa_templ = naa_templ
        self.youtubetempl = youtubetempl
        self.linktemplate = linktemplate
        self.conversions = conversions
        self.pat1 = pat1
        self.pat2 = pat2
        if len(self.df)==0:
            print(f'{key} has no records, aborting')
        else:
            self.df.rename(columns=str.lower, inplace=True)
            self.df.rename(columns={c: c.strip().replace(' ', '_') for c in self.df.columns}, inplace=True)
            self.df.rename(columns={c: c.strip().replace('-', '_') for c in self.df.columns}, inplace=True)
            self.df.drop([c for c in self.df.columns if 'unnamed' in c], axis=1, inplace=True)
            #self.df = strik[strik.event_type.notna()]
            for c in ['family_name', 'interpositions', 'first_name']: 
                self.df[c] = self.df[c].fillna('')
            self.df['nm'] = self.df.apply(lambda row: row.family_name + ', ' + row.first_name + ' ' + row.interpositions, axis=1)
            self.eventcols = ['event',
                              'event_type',  
                              'notes',
                              'migrant_quotes', 
                              ]
            self.linkcols = {'notes':['source_online','source'],
                            'general':['migration_card','item_id_naa']}
            self.quotes = ['migrant_quotes']
            for c in ['event_type', 'notes', 'migrant_quotes', 'source_online', 'migration_card','item_id_naa']:
                if c in self.df.columns:
                    self.df[c].fillna('', inplace=True)
  

    def make_event(self):
        self.df['eventtext'] = self.df.apply(lambda row: concat_evnt(row, self.eventcols, 
                                                                     self.linkcols, self.quotes,
                                                                     schemes=self.schemes, 
                                                                     mcard=self.mcard,
                                                                     naatempl=self.naa_templ,
                                                                     mcardtmplt=self.mcardtmplt,
                                                                     youtubetempl=self.youtubetempl,
                                                                     linktemplate=self.linktemplate,
                                                                     conversions=self.conversions,
                                                                     pat1=self.pat1,
                                                                     pat2=self.pat2), 
                                                                     axis=1)
        return self.df['eventtext']
        
    
    def make_personcard(self):
        profile = ''
        nddf = self.df[self.df.first_name.notna()]
        main_person = nddf[nddf.first_name.apply(lambda x: name_in_name(x, self.name)) & nddf.relation.isna()]
        mainrow = main_person[main_person.event == 'Birthday']
        mainrow.fillna('', inplace=True)
        d = mainrow.to_dict(orient='records')
        prfl = []
        fields = {'nm':'name', 
                      'date':'birthdate',
                      'location':'place of birth', 
                      'nationality':'nationality', 
                      'religion':'religion', 
                      'occupation':'occupation', 
                      'relation':'relation'}
        if len(d)> 0:
            for k in fields:
                e = ''
                val = d[0].get(k)
                if val and pd.notna(val):
                    kval = fields[k]
                    e = f"<dt>{kval.upper()}</dt>"
                    e += f"<dd>{d[0][k]}</dd>"
                prfl.append(e)
            p = '\n\n'.join(prfl)
            profile = f"<dl>{p}</dl>"
        return profile
    
    def make_family(self):
        famevents = self.df[(self.df.event=='Birthday') & (self.df.relation.notna())] 
        fams = famevents.apply(lambda row: concat_famevents(row, 
                                                            ['nm', 'date', 'relation', 'migration_card', 'item_id_naa'],
                                                            ['migration_card', 'item_id_naa'],
                                                            mcard=self.mcard, 
                                                            conversions=self.conversions,
                                                            mcardtmplt=self.mcardtmplt,
                                                            naa_templ=self.naa_templ,
                                                            pat=self.pat2), axis=1)
        if len(fams)==0:
            result = ''
        else:
            result = f'<ul>{"".join(list(fams))}</ul>' #fams.to_string(index=False)
        return result
    
    def sheet2timeline(self):
        for c in ['day', 'month', 'year']:
            self.df[c] = pd.to_numeric(self.df[c], errors='coerce')
        self.df['date'] = self.df.apply(lambda row: mkdate(row), axis=1)
        self.make_event()
        famevents = self.df[(self.df.event=='Birthday') & (self.df.relation.notna())]
        events = self.df[~self.df.index.isin(list(famevents.index))].reset_index()
        return events
#         self.make_familyname()
        
    def render(self, mask=None):
        select = self.sheet2timeline()
        select['lr'] = np.where(select.index % 2==0, 'right', 'left')
        return select
    
    def __repr__(self):
        return self.name