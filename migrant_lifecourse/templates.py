from string import Template

linktemplate = Template('<a href="$link" target="details">$info</a>')
mcardtmplt = Template('<a href="$card" target="image" rel="noopener"> $ctype</a>')

naa_templ = Template("https://recordsearch.naa.gov.au/SearchNRetrieve/Interface/ViewImage.aspx?B=$nr")

mcard = Template("/$card")

youtubetempl = Template("""<iframe width="420" height="315"
src="https://www.youtube.com/embed/$nr">
</iframe>""")

conversions = {'migration_card':'<img src="/wp-content/uploads/2022/05/mkaart_small.jpg" alt="migrant card thumbnail" />',
               'item_id_naa':'<img src="/wp-content/uploads/2022/05/naa_thmb.jpg" alt="naa recordsearch thumbnail" />',
               'ext_link': '<img src="/wp-content/uploads/2022/05/link_external.png" height="15" width="15" alt="external link" />'
              }

grid_templ = Template("""<div class="grid-container">
  <div class="personinfo">$personinfo</div>
  <div class="familyinfo">$family</div>
</div>""")

toptmpt = Template("""<div class="grid-container">
  <div class="personinfo">$personinfo</div>
  <div class="familyinfo">$family</div>
  </div>
  <div class="timeline">$events</div>""")

tmplt = Template("""
 <div class="container $l_or_r">
   <div class="content">
	 <h2>$date</h2>
	 <p>$item</p>
   </div>
 </div>
""")

container = Template("""<!DOCTYPE html>
<html>
<head/>
<body>
<img class="alignnone wp-image-256" src="/wp-content/uploads/2022/05/puzzle_flags-300x158.png" alt="" width="152" height="80" />
$body
</body>
</html>""")