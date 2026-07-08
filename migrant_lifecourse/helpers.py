import os
import pandas as pd

def name_in_name(inp, name):
    result = False
    nms = inp.split(' ')
    for n in nms:
        if n.lower() in name.lower():
            result = True
    return result

def card2local(cardname):
    n = os.path.split(cardname)[-1]
    nn = os.path.splitext(n)[0]
    nnn = nn.split('_')[-2:]
    return '_'.join(nnn)

def yt2nr(naa, pat=''):
    nr = naa
    print (pat, naa)
    n = pat.search(naa)
    try:
        nr = n.groupdict().get('nr')
    except AttributeError:
        pass
    return nr

def concat_evnt(row, 
                cols, 
                links, 
                q, 
                schemes,
                mcard,
                mcardtmplt='',
                naatempl='',
                youtubetempl='',
                linktemplate='',
                conversions={},
                pat1='',
                pat2=''
                ):
    event = []
    for item in cols:
        e = ''
        if item in row.keys():
            if item == 'event':
                e = f'<div class="event">{row[item]}</div>'
            elif item == 'event_type':
                if row[item].lower() in schemes.keys():
                    e += f'<a href="https://migrant.huygens.knaw.nl/{schemes.get(row[item].lower())}">{row[item]}</a>'
                    #print(e)
            else:
                e = f'{row.get(item)}'
                if pd.isna(e):
                    e=''
            if item in q:
                e = f'<em>{e}</em>'
            elif links.get(item):
                for l in links[item]:
                    try:
                        lnk = row[l]
                        if pd.notna(lnk) and lnk.strip()!='':
                            if l=='source_online':
                                if 'youtube' in lnk:
#                                     print(l, lnk)
                                    ytnr = yt2nr(lnk,pat=pat1)
                                    e += youtubetempl.substitute(nr=ytnr)
                                else:
                                    e += linktemplate.substitute(link=lnk, info=f' read more' + ' ' + conversions['ext_link']) #f'<a href="{lnk}">more info</a> <br/>'
                    except KeyError:
                        pass
                for l in links.get('general'):
#                         print(l)
                        try:
                            lnk = row[l]
                            if lnk:
                                if l=='item_id_naa':
                                    lnk = isolate_barcode(lnk, pat=pat2)
                                    lnk = naatempl.substitute(nr=lnk)         
                                elif l=='migration_card':
                                    lnk = card2local(lnk)
                                    lnk = mcard.substitute(card=lnk)
                                e += mcardtmplt.substitute(card=lnk, ctype=conversions.get(item) or 'more info')
#                             if pd.notna(lnk):
#                                 e += linktemplate.substitute(link=lnk, info=f' read more' + ' ' + conversions['ext_link'])
                        except KeyError:
                            pass
        if e != '':
            event.append(e)
    evnt = '</p><p>'.join(event)
    result = f"<p>{evnt}</p>"
    return result 

def mkdate(row):
    date = []
    for part in ['day', 'month', 'year']:
        prt = row.get(part)
        if not pd.isna(prt):
            date.append(int(prt))
    if date:
        try:
            date = [str(d) for d in date]
            result = '-'.join(date)
            return result
        except ValueError:
            print (row, date)

def isolate_barcode(inp, pat=''):
    res = pat.search(inp)
    gd = res.groupdict()
    result = gd.get('bc')
    return result
        
    
def concat_famevents(row, 
                     cols, 
                     links, 
                     conversions={},
                     mcard='',
                     mcardtmplt='',
                     naa_templ='',
                     pat=''):
    event = []
    for item in cols:
        e = ''
        if item in row.keys():
#             print(item)
            txt = row[item]
            if pd.notna(txt):
                if item in links:
                    if txt.strip() != '':
                        if item=='item_id_naa':
                            txt = isolate_barcode(txt, pat=pat)
                            txt = naa_templ.substitute(nr=txt)
                        if item=='migration_card':
                            txt = card2local(txt)
                            txt = mcard.substitute(card=txt)
                        e += mcardtmplt.substitute(card=txt, ctype=conversions.get(item) or 'more info')
                else:
                    e = f' {txt} '
        if e != '':
            event.append(e)
    evnt = '-'.join(event)
    result = f"<li>{evnt}</li>"
    return result